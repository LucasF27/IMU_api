## Getting the streaming batch data from the YEI 3-Space Sensor devices with
## Python 2.7, PySerial 2.6, and YEI 3-Space Python API

import threespace_api as ts_api
import time
import serial
import struct
import math

time_to_count = 20

def read_data(serial_port):
    start_time = time.time()
    count0 = 0
    count1 = 0
    count2 = 0
    while time.time() - start_time < time_to_count:
        bytes_to_read = serial_port.inWaiting()
        if bytes_to_read > 0:
            data = bytearray(serial_port.read(bytes_to_read))

            x = ''.join(chr(i) for i in data[8:12]) # angle y
            # b = ''.join(chr(i) for i in data[24:28]) # gyro y
            x = struct.unpack('>f', x)
            x = x[0]

            y = ''.join(chr(i) for i in data[12:16]) # angle y
            # b = ''.join(chr(i) for i in data[24:28]) # gyro y
            y = struct.unpack('>f', y)
            y = y[0]

            z = ''.join(chr(i) for i in data[16:20]) # angle y
            # b = ''.join(chr(i) for i in data[24:28]) # gyro y
            z = struct.unpack('>f', z)
            z = z[0]

            accelx = ''.join(chr(i) for i in data[32:36]) # angle y
            # b = ''.join(chr(i) for i in data[24:28]) # gyro y
            accelx = struct.unpack('>f', accelx)
            accelx = accelx[0]

            accely = ''.join(chr(i) for i in data[36:40]) # angle y
            # b = ''.join(chr(i) for i in data[24:28]) # gyro y
            accely = struct.unpack('>f', accely)
            accely = accely[0]

            accelz = ''.join(chr(i) for i in data[40:44]) # angle y
            # b = ''.join(chr(i) for i in data[24:28]) # gyro y
            accelz = struct.unpack('>f', accelz)
            accelz = accelz[0]

            # print(x,y,z,accelx,accely,accelz)
            ang = y/math.pi*180
            # if accelz < 0 and ang >= 0:
            #     ang = ang + 2*(90 - ang)
            if ang<0:
                ang = 360+ang
                if accelz < 0:
                    ang = ang - 2*(ang - 270)
            else:
                if accelz < 0:
                    ang = ang + 2*(90 - ang)
            print(ang)
            if data[6] == 1:
                count1 = count1 + 1
            elif data[6] == 2:
                count2 = count2 + 1
            elif data[6] == 0:
                count0 = count2 + 1
            # print("data:")
            # print ":".join(hex(c) for c in data)
        # time.sleep(0.5)
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
port = '/dev/tty.usbmodemFA131'
dng_device = ts_api.TSDongle(com_port=port)

## If a connection to the COM port fails, None is returned.
if dng_device is not None:
    ## Now we need to get our Wireless device from our Dongle device.
    ## Indexing into the TSDongle instance like it was a list will return a
    ## TSWLSensor instance.
    wl_device = dng_device[1]
    # wl_device2 = dng_device[2]
    # wl_device3 = dng_device[0]

    ## Set the stream slots for getting the tared orientation of the device as a
    ## quaternion, the raw component data, and the button state
    wl_device.setEulerAngleDecompositionOrder(3)
    wl_device.tareWithCurrentOrientation()
    wl_device.setFilterMode(1) # 1 is Kalman (Default), 0 is no filter
    wl_device.setStreamingTiming(interval=0,delay=0,duration=time_to_count*1000000,timestamp=False)
    wl_device.setStreamingSlots(slot0='getTaredOrientationAsEulerAngles',
                                slot1='getNormalizedGyroRate',
                                slot2='getNormalizedAccelerometerVector')
    # wl_device.setStreamingSlots(slot0='getUntaredOrientationAsEulerAngles',
    #                             slot1='getNormalizedGyroRate')
    # wl_device.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
    #                             slot1='getNormalizedGyroRate')
    wl_device.tareWithCurrentOrientation()
    #                             slot2='getButtonState')
    # wl_device.setStreamingSlots(slot0='getButtonState')


    # wl_device.stopStreaming()
    # dng_device.close()
    # wl_device2.setFilterMode(1) # 1 is Kalman (Default), 0 is no filter
    # wl_device2.setStreamingTiming(interval=0,delay=0,duration=time_to_count*1000000,timestamp=False)
    # wl_device2.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
    #                             slot1='getNormalizedGyroRate',
    #                             slot2='getButtonState')
    # wl_device2.setStreamingSlots(slot0='getButtonState')

    # wl_device3.setStreamingTiming(interval=0,delay=0,duration=time_to_count*1000000,timestamp=False)
    # wl_device3.setStreamingSlots(slot0='getTaredOrientationAsQuaternion',
    #                             slot1='getNormalizedGyroRate',
    #                             slot2='getButtonState')
    # wl_device3.setStreamingSlots(slot0='getButtonState')

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
        print("=======================================\n")
        time.sleep(0.1)

    ## Now close the port.
    dng_device.close()




