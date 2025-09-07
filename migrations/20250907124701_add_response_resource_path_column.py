"""
This module contains a Caribou migration.

Migration Name: add_response_resource_path_column
Migration Version: 20250907124701
"""

def upgrade(connection):
    sql = f"""
            ALTER TABLE response
            ADD COLUMN resource TEXT; 
        """
    
    connection.execute(sql)


def downgrade(connection):
    sql = f"""
            ALTER TABLE response
            DROP COLUMN resource; 
        """
    
    connection.execute(sql)
