import os
import sqlite3
from typing import Generator

import pytest

os.environ["PALABROS_DB_PATH"] = "file::memory:?cache=shared"

from palabros import __version__  # noqa:E402
from palabros.database import db_cursor  # noqa:E402
from palabros.queries import Query  # noqa:E402
from tests.base import WORDS  # noqa:E402


@pytest.fixture(scope="function")
def init_database() -> Generator[sqlite3.Cursor, None, None]:
    with db_cursor() as cur:
        cur.execute(Query.CreateVersionsTable)
        cur.execute(Query.CreateWordsTable)
        cur.execute(Query.CreateGamesTable)
        cur.execute(Query.CreateAttemptsTable)
        cur.execute(Query.CreateGamesDateIndex)
        cur.execute(Query.CreateVersion, (__version__,))
        values = ",".join([f"('{w}',{i})" for i, w in enumerate(WORDS)])
        cur.execute(Query.PopulateWordsTable.format(values))
        yield
