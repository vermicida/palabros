class Query:

    """
    This is just a query catalog.
    """

    WordExists = """
        SELECT
            COUNT(*) AS total
        FROM
            words AS w
        WHERE
            w.word = ?;
    """

    GetRandomWord = """
        SELECT
            w.word
        FROM (
            SELECT
                w.word
            FROM
                words AS w
                LEFT OUTER JOIN
                    games AS g ON w.word = g.word
            WHERE
                g.id IS NULL
            ORDER BY
                w.frequency DESC
            LIMIT
                50
        ) as w
        ORDER BY
            RANDOM()
        LIMIT
            1;
    """

    GetGameByDate = """
        SELECT
            g.id,
            g.word,
            g.date
        FROM
            games AS g
        WHERE
            g.date = ?;
    """

    CreateGame = """
        INSERT INTO
            games (
                word,
                date
            )
        VALUES (
            ?,
            ?
        );
    """

    GetAttemptsByGame = """
        SELECT
            a.id,
            a.word,
            a.match
        FROM
            attempts AS a
        WHERE
            a.game_id = ?;
    """

    CreateAttempt = """
        INSERT INTO
            attempts (
                game_id,
                word,
                match
            )
        VALUES (
            ?,
            ?,
            ?
        );
    """

    TableExists = """
        SELECT
            COUNT(*) AS total
        FROM
            sqlite_master
        WHERE
            type = 'table'
        AND
            name = ?;
    """

    CreateVersionsTable = """
        CREATE TABLE IF NOT EXISTS versions (
            version TEXT PRIMARY KEY
        );
    """

    CreateWordsTable = """
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            frequency REAL NOT NULL
        );
    """

    CreateGamesTable = """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (word) REFERENCES words (word)
        );
    """

    CreateAttemptsTable = """
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            match INTEGER NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id)
        );
    """

    CreateGamesDateIndex = """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_games_date ON games (date);
    """

    PopulateWordsTable = """
        INSERT OR IGNORE INTO words (word, frequency) VALUES {};
    """

    CreateVersion = """
        INSERT INTO
            versions (
                version
            )
        VALUES (
            ?
        );
    """
