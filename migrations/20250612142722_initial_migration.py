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
            {utils.COMMON_FIELDS}
        ) """
    
    connection.execute(sql)

    sql = f"""
        CREATE TABLE fact
        (   
            {utils.COMMON_REACTION_ITEM_FIELDS},
            type TEXT,
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
        CREATE TABLE rule
        (   
            {utils.COMMON_FIELDS_RULE},
            {utils.COMMON_CHECKS_RULE}
        ) """
    
    connection.execute(sql)


def downgrade(connection):
    connection.execute('DROP TABLE tag')
    connection.execute('DROP TABLE fact')
    connection.execute('DROP TABLE event')
    connection.execute('DROP TABLE rule')