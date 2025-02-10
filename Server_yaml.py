import yaml
import random 
import os
import time 
from serverlogging import logger 
from opcua import Server

# with open("config.yaml" , "r") as file:
#     config =  yaml.safe_load(file)
#     logger.debug("The config file have been loaded safely")
#     print(config)


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


## load the configuration 
config =  load_config()

# Getting the server connection
server = Server()
server.set_endpoint(config["server"]["endpoint"])
namespace =  server.register_namespace(config["server"]["namespace"])
print(f"Namespace index {namespace}")
logger.info(f"NameSpace index: {namespace}")

#Get the objects node
objects = server.get_objects_node()

# Creating the temperture sensor object
tempsens =  objects.add_object(namespace, config["server"]["objects"]["temperature_sensor"]["name"])
logger.info(f"Created object:{tempsens}")

# Add the variables to the object 
for var_name , value  in config['server']["objects"]["temperature_sensor"]["variables"].items():
    var =  tempsens.add_variable(namespace , var_name , value)
    if var_name == "TS1_Temperature" :
        var.set_writable()
        logger.info(f"Added Variable: {var_name} = {value}")


## Creating the light object
bulb =  objects.add_object(namespace , config['server']["objects"]["light_bulb"]["name"])
logger.info(f"Created object:{bulb}")

for var_name , value in config['server']["objects"]["light_bulb"]["variables"].items():
    var = bulb.add_variable(namespace, var_name, value)
    if var_name == "state":
        var.set_writable()
        logger.info(f"Added Variable: {var_name} = {value}")




## Now starting the server
try :
    logger.info("Starting the server")
    if( server.start()):
        logger.debug("Server is online")
    else:
        logger.debug("Server is offline")
        
    while True:
        temp_var =  tempsens.get_children()[-1]
        temperature =  temp_var.get_value() +  random.uniform(-1,1)
        temp_var.set_value(temperature)
        logger.info(f"The current temperature is: {temperature}")

        state_var = bulb.get_children()[0]
        if temperature <20 :
            state_var.set_value(True)
        else:
            state_var.set_value(False)
        
        logger.info(f"Bulb state: {state_var.get_value()} ")

        time.sleep(2)
except Exception as e:
    logger.exception(f" Server Encountered an error {e}")

finally:
    server.stop()
    logger.info("Server is Offline, Please restart the server")

