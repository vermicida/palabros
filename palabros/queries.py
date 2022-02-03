class Query:

    """
    This is just a query catalog.
    """

    WordExists = """
        SELECT
            COUNT(w.word) AS total
        FROM
            words AS w
        WHERE
            w.word = ?;
    """

    GetRandomWord = """
        SELECT
            w.word
        FROM
            words AS w
            LEFT OUTER JOIN
                games AS g ON w.word = g.word
        WHERE
            g.id IS NULL
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
