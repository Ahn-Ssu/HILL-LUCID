import time
import arena_api

from arena_api.system import system


def create_devices_with_tries():
    """
    This function waits for the user to connect a device before raising
    an exception
    """

    tries = 0
    tries_max = 6
    sleep_time_secs = 10
    # Wait for device for sleepTime*tries_max seconds
    while tries < tries_max:  
        devices = system.create_device()
        if not devices:
            print(
                f'Try {tries+1} of {tries_max}: waiting for {sleep_time_secs} '
                f'secs for a device to be connected!')
            for sec_count in range(sleep_time_secs):
                time.sleep(1)
                print(f'{sec_count + 1 } seconds passed ',
                      '∎' * sec_count, end='\r')
            tries += 1
        else:
            print(f'Created {len(devices)} device(s)')
            return devices
    else:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the example again.')


def destroy_deviceConnection(device=None):
    # for arena_api Device instance
    if isinstance(device, arena_api._device.Device) : # device in list
        system.destroy_device(device)
    # for arena_api Device instance in list (from create_device API)
    elif isinstance(device, list):
        for dev in device:
            if isinstance(dev, arena_api._device.Device):
                system.destroy_device(dev)
    else:
        raise Exception(f'No device found! Please assign a device and run '
                        f'the function again.')
    
    print(f"destroyed the device. We've recovered the resources.")


if __name__ == '__main__':
    # destroy_deviceConnection() # empty test
    deviceList = create_devices_with_tries()
    print("system.device_infos ===> {}".format(system.device_infos))
    #property
    for idx, device in enumerate(deviceList):
        print("{}: DEFAULT_NUM_BUFFERS {}".format(idx, device.DEFAULT_NUM_BUFFERS))
        print("{}: GET_BUFFER_TIMEOUT_MILLISEC {}".format(idx, device.GET_BUFFER_TIMEOUT_MILLISEC))
        print("{}: WAIT_ON_EVENT_TIMEOUT_MILLISEC {}".format(idx, device.WAIT_ON_EVENT_TIMEOUT_MILLISEC))
        print(device.nodemap)
        print(list(device.nodemap))
        # print("{}: nodemap {}".format(idx, len(device.nodemap)))
        # print("{}: tl_device_nodemap list length {}".format(idx, len(device.tl_device_nodemap)))
        # print("{}: tl_interface_nodemap list length{}".format(idx, len(device.tl_interface_nodemap)))
        # print("{}: tl_stream_nodemap list length{}".format(idx, len(device.tl_stream_nodemap)))
    # system.tl_system_nodemap
    # system.tl_interface_nodemap
    # device.tl_device_nodemap
    # device.tl_stream_nodemap
    # device.tl_interface_nodemap
    destroy_deviceConnection(deviceList)
    print("Code Test: Create and Destroy clear")