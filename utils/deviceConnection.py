import time

from typing import Union, Iterable
from arena_api.system import system
from arena_api import _device

def create_devices_with_tries() -> Iterable[_device.Device]:
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
                      '∎∎∎' * sec_count, end='\r')
            tries += 1
        else:
            print(f'Created {len(devices)} device(s)')
            return devices
    else:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the example again.')

def destroy_deviceConnection(
    device: Union[Iterable[_device.Device],_device.Device]
    ):
    # for arena_api Device instance
    if isinstance(device, _device.Device) : # device in list
        system.destroy_device(device)
    # for arena_api Device instance in list (from create_device API)
    elif isinstance(device, list):
        for dev in device:
            if isinstance(dev, _device.Device):
                system.destroy_device(dev)
    else:
        raise Exception(f'No device found! Please assign a device and run '
                        f'the function again.')
    
    system.destroy_device() # for safety
    print(f"destroyed the device. We've recovered the resources.")

if __name__ == '__main__':
    # destroy_deviceConnection() # empty test
    deviceList = create_devices_with_tries()
    print("system.device_infos ===> {}".format(system.device_infos))
    #property
    for idx, device in enumerate(deviceList):
        print("\t"+"-"*40)
        print("\t {}: DEFAULT_NUM_BUFFERS {}".format(idx, device.DEFAULT_NUM_BUFFERS))
        print("\t {}: GET_BUFFER_TIMEOUT_MILLISEC {}".format(idx, device.GET_BUFFER_TIMEOUT_MILLISEC))
        print("\t {}: WAIT_ON_EVENT_TIMEOUT_MILLISEC {}".format(idx, device.WAIT_ON_EVENT_TIMEOUT_MILLISEC))

        # too long
        print("{}: nodemap \n\t{}".format(idx, device.nodemap))
        print("{}: tl_device_nodemap list \n\t{}".format(idx, device.tl_device_nodemap))
        print("{}: tl_interface_nodemap list \n\t{}".format(idx, device.tl_interface_nodemap))
        print("{}: tl_stream_nodemap list \n\t{}".format(idx, device.tl_stream_nodemap))
        print("\t"+"-"*40)

    target = device.nodemap.feature_names
    print(type(target))
    print(target)

    for feature in target[:int(len(target)/2)]:
        print(device.nodemap[feature])
        print()
        


    destroy_deviceConnection(deviceList)
    print("\nCode Test: Create and Destroy clear\n")

    # system.tl_system_nodemap
    # system.tl_system_nodemap
    # system.tl_interface_nodemap
    # device.tl_device_nodemap
    # device.tl_stream_nodemap
    # device.tl_interface_nodemap
    # device.nodemap