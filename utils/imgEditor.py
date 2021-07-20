import cv2
import numpy as np

from arena_api import buffer

def find_centerOfGravity(
    srcImg : np.ndarray
    )-> np.ndarray:

    targetImg = srcImg.copy()

    grayScaled = cv2.cvtColor(targetImg, cv2.COLOR_BGR2GRAY) 
    _, binary = cv2.threshold(grayScaled, 150, 255, cv2.THRESH_BINARY_INV)


    # M = cv2.moments(binary)
    # cX = int(M['m10'] / M['m00'])
    # cY = int(M['m01'] / M['m00'])
    
    # cv2.circle(srcImg, (cX, cY), 3, (255, 0, 0), -1)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    for i in contours:
        M = cv2.moments(i)
        if M['m00'] == 0:
            cX = cY = 0
        else :
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        
        cv2.drawMarker(srcImg, (cX, cY), (255, 0, 0), markerType=cv2.MARKER_CROSS,thickness=3)
        # cv2.drawMarker(srcImg, (cX, cY), 3, (255, 0, 0), markerType=cv2.MARKER_TILTED_CROSS)
        cv2.drawContours(srcImg, [i], 0, (0, 0, 255), 2)

    return srcImg

def extract_bufferImg(
    target: buffer._Buffer
    ):

    if isinstance(target, list):

        for idx, unit in enumerate(target):
            data = unit.data
            width = unit.width
            height = unit.height

            np_array = np.asanyarray(data, dtype=np.uint8).reshape(height,width, -1)
            target[idx] = np_array

        return target
        

    data = target.data
    width = target.width
    height = target.height

    np_array = np.asarray(data, dtype=np.uint8)
    np_array = np_array.reshape(height,width,-1) # -1 is the Channel depth
    
    return np_array