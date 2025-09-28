"""
This module contains a Caribou migration.

Migration Name: add_rule_text_file_path_columns
Migration Version: 20250927192650
"""


def upgrade(connection):
    ## Adding columns for dialog and choices text option
    ## to store data in file instead

    sql = f"""
            ALTER TABLE rule
            ADD COLUMN use_file INTEGER DEFAULT 0
            CHECK (use_file IN (0, 1));
    """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE rule
            ADD COLUMN file_path TEXT;     
    """

    connection.execute(sql)


def downgrade(connection):
    sql = f"""
            ALTER TABLE rule
            DROP COLUMN use_file; 
        """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE rule
            DROP COLUMN file_path; 
        """
