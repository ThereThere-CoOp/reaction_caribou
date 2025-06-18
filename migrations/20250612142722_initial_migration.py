"""
This module contains a Caribou migration.

Migration Name: initial_migration
Migration Version: 20250612142722
"""

import os
import sys


sys.path.append(os.path.abspath("."))

def upgrade(connection):

    import utils

    sql = f"""
        CREATE TABLE tag
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS}
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE database_uuid
        (   
            uuid TEXT
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE fact
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS},
            type INTEGER,
            hint_string TEXT,
            is_enum INTEGER NOT NULL DEFAULT 0,
            trigger_signal_on_modified INTEGER NOT NULL DEFAULT 0,
            have_default_value INTEGER NOT NULL DEFAULT 0,
            default_value TEXT,
            CHECK (is_enum IN (0, 1) AND trigger_signal_on_modified IN (0, 1) AND have_default_value IN (0, 1))
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE event
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS}
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE response_group
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS}
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE response
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS},
            triggers TEXT,

            -- response dialog fields
            have_choices INTEGER NOT NULL DEFAULT 0,

            CHECK (have_choices IN (0, 1))
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE response_parent_group_rel
        (   
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_group_id INTEGER NOT NULL,
            response_group_id INTEGER,
            response_id, INTEGER,

            FOREIGN KEY (parent_group_id) REFERENCES response_group(id) ON DELETE CASCADE,
            FOREIGN KEY (response_group_id) REFERENCES response_group(id) ON DELETE CASCADE,
            FOREIGN KEY (response_id) REFERENCES response(id) ON DELETE CASCADE,

            UNIQUE (parent_group_id, response_group_id),
            UNIQUE (parent_group_id, response_id),

            CHECK(parent_group_id != response_group_id)
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE rule
        (   
            {utils.COMMON_FIELDS_RULE},
            event_id INTEGER,
            response_group_id INTEGER,

            -- choice and dialog text fields
            response_id INTEGER,
            text TEXT, -- this is json field
            triggers TEXT,

            FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
            FOREIGN KEY (response_group_id) REFERENCES response_group(id) ON DELETE CASCADE,

            FOREIGN KEY (response_id) REFERENCES response(id) ON DELETE CASCADE,
            {utils.COMMON_CHECKS_RULE}
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE criteria
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS},
            rule_id INTEGER NOT NULL,
            operation TEXT,
            fact_id INTEGER,
            value_a TEXT,
            value_b TEXT,
            is_reverse INTEGER NOT NULL DEFAULT 0,
            is_operation INTEGER NOT NULL DEFAULT 0,

            CHECK (is_reverse IN (0, 1) AND is_operation IN (0, 1)),
            FOREIGN KEY (fact_id) REFERENCES fact(id) ON DELETE SET NULL,
            FOREIGN KEY (rule_id) REFERENCES rule(id) ON DELETE CASCADE
        ) """
    
    connection.execute(sql)


    sql = f"""
        CREATE TABLE modification
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS},
            rule_id INTEGER NOT NULL,
            fact_id INTEGER,
            modification_value TEXT,
            operation TEXT,
            FOREIGN KEY (fact_id) REFERENCES fact(id) ON DELETE SET NULL,
            FOREIGN KEY (rule_id) REFERENCES rule(id) ON DELETE CASCADE
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE tag_item_rel
        (   
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id INTEGER NOT NULL,
            response_group_id INTEGER,
            response_id INTEGER,
            fact_id INTEGER,
            event_id INTEGER,

            FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE,
            FOREIGN KEY (response_group_id) REFERENCES response_group(id) ON DELETE CASCADE,
            FOREIGN KEY (response_id) REFERENCES response(id) ON DELETE CASCADE,
            FOREIGN KEY (fact_id) REFERENCES fact(id) ON DELETE CASCADE,
            FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
            UNIQUE (tag_id, response_group_id),
            UNIQUE (tag_id, response_id),
            UNIQUE (tag_id, fact_id),
            UNIQUE (tag_id, event_id)
        ) """
    
    connection.execute(sql)



def downgrade(connection):
    connection.execute('DROP TABLE tag_item_rel')
    connection.execute('DROP TABLE response_parent_group_rel')
    connection.execute('DROP TABLE criteria')
    connection.execute('DROP TABLE modification')
    connection.execute('DROP TABLE rule')
    connection.execute('DROP TABLE event')
    connection.execute('DROP TABLE response')
    connection.execute('DROP TABLE response_group')
    connection.execute('DROP TABLE fact')
    connection.execute('DROP TABLE tag')
    connection.execute('DROP TABLE database_uuid')