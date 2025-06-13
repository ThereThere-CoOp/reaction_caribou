"""
This module contains a Caribou migration.

Migration Name: initial_migration
Migration Version: 20250612142722
"""


COMMON_FIELDS = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT UNIQUE,
        label TEXT UNIQUE,
        description TEXT
    """

COMMON_REACTION_ITEM_FIELDS = f"""
        {COMMON_FIELDS},
        scope TEXT,
        parent TEXT
    """

def upgrade(connection):
    
    sql = f"""
        CREATE TABLE fact
        (   
            {COMMON_REACTION_ITEM_FIELDS},
            type TEXT,
            is_enum INTEGER NOT NULL DEFAULT 0,
            trigger_signal_on_modified INTEGER NOT NULL DEFAULT 0,
            have_default_value INTEGER NOT NULL DEFAULT 0,
            default_value TEXT,
            CHECK (is_enum IN (0, 1) AND trigger_signal_on_modified IN (0, 1) AND have_default_value IN (0, 1))
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE rule
        (   
            {COMMON_REACTION_ITEM_FIELDS},
            match_once INTEGER NOT NULL DEFAULT 0,
            priority INTEGER DEFAULT 0,
            CHECK (match_once IN (0, 1))
        ) """
    
    connection.execute(sql)
    
    sql = f"""
        CREATE TABLE tag
        (   
            {COMMON_FIELDS}
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE event
        (   
            {COMMON_REACTION_ITEM_FIELDS}
        ) """
    
    connection.execute(sql)


def downgrade(connection):
    connection.execute('DROP TABLE tag')
    connection.execute('DROP TABLE fact')
    connection.execute('DROP TABLE event')
    connection.execute('DROP TABLE rule')