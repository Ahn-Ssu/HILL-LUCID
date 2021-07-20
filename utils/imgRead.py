import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import numpy as np
from typing import Union, Optional
from arena_api import enums, _device, buffer
from arena_api.buffer import BufferFactory

from setting import *
from imgEditor import *



def check_buffer_list_input(buffers_list:list):

        if len(buffers_list) == 0:
            raise ValueError(
                'requeue_buffer argument can not be an empty list')

        for buf in buffers_list:
            is_instance = isinstance(buf, buffer._Buffer)
            if not is_instance:
                raise TypeError('argument list has element(s) that is not '
                                'of Buffer type')

def convert_Format(
    buffer:Union[buffer._Buffer,list],
    pixelFormat:enums=enums.PixelFormat.BGR8
    )->Union[buffer._Buffer,list]:

    print(f'Converting image buffer pixel format to {str(pixelFormat)}')
    if isinstance(buffer, list):
        check_buffer_list_input(buffer)
        print(f'buffer list length ={len(buffer)}')
        buffers = []
        for unit in (buffer):
           buffers.append(BufferFactory.convert(unit, pixelFormat))
        return buffers
    
    print('convert single buffer')
    return BufferFactory.convert(buffer, pixelFormat)
    
def read_imgData(
    device: _device.Device,
    bufferNumber: Optional[int]=1
    )->np.ndarray:
    
    buffer = None
    with device.start_stream(bufferNumber):
        print(f'Stream started with 1 buffer')

        # 'Device.get_buffer()' with no arguments returns only one buffer
        print('\tGetting one buffer')
        device_buffer = device.get_buffer(bufferNumber)

        # Convert to tkinter recognizable pixel format
        buffer = convert_Format(device_buffer)
        # Requeue to release buffer memory
        print('Requeuing device buffer')
        device.requeue_buffer(device_buffer)

    # Create a Numpy array to pass to PIL.Image
    print('Creating 3 dimensional Numpy array')
    
    # BufferFactory.destroy(buffer)
    np_array = extract_bufferImg(buffer)
    BufferFactory.destroy(buffer)

    return np_array
    

if __name__ == '__main__' :
    print("Code Test: get img data")
    from deviceConnection import *
    from pprint import pprint

    devList = create_devices_with_tries()

    myDevice = devList[0]

    configure_some_nodes(myDevice)
    
    ret = read_imgData(device= myDevice)
    print(f'Img Data Shape == {ret.shape}')
    pprint(ret,indent=2)

    cv2.imshow("Single Shot(Buffer) Img Test", ret)

    destroy_deviceConnection(devList)
    print("Test Done: get img data ")