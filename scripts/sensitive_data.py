# sensitive_data.py
# Anything that might be considered sensitive data - to be protected from distributing.

def get_sql_query(transformed_path):
    # Prepare the SQL commands using the transformed path
    sql_update_1 = f"UPDATE iparam SET svalue = '{transformed_path}' \n WHERE stype IN ('SREPORTPATH','SREPORTTEMPPATH','SATTACHMENTPATH','SATTACHMENTTEMPPATH','SFILTERSPATH');"
    sql_update_2 = f"UPDATE param SET sdefpath = '{transformed_path}';"
    
    # Define useful selects and SQL queries
    useful_selects = f"""
    /* -- Search for all objects in the system
    SELECT * FROM sys.objects;

    -- Search for a table by name
    SELECT * FROM sys.tables WHERE name LIKE '%<table_name>%';

    -- Search for tables with a specific column name
    SELECT t.name AS TableName, c.name AS ColumnName
    FROM sys.tables t
    JOIN sys.columns c ON t.object_id = c.object_id
    WHERE c.name LIKE '%<column_name>%';
    */

    /* The paths have been prepared for your discretion */
    {sql_update_1}
    {sql_update_2}

    /* Enjoy your Flight! */
    """
    return useful_selects
