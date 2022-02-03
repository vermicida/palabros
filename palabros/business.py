from collections import Counter
from datetime import datetime
from typing import List

from palabros.database import db_cursor
from palabros.errors import DatabaseError, GameError
from palabros.queries import Query
from palabros.schemas import Attempt, CharInspection, Game

WORD_LENGTH = 5


def _normalize_word(word: str) -> str:

    """
    Normalize a given word.

    Args:
        word: The word to normalize.

    Returns:
        The properly normalized word.
    """

    return word.translate(str.maketrans("áéíóúü", "aeiouu"))


def _get_random_word() -> str:

    """
    Get a random word from the database

    Returns:
        The word retrieved from the database.

    Raises:
        DatabaseError: if no word could be retrieved from the database.
    """

    with db_cursor() as cur:
        cur.execute(Query.GetRandomWord)
        result = cur.fetchone()

    if result is None:
        raise DatabaseError("No se ha podido generar una palabra para el juego de hoy")

    return result["word"]


def _inspect_attempt(seed: str, word: str) -> List[CharInspection]:

    """
    Inspect every char in the given attempt against a seed word.

    Args:
        seed: The seed word, which the player tries to guess.
        word: The word given by the player.

    Returns:
        A list of `CharInspection` instances.

    Raises:
        GameError: if the seed word or the one given by the player has a wrong length.
    """

    if len(seed) != WORD_LENGTH:
        raise GameError(f"La palabra semilla tiene que tener [bold]{WORD_LENGTH}[/] letras")

    if len(word) != WORD_LENGTH:
        raise GameError(f"La palabra tiene que tener [bold]{WORD_LENGTH}[/] letras")

    result = []
    word = _normalize_word(word)
    upper_seed = seed.upper()
    occurrences = Counter(char[0] for char in upper_seed)

    for i in range(WORD_LENGTH):

        inspection = CharInspection(
            char=word[i].upper(),
            position=i,
        )

        if inspection.char in upper_seed and occurrences[inspection.char] > 0:
            if upper_seed[i] == inspection.char:
                inspection.valid = True
            else:
                inspection.missplaced = True
            occurrences[inspection.char] -= 1

        result.append(inspection)

    return result


def word_exists(word: str) -> bool:

    """
    Check if the given word exists in the database dictionary.

    Args:
        word: The word to check.

    Returns:
        True if the word exists in the database dictionary; otherwise False.
    """

    with db_cursor() as cur:
        cur.execute(Query.WordExists, (_normalize_word(word),))
        result = cur.fetchone()

    return result is not None and bool(result["total"])


def get_current_game() -> Game:

    """
    Get the current game if it's already ongoing; otherwise create a new one.

    Returns:
        An instance of `Game` with the current game.
    """

    today = datetime.now().strftime("%Y%m%d")

    # Retrieve the current game
    with db_cursor() as cur:
        cur.execute(Query.GetGameByDate, (today,))
        game = cur.fetchone()

    # Create a new game
    if game is None:
        word = _get_random_word()
        with db_cursor() as cur:
            cur.execute(Query.CreateGame, (word, today))
            game_id = cur.lastrowid
        return Game(game_id, word, today)

    # Retrieve the current game's attempts
    with db_cursor() as cur:
        cur.execute(Query.GetAttemptsByGame, (game["id"],))
        attempts = cur.fetchall()

    return Game(
        game["id"],
        game["word"],
        game["date"],
        [
            Attempt(
                attempt["id"],
                attempt["word"],
                bool(attempt["match"]),
                _inspect_attempt(
                    game["word"],
                    attempt["word"],
                ),
            )
            for attempt in attempts
        ],
    )


def play_game(game: Game, word: str) -> Attempt:

    """
    Try to guess the seed word.

    Args:
        game: The current game.
        word: The word given by the player.

    Returns:
        An instance of `Attempt` with the result.
    """

    inspection = _inspect_attempt(game.word, word)
    match = all([char.valid for char in inspection])

    # Create a new attempt
    with db_cursor() as cur:
        cur.execute(Query.CreateAttempt, (game.id, word, match))
        attempt_id = cur.lastrowid

    # Add the attempt to the current game
    return Attempt(
        id=attempt_id,
        word=word,
        match=match,
        chars=inspection,
    )
