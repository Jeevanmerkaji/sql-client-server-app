import yaml
import pypyodbc as odbc
from opcua import Client
import time 
from serverlogging import logger

# Loading the configurations from the config file 

def load_config(config_file = "config.yaml"):
    try:
        with open(config_file, "r") as file :
            config = yaml.safe_load_all(file)

            config_dict ={}

            for doc in config:
                if "server" in doc:
                    config_dict["server"] =  doc['server']
                if "client" in doc:
                    config_dict["client"] =  doc['client']

                if "database" in doc:
                    config_dict["database"] = doc["database"]
        logger.info("The Configuration is loaded successfully")

        return config_dict    
    except Exception as e:
        logger.exception(f"Failed to load the configuration: {e}")
        raise


## Intializing the database connection 
def intialize_database(config):
    # conn = None
    try:
        connection_string = (
            f"DRIVER={config['database']['driver']};"
            f"server={config['database']['server']};"
            f"database={config['database']['database']};"
            f"Trusted_Connection={config['database']['trusted_connection']};"
        )

        logger.debug(f"Connected to the database successfully{connection_string}")
        conn = odbc.connect(connection_string)
        logger.info("Connected to the database successfully")
        cursor =  conn.cursor()

        check_table_query = """
            IF NOT EXISTS(
                SELECT 1
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME ='opcua_data'
            )
            BEGIN
                CREATE TABLE opcua_data(
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    Display_Name_Temp VARCHAR(255),
                    Display_Name_BUlb VARCHAR(255),
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
        logger.exception(f"Database Initilization error {e}")
    
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

    # load the configuration
    config = load_config()

    # Initialize the database and get the connection
    conn = intialize_database(config = config)

    # Opcua client connection
    client = Client(config["client"]["endpoint"])

    try:
        if(client.connect()):
            logger.debug("Client connected to the server")

        else:
            logger.debug("Server connection is lost")

        objects =  client.get_objects_node()
        print("The available objects in the node are" , objects)

        ## Access the bulb and temperature based on the loaded config
        bulb = objects.get_child([config["client"]["objects"]['light_bulb']['node_id']])
        tempsens =  objects.get_child([config['client']['objects']['temperature_sensor']['node_id']])

        print(f"The childs present in the bulb object are {bulb.get_children()[0].get_browse_name()}")
        print(f"The childrens present in the temperature object are {tempsens.get_children()}")


        ## Inserting the data into the database
        while True:
            
            #Fetch the bulb state and the temperature sensor value from the server 
            bulb_state =  bulb.get_child([config['client']['objects']['light_bulb']['state_variable']]).get_value()
            temp_value =  tempsens.get_child([config['client']['objects']['temperature_sensor']['temperature_variable']]).get_value()

            print(f"Bulb state:{bulb_state} , Temperature:{temp_value}")
            logger.debug(f"Bulb State: {bulb_state}, Temperature:{temp_value}")

            #Now insert the data into the database
            insert_into_database(conn, "Temperature" , "Light_bulb" , str(temp_value), str(bulb_state) )


            time.sleep(config['client']['connection_timeout'])

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.exception(f"Client error {e}")

    finally:
        client.disconnect()
        logger.info("Client session is closed")
        print("Client session closed")

        # come out from the database by releasing the connection string
        conn.close()
        logger.info("Database connection closed")
        print("Database connection is closed")

if __name__== "__main__":
    main()        


