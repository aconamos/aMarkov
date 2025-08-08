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
