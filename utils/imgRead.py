from typing import Optional, Union, Iterable
import arena_api._device
from arena_api import enums, buffer, _device
from arena_api.buffer import BufferFactory
import numpy as np

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
    buffers:Union[Iterable[buffer._Buffer],buffer._Buffer],
    pixelFormat:enums=enums.PixelFormat.BGR8
    )->buffer._Buffer:

    print('Converting image buffer pixel format to {}'.format(str(pixelFormat)))
    if isinstance(buffers, Iterable):
        for buffer in buffers:
           BufferFactory.convert(buffer, pixelFormat)
    else:
        BufferFactory.convert(buffers, pixelFormat) 
    return buffers
    
def read_imgData(
    device: _device.Device,
    bufferNumber : Optional[int]=1
    )->np.ndarray:
    
    buffer = None
    bufferNumber = 30
    with device.start_stream(bufferNumber):
        print('Stream started with {} buffer'.format(bufferNumber))

        # 'Device.get_buffer()' with no arguments returns only one buffer
        print('\tGetting {} buffer'.format(bufferNumber))
        device_buffer = device.get_buffer(bufferNumber)

        # Convert to tkinter recognizable pixel format
        buffer = convert_Format(device_buffer)

        # Requeue to release buffer memory
        print('Requeuing device buffer')
        device.requeue_buffer(device_buffer)

    # Create a Numpy array to pass to PIL.Image
    print('Creating 3 dimensional Numpy array')
    
    np_array = reshape_data(target= buffer)
    
    BufferFactory.destroy(buffer)

    return np_array

def reshape_data(
    target: Union[buffer._Buffer, list[buffer._Buffer]]
    ):
    
    if isinstance(target, buffer._Buffer):
        data = buffer.data
        width = buffer.width
        height = buffer.height

        arr = np.asarray(data, dtype=np.uint8)
        arr = arr.reshape(height, width, -1)

        BufferFactory.destroy(target)

        return arr


if __name__ == '__main__' :
    print("Code Test: get img data")
    from createDeviceConnection import *

    devList = create_devices_with_tries()

    myDevice = devList[0]

    configure_some_nodes(nodemap=myDevice.nodemap, stream_nodemap=myDevice.tl_stream_nodemap)
    
    ret = read_imgData(device= myDevice)
    print(ret.shape)
    print(ret)



    destroy_deviceConnection(devList)
    print("Test Done: get img data ")