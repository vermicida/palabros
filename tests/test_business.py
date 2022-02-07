import random

import pytest

from palabros import business
from palabros.database import db_cursor
from palabros.errors import DatabaseError, GameError
from palabros.queries import Query
from palabros.schemas import CharInspection
from tests.base import WORDS, BaseTestCase


@pytest.mark.usefixtures("init_database")
class BusinessTestCase(BaseTestCase):

    """
    Test case for the `palabros.business` module.
    """

    def test_normalize_word(self) -> None:
        text = "ánfora murciélago níscalo camión baúl zarigüeya"
        expected = "anfora murcielago niscalo camion baul zarigueya"
        self.assertNotEqual(text, business._normalize_word(text))
        self.assertEqual(expected, business._normalize_word(text))

    def test_get_random_word__no_word_found(self) -> None:
        with db_cursor() as cur:
            cur.execute("DELETE FROM words;")
        self.assertRaises(DatabaseError, business._get_random_word)

    def test_get_random_word(self) -> None:
        word = WORDS[random.randint(0, len(WORDS) - 1)]
        words = [w for w in WORDS if w != word]
        with db_cursor() as cur:
            cur.execute(Query.CreateGame, (word, ""))
        result = business._get_random_word()
        self.assertIn(result, words)

    def test_inspect_attempt__wrong_seed_word_length(self) -> None:
        self.assertRaises(
            GameError,
            business._inspect_attempt,
            "seed-word-with-bad-length",
            "leche",
        )

    def test_inspect_attempt__wrong_user_word_length(self) -> None:
        self.assertRaises(
            GameError,
            business._inspect_attempt,
            "leche",
            "user-word-with-bad-length",
        )

    def test_inspect_attempt(self) -> None:
        seed = "coche"
        word = "leche"
        inspection = business._inspect_attempt(seed, word)

        self.assertIsInstance(inspection, list)
        self.assertEqual(len(inspection), 5)

        char = inspection[0]
        self.assertIsInstance(char, CharInspection)
        self.assertEqual(char.char, "L")
        self.assertEqual(char.position, 0)
        self.assertFalse(char.valid)
        self.assertFalse(char.missplaced)

        char = inspection[1]
        self.assertIsInstance(char, CharInspection)
        self.assertEqual(char.char, "E")
        self.assertEqual(char.position, 1)
        self.assertFalse(char.valid)
        self.assertTrue(char.missplaced)

        char = inspection[2]
        self.assertIsInstance(char, CharInspection)
        self.assertEqual(char.char, "C")
        self.assertEqual(char.position, 2)
        self.assertTrue(char.valid)
        self.assertFalse(char.missplaced)

        char = inspection[3]
        self.assertIsInstance(char, CharInspection)
        self.assertEqual(char.char, "H")
        self.assertEqual(char.position, 3)
        self.assertTrue(char.valid)
        self.assertFalse(char.missplaced)

        char = inspection[4]
        self.assertIsInstance(char, CharInspection)
        self.assertEqual(char.char, "E")
        self.assertEqual(char.position, 4)
        self.assertFalse(char.valid)
        self.assertFalse(char.missplaced)

    def test_word_exists(self) -> None:

        word = WORDS[random.randint(0, len(WORDS) - 1)]
        result = business.word_exists(word)
        self.assertTrue(result)

        word = "movil"
        result = business.word_exists(word)
        self.assertFalse(result)
