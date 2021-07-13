import time

from arena_api.system import system


def set_default(device=None):

    # Reset to default user set
    print(device.nodemap['UserSetSelector'].value)
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
