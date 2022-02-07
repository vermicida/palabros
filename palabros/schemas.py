from dataclasses import dataclass, field
from typing import List


@dataclass
class CharInspection:

    """
    Schema representing an inspection of an attempt word char.
    """

    char: str
    position: int
    valid: bool = False
    missplaced: bool = False


@dataclass
class Attempt:

    """
    Schema representing a database `Attempt` record.
    """

    id: int
    word: str
    match: bool
    chars: List[CharInspection] = field(default_factory=list)


@dataclass
class Game:

    """
    Schema representing a database `Game` record.
    """

    id: int
    word: str
    date: str
    attempts: List[Attempt] = field(default_factory=list)
    max_attempts: int = 6

    def any_match(self) -> bool:

        """
        Check if any of the attempts did a match.

        Returns:
            True if a match is found; otherwise False.
        """

        return any([attempt.match for attempt in self.attempts])

    def any_attempt_left(self) -> bool:

        """
        Check if there is any attempt left.

        Returns:
            True when one or more attempts are left; otherwise, False.
        """

        return len(self.attempts) < self.max_attempts

    def get_attempts_left(self) -> int:

        """
        Get the number of the attempts left.

        Returns:
            The number of the attempts left.
        """

        return self.max_attempts - len(self.attempts)
