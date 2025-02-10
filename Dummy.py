import pandas as pd
import pypyodbc as odbc
import numpy as np
import json


# Database connection
conn_str1 = 'DRIVER={SQL Server};SERVER=SMS-142M\\SQLEXPRESS;DATABASE=KsDatabase_106_50_delete;Trusted_Connection=yes;'
conn_str2 = 'DRIVER={SQL Server};SERVER=SMS-142M\\SQLEXPRESS;DATABASE=KsDatabase_106_50_new2;Trusted_Connection=yes;'

conn1 = odbc.connect(conn_str1)
conn2 = odbc.connect(conn_str2)

# Query to get all tables
table_query = """
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'
"""



differences = []
detailed_differences={}

try:

    
    tables_database1 = pd.read_sql(table_query, conn1)
    tables_database2 = pd.read_sql(table_query, conn2)
    for table_name in tables_database1['table_name']:
        if table_name.lower() in tables_database2['table_name'].str.lower().values:
            print(f"Comparing table: {table_name}")
            query = f"SELECT * FROM [{table_name}]"
        try:
            df1 = pd.read_sql(query, conn1)
            df2 = pd.read_sql(query, conn2)
            
            # Ensure both dataframes have the same columns
            common_columns = df1.columns.intersection(df2.columns)
            
            df1 = df1[common_columns]
            df2 = df2[common_columns]

            print(f"Printing the shape of the table name {table_name}")    
            print(df1.shape)
            print(df2.shape)

            if (df1.shape != df2.shape):
                differences.append(table_name)
            
            tables_with_SEG_WP_ID = []
            has_seg_id = []                                                                                                                                                     


            for c in differences:
                query = f"SELECT * FROM [{c}]"
                database1= pd.read_sql(query, conn1)
                has_seg_id =  'SEG_ID' in database1.columns
                has_wp_id = 'WP_ID' in database1.columns

                if (has_seg_id or has_wp_id):
                    tables_with_SEG_WP_ID.append(c)
                    

            # comparison = ~ (df1 != df2)
            # print(f"Printing the Comaparison table for the table {table_name}")
            # print(comparison)

            # if comparison.any().any():
            #         differences.append(table_name)
                    
            #         # Get the differing rows and columns
            #         diff_locations = np.where(comparison)
            #         diff_rows = diff_locations[0]
            #         diff_cols = diff_locations[1]
                    
            #         table_differences = []
                    
            #         for row, col in zip(diff_rows, diff_cols):
            #             column_name = df1.columns[col]
            #             value_db1 = df1.iloc[row, col]
            #             value_db2 = df2.iloc[row, col]
                        
            #             table_differences.append({
            #                 "row": int(row),
            #                 "column": column_name,
            #                 "value_db1": str(value_db1),
            #                 "value_db2": str(value_db2)
            #             })
                    
            #         detailed_differences[table_name] = {
            #             "data_differences": table_differences
            #         }

                # Print or process the detailed differences
            # print("\nDetailed differences:")
            # print(json.dumps(detailed_differences, indent=2))

        except Exception as e:
            print(f"An error occurred: {str(e)}")
      
    # with open('database_differences.json', 'w') as f:
    #     json.dump(detailed_differences, f, indent=2)   
    # print(tables_with_SEG_WP_ID)
    
    
    print(differences)
    


    # Comparing the databases for the similarity.. Here there are 3 databases.


finally:
    conn1.close()
    conn2.close()