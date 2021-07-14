import arena_api
from arena_api.system import system
from typing import NoReturn

def set_default(device : arena_api._device.Device):

    if device==None:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the function again.')

    # Reset to default user set
    device.nodemap['UserSetSelector'].value = 'Default'
    device.nodemap['UserSetLoad'].execute()
    print('Device settings has been reset to \'Default\' user set')


if __name__ == '__main__':
    print('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
    print('\nExample started\n')

    from createDeviceConnection import create_devices_with_tries, destroy_deviceConnection
    devList = create_devices_with_tries()

    set_default(devList[0])

    destroy_deviceConnection(devList)
    
    print('\nExample finished successfully')
