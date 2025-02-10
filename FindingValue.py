import pandas as pd
import pypyodbc as odbc

# Database connection
conn_str = 'DRIVER={SQL Server};SERVER=SMS-142M\\SQLEXPRESS;DATABASE=KsDataBase_Old;Trusted_Connection=yes;'
conn = odbc.connect(conn_str)

# Define the search value
search_value = 2295

# Query to get all tables with the SEG_ID column
table_query = """
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE COLUMN_NAME = 'SEG_ID' AND TABLE_SCHEMA = 'dbo';
"""

# Try executing the query and handle errors
try:
    tables_with_seg_id = pd.read_sql(table_query, conn)
    print(tables_with_seg_id)
    if tables_with_seg_id.empty:
        print("No tables with the column 'SEG_ID' were found in the database.")
    else:
        # Loop through tables to check for the search value
        for table_name in tables_with_seg_id['table_name']:
            print(f"Checking table: {table_name}")
            # Query to search for the value in the SEG_ID column
            query = f"SELECT * FROM [dbo].[{table_name}] WHERE SEG_ID = {search_value}"
            try:
                result = pd.read_sql(query, conn)
                if not result.empty:
                    print(f"Value {search_value} found in table {table_name}:")
                    print(result)
                else:
                    print(f"Value {search_value} not found in table {table_name}.")
            except Exception as e:
                print(f"Error querying table {table_name}: {e}")
except Exception as e:
    print(f"Error executing table query: {e}")

# Close the connection
conn.close()
