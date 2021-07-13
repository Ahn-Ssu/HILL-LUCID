import cv2
from utils.createDeviceConnection import *
from utils.imgRead import *



devList = create_devices_with_tries()
myDev = devList[0]

configure_some_nodes(myDev)

while cv2.waitKey(33)<0:
    img = read_imgData(myDev)
    cv2.imshow("np to", img)
    

destroy_deviceConnection(myDev)