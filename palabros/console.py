from datetime import datetime, time, timedelta
from typing import List

from rich.console import Console
from rich.padding import Padding
from rich.table import Table, box

from palabros.business import WORD_LENGTH
from palabros.schemas import Attempt, Game


def _generate_attempt_row(attempt: Attempt) -> List[Padding]:

    """
    Generate a table row with the given attempt info.

    Args:
        attempt: The attempt result to show.

    Returns:
        A list of `rich.padding.Padding` instances.
    """

    return [
        Padding(
            char.char,
            1,
            style="bold black on green"
            if char.valid
            else "bold black on yellow"
            if char.missplaced
            else "bold white on black",
        )
        for char in sorted(attempt.chars, key=lambda x: x.position)
    ]


def _generate_empty_row(cols: int = WORD_LENGTH) -> List[str]:

    """
    Generate and empty table row.

    Args:
        cols: The number of columns.

    Returns:
        A list of `rich.padding.Padding` instances.
    """

    return [Padding("", 1) for _ in range(cols)]


def _create_table(game: Game) -> Table:

    """
    Create a table to show the given game status.

    Args:
        game: The game to show.

    Returns:
        An instance of `rich.table.Table`.
    """

    table = Table(
        show_header=False,
        show_footer=False,
        show_lines=True,
        box=box.HEAVY,
    )

    table.add_column(width=5, justify="center")
    table.add_column(width=5, justify="center")
    table.add_column(width=5, justify="center")
    table.add_column(width=5, justify="center")
    table.add_column(width=5, justify="center")

    for attempt in game.attempts:
        table.add_row(*_generate_attempt_row(attempt))

    for _ in range(game.get_attempts_left()):
        table.add_row(*_generate_empty_row())

    return table


def _get_countdown() -> str:

    """
    Calculate the countdown to the moment the user can play again.

    Returns:
        The countdown, given as a string.
    """

    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    midnight = datetime.combine(tomorrow.date(), time(0, 0))
    countdown = midnight - now
    hours, remainder = divmod(countdown.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{str(hours).rjust(2, "0")}:{str(minutes).rjust(2, "0")}:{str(seconds).rjust(2, "0")}'


def print_error(message: str) -> None:

    """
    Print the given error message in the console.

    Args:
        message: The message to print.
    """

    console = Console()
    console.print(f"\n{message}\n")


def print_result(game: Game) -> None:

    """
    Print the status of the given game in the console.

    Args:
        game: The game which status should be printed.
    """

    message = (
        f"¡Bien hecho! Siguiente palabra en [bold]{_get_countdown()}[/]."
        if game.any_match()
        else f"¡Has fallado! Te quedan [bold]{game.get_attempts_left()}[/] intentos."
        if game.any_attempt_left()
        else f"¡Tenías que acertar [bold]{game.word.upper()}[/]! Siguiente palabra en [bold]{_get_countdown()}[/]."
    )

    console = Console()
    console.print(_create_table(game))
    console.print(f"\n{message}\n")
