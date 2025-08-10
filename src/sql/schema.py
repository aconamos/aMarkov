"""
This file contains virtually every action you could ever want to take on the database
in the context of this bot.
"""

from sqlite3 import Connection
from discord import Message
from loguru import logger


def write_schema(database: Connection):
    logger.trace("creating database if necessary...")

    database.execute("""
    CREATE TABLE IF NOT EXISTS servers
        (
            id              INTEGER PRIMARY KEY NOT NULL,
            probability     REAL NOT NULL DEFAULT 5,
            enabled         INTEGER NOT NULL DEFAULT 1,
            mentions        INTEGER NOT NULL DEFAULT 1,
            equal_chance    INTEGER NOT NULL DEFAULT 0
        ) STRICT
        ;
    """)

    database.execute("""
    CREATE TABLE IF NOT EXISTS messages
        (
            id              INTEGER PRIMARY KEY NOT NULL,
            guild_id        INTEGER NOT NULL,
            channel_id      INTEGER NOT NULL,
            author_id       INTEGER NOT NULL,
            content         TEXT,
            FOREIGN KEY(guild_id) REFERENCES servers(id)
        ) STRICT
        ;
    """)

    database.commit()


def fetch_config(guild_id: int, database: Connection) -> None | tuple[int, float, bool, bool, bool]:
    logger.trace(f"fetching server config for guild_id: {guild_id}")

    res = database.execute(f"""
    SELECT *
    FROM servers
    WHERE
        id = {guild_id}
        ;
    """).fetchone()

    if res is None:
        logger.trace("server is not configured, not proceeding")
        return

    id, probability, enabled, mentioned, equal_chance = res

    enabled = True if enabled == 1 else False
    mentioned = True if enabled == 1 else False
    equal_chance = True if enabled == 1 else False

    return (id, probability, enabled, mentioned, equal_chance)


def fetch_log(guild_id: int, database: Connection):
    logger.trace(f"fetching logs for guild_id: {guild_id}")

    res = database.execute(f"""
    SELECT (content)
    FROM messages
    WHERE
        guild_id = {guild_id}
        ;
    """).fetchall()

    return [row[0] for row in res]


def _query_bool(guild_id: int, field: str, database: Connection) -> bool:
    logger.trace(f"querying {field} (bool) for guild_id: {guild_id}")

    enabled = database.execute(f"""
    SELECT ({field})
    FROM servers
    WHERE
        id = {guild_id}
        ;
    """).fetchone()[0]

    enabled = True if enabled == 1 else False

    return enabled


def _toggle_bool(guild_id: int, field: str, database: Connection) -> bool:
    logger.trace(f"setting {field} (bool) for guild_id: {guild_id}")

    enabled = query_enabled(guild_id, database)

    database.execute(f"""
    UPDATE servers
    SET
        {field} = {0 if enabled else 1}
    WHERE
        id = {guild_id}
        ;
    """)

    database.commit()

    return not enabled


def query_enabled(guild_id: int, database: Connection) -> bool:
    return _query_bool(guild_id, "enabled", database)


def toggle_enabled(guild_id: int, database: Connection) -> bool:
    return _toggle_bool(guild_id, "enabled", database)


def query_mentions(guild_id: int, database: Connection) -> bool:
    return _query_bool(guild_id, "mentions", database)


def toggle_mentions(guild_id: int, database: Connection) -> bool:
    return _toggle_bool(guild_id, "mentions", database)


def query_equal_chance(guild_id: int, database: Connection) -> bool:
    return _query_bool(guild_id, "equal_chance", database)


def toggle_equal_chance(guild_id: int, database: Connection) -> bool:
    return _toggle_bool(guild_id, "equal_chance", database)


def query_probability(guild_id: int, database: Connection) -> float:
    logger.trace(f"querying probability for guild_id: {guild_id}")

    probability: float = database.execute(f"""
    SELECT (probability)
    FROM servers
    WHERE
        id = {guild_id}
        ;
    """).fetchone()[0]

    return probability


def set_probability(guild_id: int, probability: int, database: Connection):
    logger.trace(f"setting probability to {probability} for guild_id: {guild_id}")

    assert probability > 0
    assert probability <= 100

    database.execute(
        f"""
        UPDATE servers
        SET
            probability = ?
        WHERE
            id = {guild_id}
            ;
        """,
        [probability],
    )

    database.commit()


def create_message(message: Message, database: Connection):
    assert message.guild is not None

    logger.trace("inserting message into db...")

    database.execute(
        """
    INSERT INTO messages
        (id, guild_id, channel_id, author_id, content)
    VALUES
        (?, ?, ?, ?, ?)
        ;
    """,
        [
            message.id,
            message.guild.id,
            message.channel.id,
            message.author.id,
            message.content,
        ],
    )

    database.commit()


def server_present(guild_id: int, database: Connection):
    return (
        database.execute(f"""
        SELECT *
        FROM servers
        WHERE
            id = {guild_id}
            ;
    """).fetchone()
        is not None
    )


def init_server(guild_id: int, database: Connection):
    logger.trace(f"initializing guild_id: {guild_id}")

    id, probability, enabled, mentions, equal_chance = database.execute(f"""
        INSERT INTO servers
            (id)
        VALUES
            ({guild_id})
        RETURNING
            *
            ;
        """).fetchone()

    enabled = True if enabled == 1 else False
    mentions = True if mentions == 1 else False
    equal_chance = True if equal_chance == 1 else False

    database.commit()

    return (id, probability, enabled, mentions, equal_chance)
