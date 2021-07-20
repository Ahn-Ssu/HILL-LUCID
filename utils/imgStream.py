import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.setting import configure_some_nodes
from utils.imgEditor import extract_bufferImg
from utils.deviceConnection import destroy_deviceConnection

import cv2
from typing import Optional
from arena_api import buffer, enums, _device
from arena_api.buffer import BufferFactory
from arena_api.callback import callback, callback_function

def convert_Format(
    buffer:buffer._Buffer,
    format:enums.PixelFormat=enums.PixelFormat.BGR8):

    return BufferFactory.convert(buffer, format)

@callback_function.device.on_buffer
def stream_buffer(
    buffer:buffer._Buffer,
    *args,
    **kwargs
    ):

    converted = convert_Format(buffer)
    arr = extract_bufferImg(converted)

    cv2.imshow("buffer Stream from device", arr)
    cv2.waitKey(1) # nothing

def stream(
    device: _device.Device,
    bufferNumber: Optional[int]=5
    ):

    configure_some_nodes(device)
    handle = callback.register(device, stream_buffer, None)

    device.start_stream(bufferNumber)

    input("\tEnter to exit stream")
    device.stop_stream()
    callback.deregister(handle)
    destroy_deviceConnection(device)

if __name__ == '__main__':
    print('Stream Example start')
    from deviceConnection import create_devices_with_tries

    devList = create_devices_with_tries()
    stream(devList[0])
    destroy_deviceConnection(devList)

    print('Stream Example Done')
    