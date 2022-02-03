from enum import Enum, unique


@unique
class ErrorCode(str, Enum):

    """
    The available error codes.
    """

    DatabaseErrorCode = "palabros.databaseError"
    GameErrorCode = "palabros.gameError"


class PalabrosError(Exception):

    """
    Generic error.
    """

    @property
    def code(self) -> str:

        """
        Get the error code.

        Returns:
            The error code.
        """

        return self._code

    @property
    def message(self) -> str:

        """
        Get the error message.

        Returns:
            The error message.
        """

        return self._message

    def __init__(self, code: str, message: str) -> None:

        """
        Class constructor.

        Args:
            code: The error code.
            message: The message code.
        """

        self._code = code
        self._message = message

    def __str__(self) -> str:

        """
        Get a readable representation of the exception.

        Returns:
            A string representing the exception.
        """

        return self.message

    def __repr__(self) -> str:

        """
        Get an unambiguous representation of the exception.

        Returns:
            A string representing the exception.
        """

        return f"<{self.__class__.__name__} code={self.code}> {self.message}"


class DatabaseError(PalabrosError):

    """
    An exception raised when an error occurred while working with the database.
    """

    def __init__(self, message: str) -> None:

        """
        Class constructor.

        Args:
            message: The message code.
        """

        super().__init__(ErrorCode.DatabaseErrorCode, message)


class GameError(PalabrosError):

    """
    An exception raised when an error occurred while working a `Game` business logic.
    """

    def __init__(self, message: str) -> None:

        """
        Class constructor.

        Args:
            message: The message code.
        """

        super().__init__(ErrorCode.GameErrorCode, message)
