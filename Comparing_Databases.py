# import pandas as pd
# import pypyodbc as odbc
# import numpy as np

# from sqlalchemy import create_engine

# # Database connection
# conn_str1 = 'DRIVER={SQL Server};SERVER=SMS-142M\\SQLEXPRESS;DATABASE=KsDatabase_106_50_base;Trusted_Connection=yes;'
# conn_str2 = 'DRIVER={SQL Server};SERVER=SMS-142M\\SQLEXPRESS;DATABASE=KsDatabase_106_50_new;Trusted_Connection=yes;'
# conn1 = odbc.connect(conn_str1)
# conn2 = odbc.connect(conn_str2)



# # Query to get all tables
# table_query = """
# SELECT TABLE_NAME
# FROM INFORMATION_SCHEMA.TABLES
# WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'
# """

# differences = []

# try:
#     tables_database1 = pd.read_sql(table_query, conn1)
#     tables_database2 = pd.read_sql(table_query, conn2)
#     print("Tables in Database 2:")
#     print(tables_database2)

#     for table_name in tables_database1['table_name']:
#         if table_name in tables_database2['table_name'].values:
#             query = f"SELECT * FROM [{table_name}]"
#             try:
#                 df1 = pd.read_sql(query, conn1)
#                 df2 = pd.read_sql(query, conn2)
                
#                 # Ensure both dataframes have the same columns
#                 common_columns = df1.columns.intersection(df2.columns)
#                 df1 = df1[common_columns]
#                 df2 = df2[common_columns]
                
#                 if not df1.equals(df2):
#                     diff_mask = ~(df1 == df2)
#                     for col in common_columns:
#                         row_diff = diff_mask[col]
#                         if row_diff.any():
#                             for idx in row_diff[row_diff].index:
#                                 differences.append({
#                                     'Table': table_name,
#                                     'Column': col,
#                                     'Row': idx,
#                                     'DB1 Value': df1.loc[idx, col],
#                                     'DB2 Value': df2.loc[idx, col]
#                                 })
#             except Exception as e:
#                 print(f"Error processing table {table_name}: {e}")
#         else:
#             print(f"Table {table_name} not found in the second database")

#     if differences:
#         result_df = pd.DataFrame(differences)
#         print("\nDifferences found:")
#         print(result_df)
#     else:
#         print("\nNo differences found between the databases.")

# except Exception as e:
#     print(f"Error executing table query: {e}")

# finally:
#     # Close the connections
#     conn1.close()
#     conn2.close()


# import pypyodbc as odbc
# import pandas as pd

# # Database connection details
# server = 'SMS-142M\\SQLEXPRESS'
# database1 = 'KsDatabase_106_50_base'
# database2 = 'KsDatabase_106_50_new'
# conn_str = f'DRIVER={{SQL Server}};SERVER={server};Trusted_Connection=yes;'

# # List of tables to check
# tables_to_check = [
#     'DIMENSIONS_BLADE', 'DIMENSIONS_CAM', 'DIMENSIONS_EXTRUDER',
#     'DIMENSIONS_ROLLER', 'DIMENSIONS_ROTOR', 'DIMENSIONS_TPWORM',
#     'DIMENSIONS_WORM', 'Einfügefehler', 'GENERAL_VERS', 'MachineData_Helix',
#     'MachineData_Helix_Gti', 'MachineData_Helix_Gti2', 'MachineData_Helix_Segment',
#     'MachineData_Helix_Workpiece', 'MACHINEDATA_TAB_NAME', 'MACHINETOOLDATA_TAB_NAME',
#     'MEMOTEXT', 'PERSID_DATA', 'PNC_DATA', 'PROCESS_CAM',
#     'PROCESS_CYCLE_CAM', 'PROCESS_CYCLE_EXTRUDER', 'PROCESS_CYCLE_ROLLER', 'PROCESS_CYCLE_ROTOR',
#     'PROCESS_CYCLE_TPWORM', 'PROCESS_CYCLE_WORM', 'PROCESS_EXTRUDER', 'PROCESS_ROLLER',
#     'PROCESS_ROTOR', 'PROCESS_TPWORM', 'PROCESS_WORM', 'PROFILE',
#     'PROFILE_ACTUAL', 'PROFILE_CORRECTION', 'PROFILE_LAST_CORRECTION', 'PROJECT',
#     'SEGMENT', 'SERVICE_OPTIONEN', 'SETTINGS', 'SETTINGS_CONE_ACTUAL',
#     'SETTINGS_CORRECTION', 'SETTINGS_LAST_CORRECTION', 'SETTINGS_LEAD_ACTUAL', 'TOOL_CUTTERHEADBODY',
#     'TOOL_CUTTERHEADDATA', 'TOOL_DRESSER', 'TOOL_DRESSER_CORRECTION', 'TOOL_DRESSER_LAST_CORRECTION',
#     'TOOL_GRINDINGWHEEL', 'WORK_ROUTINE', 'WORKPIECE'
# ]

# # Connect to the databases
# conn1 = odbc.connect(conn_str + f'DATABASE={database1};')
# conn2 = odbc.connect(conn_str + f'DATABASE={database2};')

# all_differences = [] 

# for table_name in tables_to_check:
#     print(f'Checking table: {table_name}')
    
#     # Query to check for differences
#     diff_query = f"""
#     SELECT COUNT(*) as diff_count
#     FROM (
#         SELECT * FROM {database1}.dbo.{table_name}
#         EXCEPT
#         SELECT * FROM {database2}.dbo.{table_name}
#         UNION ALL
#         SELECT * FROM {database2}.dbo.{table_name}
#         EXCEPT
#         SELECT * FROM {database1}.dbo.{table_name}
#     ) AS Diff
#     """
    
#     # Execute the query
#     cursor = conn1.cursor()
#     cursor.execute(diff_query)
#     row_count = cursor.fetchone()[0]
    
#     if row_count > 0:
#         print(f'Differences found in table: {table_name}')
        
#         # Query to get the differences
#         diff_data_query = f"""
#         SELECT 
#             '{database1}' AS Database1,
#             '{database2}' AS Database2,
#             '{table_name}' AS TableName,
#             'Database1' AS Source,
#             *
#         FROM {database1}.dbo.{table_name}
#         EXCEPT
#         SELECT 
#             '{database1}' AS Database1,
#             '{database2}' AS Database2,
#             '{table_name}' AS TableName,
#             'Database1' AS Source,
#             *
#         FROM {database2}.dbo.{table_name}
#         UNION ALL
#         SELECT 
#             '{database1}' AS Database1,
#             '{database2}' AS Database2,
#             '{table_name}' AS TableName,
#             'Database2' AS Source,
#             *
#         FROM {database2}.dbo.{table_name}
#         EXCEPT
#         SELECT 
#             '{database1}' AS Database1,
#             '{database2}' AS Database2,
#             '{table_name}' AS TableName,
#             'Database2' AS Source,
#             *
#         FROM {database1}.dbo.{table_name}
#         """
        
#         # Execute and display the differences
#         df = pd.read_sql(diff_data_query, conn1)
#         all_differences.append(df)
       
        
#     else:
#         print(f'No differences found in table: {table_name}')

# # Close the connections
# conn1.close()
# conn2.close()


# final_df = pd.concat(all_differences, ignore_index=True)
# final_df.to_csv('diff.csv')

import pandas as pd
import pypyodbc as odbc
import numpy as np
import json


# Database connection
conn_str1 = 'DRIVER={SQL Server};SERVER=SMS-142M\\SQLEXPRESS;DATABASE=KsDatabase_106_50_base;Trusted_Connection=yes;'
conn_str2 = 'DRIVER={SQL Server};SERVER=SMS-142M\\SQLEXPRESS;DATABASE=KsDatabase_106_50_delete;Trusted_Connection=yes;'
conn1 = odbc.connect(conn_str1)
conn2 = odbc.connect(conn_str2)

# Query to get all tables
table_query = """
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'
"""

differences = []

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

                # Compare dataframes
                comparison = (df1 != df2) 
                
                if comparison.any().any():
                    # Get indices where differences occur
                    diff_indices = comparison.any(axis=1)
                    
                    # Create a dictionary to store differences
                    table_differences = {
                        'table_name': table_name,
                        'differences': []
                    }
                    
                    for idx in diff_indices[diff_indices].index:
                        row_diff = {
                            'row_index': int(idx),
                            'differences': {}
                        }
                        for col in common_columns:
                            if comparison.loc[idx, col]:
                                row_diff['differences'][col] = {
                                    'db1_value': str(df1.loc[idx, col]),
                                    'db2_value': str(df2.loc[idx, col])
                                }
                        table_differences['differences'].append(row_diff)
                    
                    differences.append(table_differences)
                    print(f"Found differences in table: {table_name}")
                else:
                    print(f"No differences found in table: {table_name}")

            except Exception as e:
                print(f"Error comparing table {table_name}: {str(e)}")

    # Save differences to a JSON file
    with open('database_differences.json', 'w') as f:
        json.dump(differences, f, indent=2)

    print("Comparison complete. Differences saved to 'database_differences.json'")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    conn1.close()
    conn2.close()
                # print(comparison)
                
    #             # Reset index to avoid issues with different indexes
    #             df1 = df1.reset_index(drop=True)
    #             df2 = df2.reset_index(drop=True)
                
    #             # Compare dataframes
    #             diff_mask = ~ (df1 == df2)
    #             for col in common_columns:
    #                 row_diff = diff_mask[col]
    #                 if row_diff.any():
    #                     for idx in row_diff[row_diff].index:
    #                         differences.append({
    #                             'Table': table_name,
    #                             'Column': col,
    #                             'Row': idx,
    #                             'DB1 Value': df1.loc[idx, col],
    #                             'DB2 Value': df2.loc[idx, col]
    #                         })
                
    #             if len(differences) > 0:
    #                 print(f"Differences found in table: {table_name}")
    #             else:
    #                 print(f"No differences found in table: {table_name}")
                    
    #         except Exception as e:
    #             print(f"Error processing table {table_name}: {str(e)}")
    #     else:
    #         print(f"Table {table_name} not found in the second database")

    # if differences:
    #     result_df = pd.DataFrame(differences)
    #     print("\nDifferences found:")
    #     print(result_df)
        
    #     # Optionally, save to CSV
    #     result_df.to_csv('database_differences.csv', index=False)
    #     print("Differences saved to 'database_differences.csv'")
    # else:
    #     print("\nNo differences found between the databases.")

#             except Exception as e:
#                 print(f"Error executing table query: {str(e)}")

# finally:
#     # Close the connections
#     conn1.close()
#     conn2.close()
