import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.sqlite3')

_SCHEMA = """
CREATE TABLE IF NOT EXISTS "247" (
    "guild_id"  INTEGER,
    "channel_id" INTEGER,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "afk" (
    "user_id" INTEGER,
    "afkk" TEXT DEFAULT '{}',
    "globally" INTEGER DEFAULT 0,
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "auto" (
    "guild_id" INTEGER,
    "humans" TEXT,
    "bots" TEXT,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "badges" (
    "user_id" INTEGER,
    "BUG" INTEGER DEFAULT 0,
    "DONATOR" INTEGER DEFAULT 0,
    "SPECIAL" INTEGER DEFAULT 0,
    "SUPPORTER" INTEGER DEFAULT 0,
    "FRIEND" INTEGER DEFAULT 0,
    "VIP" INTEGER DEFAULT 0,
    "OWNER" INTEGER DEFAULT 0,
    "DEVELOPER" INTEGER DEFAULT 0,
    "STAFF" INTEGER DEFAULT 0,
    "ADMIN" INTEGER DEFAULT 0,
    "MOD" INTEGER DEFAULT 0,
    "PREMIUM" INTEGER DEFAULT 0,
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "bl" (
    "main" INTEGER DEFAULT 1,
    "user_ids" TEXT DEFAULT '[]',
    PRIMARY KEY("main")
);

CREATE TABLE IF NOT EXISTS "bot" (
    "bot_id" INTEGER,
    "totaltime" INTEGER DEFAULT 0,
    "server" TEXT DEFAULT '{}',
    "user" TEXT DEFAULT '{}',
    PRIMARY KEY("bot_id")
);

CREATE TABLE IF NOT EXISTS "bypass" (
    "guild_id" INTEGER,
    "bypass_users" TEXT DEFAULT '{}',
    "bypass_roles" TEXT DEFAULT '{}',
    "bypass_channels" TEXT DEFAULT '{}',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "count" (
    "xd" INTEGER DEFAULT 1,
    "guild_count" TEXT DEFAULT '{}',
    "cmd_count" TEXT DEFAULT '{}',
    "user_count" TEXT DEFAULT '{}',
    PRIMARY KEY("xd")
);

CREATE TABLE IF NOT EXISTS "daily" (
    "id" INTEGER,
    "guild" INTEGER DEFAULT 0,
    "user" INTEGER DEFAULT 0,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "gwmain" (
    "guild_id" INTEGER,
    "gw" TEXT DEFAULT '{}',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "help" (
    "main" INTEGER DEFAULT 1,
    "no" INTEGER,
    PRIMARY KEY("main")
);

CREATE TABLE IF NOT EXISTS "ignore" (
    "guild_id" INTEGER,
    "cmd" TEXT DEFAULT '[]',
    "channel" TEXT DEFAULT '[]',
    "user" TEXT DEFAULT '[]',
    "role" TEXT DEFAULT '[]',
    "module" TEXT DEFAULT '[]',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "imp" (
    "guild_id" INTEGER,
    "cmd" TEXT DEFAULT 0,
    "admin" TEXT DEFAULT 0,
    "kick" TEXT DEFAULT 0,
    "ban" TEXT DEFAULT 0,
    "mgn" TEXT DEFAULT 0,
    "mgnch" TEXT DEFAULT 0,
    "mgnro" TEXT DEFAULT 0,
    "mention" TEXT DEFAULT 0,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "invc" (
    "guild_id" INTEGER,
    "vc" TEXT DEFAULT '{}',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "lockr" (
    "guild_id" INTEGER,
    "role_id" TEXT DEFAULT '[]',
    "bypass_uid" TEXT DEFAULT '[]',
    "bypass_rid" TEXT DEFAULT '[]',
    "m_list" TEXT DEFAULT '{}',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "logs" (
    "guild_id" INTEGER,
    "mod" INTEGER,
    "role" INTEGER,
    "channel" INTEGER,
    "server" INTEGER,
    "member" INTEGER,
    "message" INTEGER,
    "antinuke" INTEGER,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "main" (
    "xd" INTEGER DEFAULT 77,
    "nopre" TEXT DEFAULT '[]',
    "bperm" TEXT DEFAULT '[]',
    PRIMARY KEY("xd")
);

CREATE TABLE IF NOT EXISTS "messages_db" (
    "guild_id" INTEGER,
    "messages" TEXT DEFAULT '{}',
    "daily_messages" TEXT DEFAULT '{}',
    "bl_channels" TEXT DEFAULT '[]',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "noprefix" (
    "user_id" INTEGER,
    "servers" TEXT,
    "main" INTEGER DEFAULT 0,
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "panel" (
    "guild_id" INTEGER,
    "channel_id" INTEGER,
    "msg_id" INTEGER,
    "opencategory" INTEGER,
    "closedcategory" INTEGER,
    "claimedrole" INTEGER,
    "supportrole" INTEGER,
    "pingrole" INTEGER,
    "name" TEXT,
    "msg" TEXT DEFAULT 'To create a ticket interact with the button below 📩',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "pfp" (
    "guild_id" INTEGER,
    "channel_id" INTEGER,
    "type" TEXT,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "pl" (
    "user_id" INTEGER,
    "pl" TEXT DEFAULT '{}',
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "prefixes" (
    "guild_id" INTEGER,
    "prefix" TEXT DEFAULT '-',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "punish" (
    "guild_id" INTEGER,
    "PUNISHMENT" TEXT DEFAULT 'BAN',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "raidmode" (
    "guild_id" INTEGER,
    "toggle" INTEGER DEFAULT 0,
    "time" INTEGER DEFAULT 10,
    "max" INTEGER DEFAULT 15,
    "PUNISHMENT" TEXT DEFAULT 'KICK',
    "lock" INTEGER DEFAULT 0,
    "lockdown" INTEGER DEFAULT 1,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "roles" (
    "guild_id" INTEGER,
    "role" INTEGER DEFAULT 0,
    "official" INTEGER DEFAULT 0,
    "vip" INTEGER DEFAULT 0,
    "guest" INTEGER DEFAULT 0,
    "girls" INTEGER DEFAULT 0,
    "tag" TEXT,
    "friend" INTEGER DEFAULT 0,
    "custom" TEXT DEFAULT '{}',
    "ar" INTEGER DEFAULT 0,
    "stag" TEXT,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "setup" (
    "guild_id" INTEGER,
    "channel_id" INTEGER,
    "msg_id" INTEGER,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "srmain" (
    "guild_id" INTEGER,
    "data_button" TEXT DEFAULT '[]',
    "data_dropdown" TEXT DEFAULT '[]',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "ticket" (
    "guild_id" INTEGER,
    "name" TEXT,
    "count" INTEGER DEFAULT 0,
    "opendata" TEXT DEFAULT '{}',
    "closeddata" TEXT DEFAULT '{}',
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "titles" (
    "user_id" INTEGER,
    "title" TEXT,
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "todo" (
    "user_id" INTEGER,
    "todo" TEXT DEFAULT '[]',
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "toggle" (
    "guild_id" INTEGER,
    "BAN" INTEGER DEFAULT 0,
    "BOT" INTEGER DEFAULT 0,
    "KICK" INTEGER DEFAULT 0,
    "ROLE CREATE" INTEGER DEFAULT 0,
    "ROLE DELETE" INTEGER DEFAULT 0,
    "ROLE UPDATE" INTEGER DEFAULT 0,
    "CHANNEL CREATE" INTEGER DEFAULT 0,
    "CHANNEL DELETE" INTEGER DEFAULT 0,
    "CHANNEL UPDATE" INTEGER DEFAULT 0,
    "MEMBER UPDATE" INTEGER DEFAULT 0,
    "GUILD UPDATE" INTEGER DEFAULT 0,
    "WEBHOOK" INTEGER DEFAULT 0,
    "ALL" INTEGER DEFAULT 0,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "user" (
    "user_id" INTEGER,
    "totaltime" INTEGER DEFAULT 0,
    "server" TEXT DEFAULT '{}',
    "friend" TEXT DEFAULT '{}',
    "artist" TEXT DEFAULT '{}',
    "track" TEXT DEFAULT '{}',
    PRIMARY KEY("user_id")
);

CREATE TABLE IF NOT EXISTS "warn" (
    "guild_id" INTEGER,
    "data" TEXT DEFAULT '{}',
    "count" INTEGER DEFAULT 0,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "welcome" (
    "guild_id" INTEGER,
    "channel_id" INTEGER,
    "msg" TEXT DEFAULT 'Hey $user_mention',
    "emdata" TEXT DEFAULT '{}',
    "embed" INTEGER DEFAULT 0,
    "ping" INTEGER DEFAULT 0,
    "autodel" INTEGER DEFAULT 0,
    PRIMARY KEY("guild_id")
);

CREATE TABLE IF NOT EXISTS "wl" (
    "guild_id" INTEGER,
    "BAN" TEXT DEFAULT '[]',
    "BOT" TEXT DEFAULT '[]',
    "KICK" TEXT DEFAULT '[]',
    "ROLE CREATE" TEXT DEFAULT '[]',
    "ROLE DELETE" TEXT DEFAULT '[]',
    "ROLE UPDATE" TEXT DEFAULT '[]',
    "CHANNEL CREATE" TEXT DEFAULT '[]',
    "CHANNEL DELETE" TEXT DEFAULT '[]',
    "CHANNEL UPDATE" TEXT DEFAULT '[]',
    "MEMBER UPDATE" TEXT DEFAULT '[]',
    "GUILD UPDATE" TEXT DEFAULT '[]',
    "WEBHOOK" TEXT DEFAULT '[]',
    "ALL" TEXT DEFAULT '[]',
    PRIMARY KEY("guild_id")
);
"""


def _migrate_user_table(conn: sqlite3.Connection) -> None:
    """
    The original `user` table was created with a stray comma in the SQL:
        "track", TEXT DEFAULT "{}"
    which produced a spurious column literally named TEXT instead of setting
    the type of track to TEXT.  This migration replaces the table with the
    correct schema while preserving all existing data.
    """
    cols = [row[1] for row in conn.execute("PRAGMA table_info(user)").fetchall()]
    if "TEXT" not in cols:
        return

    conn.execute("ALTER TABLE user RENAME TO _user_old")
    conn.execute("""
        CREATE TABLE "user" (
            "user_id"   INTEGER,
            "totaltime" INTEGER DEFAULT 0,
            "server"    TEXT DEFAULT '{}',
            "friend"    TEXT DEFAULT '{}',
            "artist"    TEXT DEFAULT '{}',
            "track"     TEXT DEFAULT '{}',
            PRIMARY KEY("user_id")
        )
    """)
    conn.execute("""
        INSERT INTO user (user_id, totaltime, server, friend, artist, track)
        SELECT user_id, totaltime, server, friend, artist, track
        FROM _user_old
    """)
    conn.execute("DROP TABLE _user_old")
    conn.commit()
    print("[init_db] Migrated user table: removed spurious TEXT column")


def init_db() -> None:
    """
    Create all database.sqlite3 tables if they do not already exist,
    and apply any pending schema migrations.  Safe to call every startup.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(_SCHEMA)
        _migrate_user_table(conn)
        conn.commit()
    print("[init_db] database.sqlite3 initialised / verified OK")
