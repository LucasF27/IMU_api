## Getting the streaming batch data from the YEI 3-Space Sensor devices with
## Python 2.7, PySerial 2.6, and YEI 3-Space Python API

import threespace_api as ts_api
import time
import serial

time_to_count = 1

def read_data(serial_port):
    start_time = time.time()
    count0 = 0
    count1 = 0
    count2 = 0
    while time.time() - start_time < time_to_count:
        bytes_to_read = serial_port.inWaiting()
        if bytes_to_read > 0:
            data = bytearray(serial_port.read(bytes_to_read))
            # print()
            if data[6] == 1:
                count1 = count1 + 1
            elif data[6] == 2:
                count2 = count2 + 1
            elif data[6] == 0:
                count0 = count2 + 1
            # print("data:")
            # print ":".join(hex(c) for c in data)
            # print(data.decode())
        # else:
            # print "no data"
    freq0 = count0/time_to_count
    freq1 = count1/time_to_count
    freq2 = count2/time_to_count
    print "Frequency 0: ", freq0
    print "Frequency 1: ", freq1
    print "Frequency 2: ", freq2


################################################################################
################ Second getting data over a wireless connection ################
################################################################################
# device_list = ts_api.getComPorts(filter=ts_api.TSS_FIND_DNG)


## Only one 3-Space Sensor Dongle device is needed so we are just going to
## take the first one from the list.
# com_port = device_list[0]
port = '/dev/tty.usbmodemFD121'
dng_device = ts_api.TSDongle(com_port=port)

## If a connection to the COM port fails, None is returned.
if dng_device is not None:
    ## Now we need to get our Wireless device from our Dongle device.
    ## Indexing into the TSDongle instance like it was a list will return a
    ## TSWLSensor instance.
    wl_device = dng_device[1]
    wl_device2 = dng_device[2]
    wl_device3 = dng_device[0]

    ## Set the stream slots for getting the tared orientation of the device as a
    ## quaternion, the raw component data, and the button state
    wl_device.setFilterMode(0) # 1 is Kalman (Default), 0 is no filter
    wl_device.setStreamingTiming(interval=0,delay=0,duration=time_to_count*1000000,timestamp=False)
    wl_device.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                                slot1='getNormalizedGyroRate',
                                slot2='getButtonState')
    # wl_device.setStreamingSlots(slot0='getButtonState')


    # wl_device.stopStreaming()
    # dng_device.close()
    # wl_device2.setFilterMode(1) # 1 is Kalman (Default), 0 is no filter
    wl_device2.setStreamingTiming(interval=0,delay=0,duration=time_to_count*1000000,timestamp=False)
    wl_device2.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                                slot1='getNormalizedGyroRate',
                                slot2='getButtonState')
    # wl_device.setStreamingSlots(slot0='getButtonState')

    wl_device3.setStreamingTiming(interval=0,delay=0,duration=time_to_count*1000000,timestamp=False)
    wl_device3.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
                                slot1='getNormalizedGyroRate',
                                slot2='getButtonState')

    wl_device.startStreaming(False)
    # wl_device2.startStreaming(False)
    # wl_device3.startStreaming(False)
    # wl_device.stopStreaming()
    dng_device.close()
    serial_port = serial.Serial(port=port, baudrate=115200, timeout=0.001)
    read_data(serial_port)
    # wl_device.stopStreaming()
    # dng_device.close()
    exit()


    ## Now we can start getting the streaming batch data from the device.
    print("==================================================")
    print("Getting the streaming batch data.")
    start_time = time.time()
    while time.time() - start_time < 1:
        # print(time.clock() - start_time)
        print(wl_device.getStreamingBatch(True))
        print(dng_device._getMa)
        print("=======================================\n")
        time.sleep(0.1)

    ## Now close the port.
    dng_device.close()




