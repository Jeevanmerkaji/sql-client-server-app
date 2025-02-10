## Here Creating the client code that will connect to the server which is created and read and write the values 

from opcua import Client

# Establishing a connection to the server using the address
client = Client("opc.tcp://127.0.0.1:12345")
client.connect()

# Printing all the namespaces that are available in the server 
namespaces_available =  client.get_namespace_array()
print("Printing all the namespaces that are available in the array" + str(namespaces_available))

# Getting all the objects that are available in the node 
objects =  client.get_objects_node()
print("The available objects in the node are" + str(objects))

# Getting all the childrens that are created in the particular objects 
childrens = objects.get_children()
print("The available childrens in the objects are"  +  str(childrens))

#now getting the main childrens that are the objects from the object
bulb  =  objects.get_children()[2]
tempsens  =  objects.get_children()[1]

# Now we can get the childrens or the varibles that are stored inside these main objects
print("The children of the object bulb is: " + str(bulb.get_children()[0].get_browse_name()))

# to obtain the current state of the bulb
state =  bulb.get_children()[0]
print("The current state of the bulb is" +  str(state.get_value()))

#  Now changing the value of the bulb to TRUE
state.set_value(False)

print("The current state of the bulb after resetting is: " +  str(state.get_value()))


# Diretcly getting the node from the clinet
# temp  = client.get_node('ns=2 ; s ="TS1_Temperature"') ==> this will directly get the current variable
# Now getting the childrens of the temperature sensor 
print("The childrens of the temperature sensor is: "  + str(tempsens.get_children()))
for i in tempsens.get_children() :
    i.get_value()


client.close_session()






