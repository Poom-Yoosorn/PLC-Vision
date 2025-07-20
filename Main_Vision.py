import cv2
from opcua import Client

objects = None
proximityVar = "BottleDetected"
ejectVar = "EjectBottle"
exitVar = "exitScript"
sessionVar = "sessionNumber"

plcVarPath = ["0:Objects",
              "2:DeviceSet",
              "4:CODESYS Control Win V3 x64",
              "3:Resources",
              "4:Application",
              "3:Programs",
              "4:POU_Main",
              "var"]
img_raw = None
imageName = "bottle_label.jpg"
#imageName = "bottle.jpg"

lastSession = 0

def connectOPCUA():
    global objects
    client = Client("opc.tcp://LAPTOP-S2HU8GI9:4840")
    client.connect()
    print("OPC UA Client is connected to Server")

    objects = client.get_root_node()

def checkSensor():
    global objects,BottleDetected_mem
    plcVarPath[len(plcVarPath)-1] = str("4:") + str(proximityVar)
    var_path = objects.get_child(plcVarPath)
    
    BottleDetected = var_path.get_value()
    #print("Proximity Sensor Check : " + str(value))
    
    return BottleDetected
        

def activateEject():
    global objects
    plcVarPath[len(plcVarPath)-1] = str("4:") + str(ejectVar)
    var_path = objects.get_child(plcVarPath)
    
    var_type = var_path.get_data_type_as_variant_type()
    value = var_path.set_value(True,var_type)
    print("Ejection Actuator is Activated")
    
def exitScript():
    global objects
    plcVarPath[len(plcVarPath)-1] = str("4:") + str(exitVar)
    var_path = objects.get_child(plcVarPath)
    
    value = var_path.get_value()
    if value:
        print("Script Closed")
    
    return value

def grabFrame():
    global img_raw
    pic_directory = "imageBottle//" + imageName
    img_raw = cv2.imread(pic_directory, cv2.IMREAD_GRAYSCALE)

def checkLabel(img_fillter,img_raw):
    contours, hier = cv2.findContours(img_fillter, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        ep = 0.1*cv2.arcLength(cnt, True)
        ap = cv2.approxPolyDP(cnt, ep, True)
        
        area = cv2.contourArea(cnt)
        if (len(ap)==4 and area<25000 and area>142):
            cv2.drawContours(img_raw, cnt,-1,(0,255,0),2)
            print("No Issue.Label Is Detected")
            return 1
        
    print("No Label Detected")
    return 0



def classifyCameraImage():
    global img_raw
    
    img_fillter = cv2.adaptiveThreshold(img_raw, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
    cv2.imwrite("imageBottle//bottle-binary.jpg", img_fillter)
    
    return checkLabel(img_fillter,img_raw)

    
def getSessionNumber():
    global objects
    plcVarPath[len(plcVarPath)-1] = str("4:") + str(sessionVar)
    var_path = objects.get_child(plcVarPath)
    
    value = var_path.get_value()
    return value    

if __name__ == '__main__':
    
    connectOPCUA()
    
    while(1):
        if exitScript():
            break
        else:
           if checkSensor() and lastSession != getSessionNumber():                              
               lastSession = getSessionNumber() 
                   
                   
               grabFrame()
               if not classifyCameraImage():
                   activateEject()





