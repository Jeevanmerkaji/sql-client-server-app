from opcua import Server
import random
import time
from serverlogging import logger


server = Server()
server.set_endpoint("opc.tcp://127.0.0.1:12345")
server.register_namespace("Room1")
logger.info("OPC UA Server initialized with endpoint opc.tcp://127.0.0.1:12345")


# Get the objects from the node
objects = server.get_objects_node()
print(" The objects created is : " + str(objects))
logger.info("Temperature Sensor 1 object added.")

# Now add the objects
tempsens =  objects.add_object('ns=2 ; s="TS1"' , "Temperature Sensor 1")
print("The first object which is added to the node is " + str(tempsens))

#Now add the variable to the object that is created  
tempsens.add_variable('ns=2 ; s= "TS1_VendorName" ', "TS1 Vendor Name" , "Sensor king")
print("The First added variable is " + str(tempsens))

# Now adding the second variable 
tempsens.add_variable('ns=2 ; s= "TS1_SerialNumber" ', "TS1 Serial Number" , 124563)
print("The Second added variable is " + str(tempsens))

# Now adding the third variable 
temp  =  tempsens.add_variable('ns=2 ; s= "TS1_Temperature" ', "TS1 Temperatrue" ,20)
print("The Third added variable is " + str(tempsens))
logger.info("Temperature variables added and writable.")

# Now Creating the 2nd object 
bulb =  objects.add_object(2 , "Light Bulb")
print("The second object which is added to the node is " + str(bulb))

# Now adding the first variable to the 2nd object 
state =  bulb.add_variable(2 , "State of the bulb" , True)
print("The First added variable to the 2nd object is " + str(state))

# Set the particular variable as writable to allow the client to make changes
state.set_writable()
logger.info("Light Bulb object and state variable added.")

#Setting the initial value of the temperature
temperature = 20.0

# now starting the loop to start the server
try: 
    logger.info("Starting OPC UA Server...")
    print("Start the server")
    if (server.start()):
        logger.debug("Server is online.")
    else:
        logger.debug("Server is offline.")

    
    while True:
        temperature += random.uniform(-1,1)
        temp.set_value(temperature)
        print("New Temperature: " +str(temp.get_value()))
        logger.debug(f"Updated temperature: {temperature}")
        if temperature < 20:
            state.set_value(True)  # Turn the bulb ON
            print("State of the light bulb is " + str(state.get_value()))
            logger.debug("Light bulb turned ON.")
        else:
            state.set_value(False)  # Turn the bulb OFF
            print("State of the light bulb is " + str(state.get_value()))
            logger.debug("Light bulb turned OFF.")

        time.sleep(2)   
except Exception as e:
     logger.exception(f"Server encountered an error: {e}")
finally:
    server.stop()
    print("Server is Offline")
    logger.info("Server is offline.")

  