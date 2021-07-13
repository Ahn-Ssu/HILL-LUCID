from typing import NoReturn, Optional
import arena_api
from arena_api import enums
from arena_api.buffer import BufferFactory
from arena_api.system import system
import numpy as np

def configure_some_nodes(
    nodemap:arena_api._nodemap.Nodemap,
    stream_nodemap:arena_api._nodemap.Nodemap,
    width:Optional[int] = None,
    heigth:Optional[int] = None,
    pixelFormat:Optional[str] = 'Mono8'
    )->NoReturn:

    # Enable stream auto negotiate packet size
    stream_nodemap['StreamAutoNegotiatePacketSize'].value = True

    # Enable stream packet resend
    stream_nodemap['StreamPacketResendEnable'].value = True

    # Width and height --------------------------------------------------------
    print('Getting \'Width\', \'Height\', and \'PixelFormat\' Nodes')
    nodes = nodemap.get_node(['Width', 'Height', 'PixelFormat'])

    # Set width and height to their max values
    print('Setting \'Width\' and \'Height\' Nodes value to their '
          'values(default:max')
    if width :
        nodes['Width'].value = width
    else:
        nodes['Width'].value = nodes['Width'].max

    if heigth:
        nodes['Height'].value = heigth
    else:
        nodes['Height'].value = nodes['Height'].max

    # Pixel format ------------------------------------------------------------
    new_pixel_format = pixelFormat
    print(f'Setting \'PixelFormat\' to \'{new_pixel_format}\'')
    nodes['PixelFormat'].value = new_pixel_format

def convert_Format(
    buffer:arena_api.buffer._Buffer,
    pixelFormat:arena_api.enums=enums.PixelFormat.BGR8
    )->arena_api.buffer._Buffer:

    print('Converting image buffer pixel format to {}'.format(str(pixelFormat)))
    return BufferFactory.convert(buffer, pixelFormat)
    
def read_img(
    device: arena_api._device.Device
    )->np:
    
    buffer = None
    with device.start_stream(1):
        print(f'Stream started with 1 buffer')

        # 'Device.get_buffer()' with no arguments returns only one buffer
        print('\tGetting one buffer')
        device_buffer = device.get_buffer()

        # Convert to tkinter recognizable pixel format
        buffer = convert_Format(device_buffer)

        # Requeue to release buffer memory
        print('Requeuing device buffer')
        device.requeue_buffer(device_buffer)

    # Create a Numpy array to pass to PIL.Image
    print('Creating 3 dimensional Numpy array')
    data = buffer.data
    width = buffer.width
    height = buffer.height
    
    np_array = np.asarray(data, dtype=np.uint8)
    np_array = np_array.reshape(height,width,-1)
    
    BufferFactory.destroy(buffer)

    return np_array


if __name__ == '__main__' :
    print("Code Test: get img data")
    from createDeviceConnection import *

    devList = create_devices_with_tries()

    myDevice = devList[0]

    configure_some_nodes(nodemap=myDevice.nodemap, stream_nodemap=myDevice.tl_stream_nodemap)
    
    ret = read_img(device= myDevice)
    print(ret.shape)
    print(ret)



    destroy_deviceConnection(devList)