import pypyodbc as odbc
from opcua import Client
import time
from clientlogging import logger 

# Function to initialize the database connection
def initialize_database():
    try:
        conn = odbc.connect(
            "DRIVER={SQL Server};"
            "server=SMS-142M\\SQLEXPRESS;"
            "database=myappication;"
            "Trusted_Connection=yes;"
        )
        logger.info("Connected to database successfully.")
        cursor = conn.cursor()

        check_table_query = """
            IF NOT EXISTS (
                SELECT 1 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'opcua_data'
            )
            BEGIN
                CREATE TABLE opcua_data (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    Display_Name_Temp VARCHAR(255),
                    Display_Name_Bulb VARCHAR(255),
                    value_temp TEXT,
                    value_bulb TEXT,
                    timestamp DATETIME DEFAULT GETDATE()
                )
            END
        """
        cursor.execute(check_table_query)
        conn.commit()
        logger.info("Database table verified or created.")
    except Exception as e:
        logger.exception(f"Database initialization error: {e}")
    return conn

  


# Function to insert data into the database
def insert_into_database(conn, variable_name1, bulb_name ,value_temp, value_bulb):
    cursor = conn.cursor()
    try:
        # Using placeholders for SQL Server
        cursor.execute("""
            INSERT INTO opcua_data (Display_Name_Temp, Display_Name_Bulb, value_temp, value_bulb)
            VALUES (?, ?, ?,?)
        """, (variable_name1, bulb_name, str(value_temp), str(value_bulb)))

        print(f"Data inserted: Display_Name_Temp={variable_name1}, Display_Name_Bulb={bulb_name}, Value Temp={value_temp}, Value Bulb={value_bulb}")
        conn.commit()
        logger.info(f"Data inserted: Temp={value_temp}, Bulb={value_bulb}")

    except Exception as e:
        print(f"Failed to insert data: {e}")
        logger.exception(f"Failed to insert data: {e}")


def main():
    # Initialize the database and get the connection
    conn = initialize_database()

    # OPC UA Client connection
    client = Client("opc.tcp://127.0.0.1:12345")

    try:
        if(client.connect()):
            logger.debug("Client connected to the server.")
            print("Client connected to the server")
        else:
            logger.debug("Server connection is lost")
        

        # Get the objects node
        objects = client.get_objects_node()
        print("The available objects in the node are:", objects)


        bulb  =  objects.get_children()[2]
        tempsens  =  objects.get_children()[1]
        print("The children of the object bulb is: " + str(bulb.get_children()[0].get_browse_name()))

        print("The childrens of the temperature sensor is: "  + str(tempsens.get_children()))
        for i in tempsens.get_children() :
            i.get_value()

        # # Accessing the temperature sensor object
        # temp_sensor = objects.get_child(["2", "TS1"])  
        # temperature_var = temp_sensor.get_child(["2", "TS1_Temperature"])



        # # Accessing the bulb object
        # bulb = objects.get_child(["2", "Light Bulb"])
        # bulb_state_var = bulb.get_child(["0", "State of the bulb"])

        while True:
            # Fetch the temperature value and bulb state
            state =  bulb.get_children()[0]
            # tempsens = tempsens.get_children()[1]
            if len(tempsens.get_children()) > 1:
                tempsens_var = tempsens.get_children()[2]  # Second child (temperature sensor)
            else:
                print("Error: No children found for the temperature sensor object.")
                logger.warning("Temperature sensor variable not found.")
            
            print("The current state of the bulb is " +  str(state.get_value()))
            print("The current temperature is: " + str(tempsens_var.get_value()))
            logger.debug(f"Temperature: {tempsens_var.get_value()}, Bulb State: {state.get_value()}")

            # Insert data into the database
            insert_into_database(conn, "Temperature", "Light Bulb", str(tempsens_var.get_value()),state.get_value())
            

            # print(f"Temperature: {temperature}, Bulb State: {bulb_state}")

            # Sleep for a short interval before the next update
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.exception(f"Client error: {e}")
        

    finally:
        # Close the OPC UA client session
        client.disconnect()
        logger.info("Client session closed.")
        print("Client session closed.")

        # Close the database connection
        conn.close()
        logger.info("Database connection closed.")
        print("Database connection closed.")


if __name__ == "__main__":
    main()
