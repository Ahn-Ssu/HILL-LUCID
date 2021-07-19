import cv2
from utils.createDeviceConnection import *
from utils.imgRead import *
from utils.gravityCentor import *

          

devList = create_devices_with_tries()
len(devList)
myDev = devList[0]

configure_some_nodes(myDev)

while cv2.waitKey(33)<0:
    img = read_imgData(myDev)
    if isinstance(img, list): # numpy is also iterable
        for im in img:
            COG_im = find_centerOfGravity(im)
            cv2.imshow("np to", COG_im)
    else:
        COG_img = find_centerOfGravity(img)
        cv2.imshow("np to", COG_img)
    

destroy_deviceConnection(myDev)


print("Code Run End")