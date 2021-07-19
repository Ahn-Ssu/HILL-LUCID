from typing import Union, Optional
from arena_api import enums, _device, buffer
from arena_api.buffer import BufferFactory
import numpy as np
import arena_api
from numpy.random.mtrand import f

def configure_some_nodes(
    device:_device.Device,
    width:Optional[int] = None,
    heigth:Optional[int] = None,
    pixelFormat:Optional[str] = 'Mono8'
    ):

    nodemap=device.nodemap
    stream_nodemap=device.tl_stream_nodemap

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
    buffer:Union[buffer._Buffer,list],
    pixelFormat:enums=enums.PixelFormat.BGR8
    )->Union[buffer._Buffer,list]:

    print('Converting image buffer pixel format to {}'.format(str(pixelFormat)))
    if isinstance(buffer, list):
        print(f'buffer list length ={len(buffer)}')
        for idx, unit in enumerate(buffer):
           buffer[idx] = BufferFactory.convert(unit, pixelFormat) 
        return buffer
    
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
    np_array = extractReshape(buffer)

    return np_array

def extractReshape(
    target: buffer._Buffer
    ):
    data = target.data
    width = target.width
    height = target.height

    np_array = np.asarray(data, dtype=np.uint8)
    np_array = np_array.reshape(height,width,-1) # -1 is the Channel depth
    
    BufferFactory.destroy(target)

    return np_array
    


if __name__ == '__main__' :
    print("Code Test: get img data")
    from createDeviceConnection import *

    devList = create_devices_with_tries()

    myDevice = devList[0]

    configure_some_nodes(myDevice)
    
    ret = read_imgData(device= myDevice)
    print(ret.shape)
    print(ret)



    destroy_deviceConnection(devList)
    print("Test Done: get img data ")