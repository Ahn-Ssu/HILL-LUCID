import cv2
from utils.createDeviceConnection import *
from utils.imgRead import *
from utils.gravityCentor import *



devList = create_devices_with_tries()
myDev = devList[0]

configure_some_nodes(myDev)

while cv2.waitKey(33)<0:
    img = read_imgData(myDev)
    COG_img = find_centerOfGravity(img)
    cv2.imshow("np to", COG_img)
    

destroy_deviceConnection(myDev)