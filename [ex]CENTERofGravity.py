import cv2
import numpy as np

def find_centerOfGravity(
    srcImg : np
    )-> np:

    targetImg = srcImg.copy()

    grayScaled = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY) 
    _, binary = cv2.threshold(grayScaled, 150, 255, cv2.THRESH_BINARY_INV)


    M = cv2.moments(binary)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    
    cv2.circle(srcImg, (cX, cY), 3, (255, 0, 0), -1)

    return srcImg



import cv2
from utils.createDeviceConnection import *
from utils.imgRead import *



devList = create_devices_with_tries()
myDev = devList[0]

configure_some_nodes(myDev)

while cv2.waitKey(33)<0:
    img = read_imgData(myDev)
    COG = find_centerOfGravity(img)
    cv2.imshow("np to", COG)
    

destroy_deviceConnection(myDev)