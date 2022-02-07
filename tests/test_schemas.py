from palabros import schemas
from tests.base import BaseTestCase


class GameSchemaTestCase(BaseTestCase):

    """
    Test case for the `palabros.schemas.Game` class.
    """

    def test_any_match(self) -> None:
        game = schemas.Game(1, "", "")
        self.assertFalse(game.any_match())
        game.attempts.append(schemas.Attempt(1, "", False))
        self.assertFalse(game.any_match())
        game.attempts.append(schemas.Attempt(2, "", True))
        self.assertTrue(game.any_match())

    def test_any_attempt_left(self) -> None:
        game = schemas.Game(1, "", "")
        self.assertTrue(game.any_attempt_left())
        for i in range(game.max_attempts):
            game.attempts.append(schemas.Attempt(i, "", False))
        self.assertFalse(game.any_attempt_left())

    def test_get_attempts_left(self) -> None:
        game = schemas.Game(1, "", "")
        for i in range(game.max_attempts):
            game.attempts.append(schemas.Attempt(i, "", False))
            expected = game.max_attempts - i - 1
            self.assertEqual(expected, game.get_attempts_left())
