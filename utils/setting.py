import arena_api
from arena_api import _device, buffer
from arena_api.system import system
from typing import Optional

def set_default(device : arena_api._device.Device):

    if device==None:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the function again.')

    # Reset to default user set
    device.nodemap['UserSetSelector'].value = 'Default'
    device.nodemap['UserSetLoad'].execute()
    print('Device settings has been reset to \'Default\' user set')


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

if __name__ == '__main__':
    print('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
    print('\nExample started\n')

    from createDeviceConnection import create_devices_with_tries, destroy_deviceConnection
    devList = create_devices_with_tries()

    set_default(devList[0])

    destroy_deviceConnection(devList)
    
    print('\nExample finished successfully')