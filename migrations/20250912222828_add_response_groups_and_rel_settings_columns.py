"""
This module contains a Caribou migration.

Migration Name: add_response_groups_and_rel_settings_columns
Migration Version: 20250912222828
"""


def upgrade(connection):
    sql = f"""
            ALTER TABLE response_group
            -- the method how the group will return the response
            -- by_order: By response order
            -- random: Randomly each time
            -- random_weight: By random using a weight from a function
            ADD COLUMN return_method TEXT DEFAULT 'random'; 
    """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE response_parent_group_rel
            ADD COLUMN execution_order INTEGER; 
    """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE response_parent_group_rel
            ADD COLUMN match_once INTEGER DEFAULT 0
            CHECK (match_once IN (0, 1));
            
    """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE response_parent_group_rel
            ADD COLUMN weight_function TEXT;
            
    """

    connection.execute(sql)


def downgrade(connection):
    sql = f"""
            ALTER TABLE response_group
            DROP COLUMN return_method; 
        """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE response_parent_group_rel
            DROP COLUMN execution_order; 
        """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE response_parent_group_rel
            DROP COLUMN match_once; 
        """

    connection.execute(sql)

    sql = f"""
            ALTER TABLE response_parent_group_rel
            DROP COLUMN weight_function; 
        """

    connection.execute(sql)
