from opcua import Server
import random
import time 
from lxml import etree


if __name__ =="__main__":

    parser= etree.XMLParser();
    tree = etree.parse("AddressSpace.xml", parser)
    root =  tree.getroot()
    serverNodes1 =[]
    serverNodes2 =[]
    serverToReadAddress = ""
    serverToWriteAddress = ""
    serverReadPassword = ""
    serverWritePassword = ""
    serverReadUser = ""
    serverWriteUser = ""
    serverReadLogin = False
    serverWriteLogin = False
    serverToRead = "TemperatureSensorReadingServer"

    for child in root:
        if(child.get("Type")== serverToRead):
            serverToReadAddress =  child.get("Url")
            serverReadLogin =  child.get("IsAuthentificationRequired").lower = "true"
            serverReadUser = child.get("User")
            serverReadPassword =  child.get("Password")
            serverNodes1  = child

        if(child.get("Type" == "WritingServer")):
            serverToWriteAddress = child.get("Url")
            serverWriteLogin =  child.get("IsAuthenticationRequired").lower = "true"
            serverWriteUser =  child.get("User")
            serverWritePassword = child.get("Password")
            serverNodes2 = child
    

    print("Starting the Server")
    serverRead =  Server()
    serverRead.set_endpoint(serverToReadAddress)
    uri = root.get("Uri")
    idx = serverRead.register_namespace(uri)

    objects = serverRead.get_objects_node()
    print("The objects created is: " + str(objects))

    for item in serverNodes1:
        objName = item.get("Name")
        objPath =  item.get("Path")

        objects.add_object(item.get("Name"),item.get("Path"))


        
        
    

