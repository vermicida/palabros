import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from palabros import __version__
from palabros.errors import DatabaseError
from palabros.queries import Query

_APP_PATH = Path.home().joinpath(".palabros")
_DB_PATH = _APP_PATH.joinpath("games.db")
_WORDS_JSON_PATH = Path(__file__).parent.joinpath("words.json")


@contextmanager
def db_cursor() -> Generator[sqlite3.Cursor, None, None]:

    """
    Create a cursor to interact with the database.

    Yields:
        An instance of `sqlite3.Cursor`.

    Raises:
        DatabaseError: if any error occurred while working with the database.
    """

    try:
        with sqlite3.connect(
            os.getenv("PALABROS_DB_PATH", str(_DB_PATH)),
            isolation_level=None,
        ) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            yield cur
    except sqlite3.DatabaseError as err:
        raise DatabaseError(str(err)) from err


def _generate_words_population_query() -> str:

    """
    Generate the query to populate the words table.

    Returns:
        The query, ready to execute.
    """

    with open(_WORDS_JSON_PATH) as f:
        words = json.load(f)
    values = ", ".join([f"('{k}', {v})" for k, v in words.items()])
    return Query.PopulateWordsTable.format(values)


def _table_exists(table: str) -> bool:

    """
    Check if the given table exists in the database.

    Args:
        table: The table to check.

    Returns:
        True if the table exists in the database; otherwise False.
    """

    with db_cursor() as cur:
        cur.execute(Query.TableExists, (table,))
        result = cur.fetchone()

    return result is not None and bool(result["total"])


def init() -> None:

    """
    Initialize the database.
    """

    if not _APP_PATH.exists():
        _APP_PATH.mkdir(parents=True, exist_ok=True)

    if _DB_PATH.exists():
        if _table_exists("versions"):
            return
        # Force old database rebuilding
        _DB_PATH.unlink(missing_ok=True)

    with db_cursor() as cur:
        cur.execute(Query.CreateVersionsTable)
        cur.execute(Query.CreateWordsTable)
        cur.execute(Query.CreateGamesTable)
        cur.execute(Query.CreateAttemptsTable)
        cur.execute(Query.CreateGamesDateIndex)
        cur.execute(Query.CreateVersion, (__version__,))
        cur.execute(_generate_words_population_query())
