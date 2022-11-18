import json

def extractCellId(rawstring :str):
    """
    This function return the name of the cell after requesting locationInfo
    """
    cellStr = rawstring.rfind("cell_id")
    return rawstring[cellStr+11:cellStr+20]

def extractLatAndLong(rawstring :str):
    """
    This function return the latitude,longitude after requesting get_coordinates_of_cell()
    """
    #print(rawstring)
    pos1 = rawstring.rfind("latitude")
    pos2 = rawstring.rfind("longitude")
    pos3 = rawstring.rfind("name")
    myString = rawstring[pos1+11:pos2-4] + "," + rawstring[pos2+12:pos3-4]
    myString = myString.replace('\n', '')
    #print(myString)
    return(myString)

def determinCallbacktype(str):
    if(str.rfind("transaction") > -1):
        return("callbacktype = qos")
    else:
        return("callbacktype = unknown")

def extractQosEvent(str):
    pos1 = str.rfind("event") 
    pos2 = str.rfind("accumulatedUsage") 
    return(str[pos1+9:pos2-4])