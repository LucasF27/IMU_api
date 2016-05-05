import threespace_api as ts_api
import time
import sys
import glob
import serial

def get_port():
    """Get the serial port where the device is connected. Only available on Windows and OSX
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :return:
        The serial port where the device is connected
    """
    port = 0
    if sys.platform.startswith('darwin'):
        port = glob.glob('/dev/tty.usbmodem*')[0]
    elif sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(32)]
        for p in ports:
            try:
                s = serial.Serial(p)
                s.close()
                port = p
            except (OSError, serial.SerialException):
                pass
    return port

dng_device = ts_api.TSDongle(com_port=get_port())
# device = ts_api.TSWLSensor(com_port=get_port())
device0 = dng_device[0]
device1 = dng_device[1]

## If a connection to the COM port fails, None is returned.
if device0 is not None:
    cont = 0
    print(device0)
    print(device1)
    device0.setStreamingTiming(0,0,1000000,True)
    ## Set the stream slots for getting the tared orientation of the device as a
    ## quaternion, the raw component data, and the button state
    device0.setStreamingSlots(   slot0='getTaredOrientationAsEulerAngles',
                                slot1='getNormalizedGyroRate')
    device1.setStreamingTiming(0,0,1000000,True)
    ## Set the stream slots for getting the tared orientation of the device as a
    ## quaternion, the raw component data, and the button state
    device1.setStreamingSlots(   slot0='getButtonState')

    ## Now we can start getting the streaming batch data from the device.
    print("==================================================")
    print("Getting the streaming batch data.")
    start_time = time.time()
    device0.startStreaming()
    device1.startStreaming()
    # device0.startRecordingData()
    old_time = 0
    new_time = 0
    # while cont < 10:
    #     print 'cont: ',cont,' - time: ',time.time()-start_time
    #     time.sleep(1)
    #     cont += 1
    # cont = 0
    # start_time = time.time()
    data0 = 0
    data1 = 0
    while time.time() - start_time < 1:
        # print device.stream_last_data
        # print device.getLatestStreamData(1000)
        # print device.stre
        # print("=======================================\n")
        # raw_input('go')
        data0 = device0.getStreamingBatch(True)
        data1 = device1.getStreamingBatch(True)
        new_time = data0[1]
        if not new_time == old_time:
            # print '0: ',data0
            # print '1: ',data1
            # print data[0][0]
            # if not data0[0][6] == 0:
            #     print '0: ',data0[0][6]
            # if not data1[0][6] == 0:
            #     print '1: ',data1[0][6]
            cont += 1
            old_time = new_time
        # print time.clock()
    ## Now close the port.
    print 'time: ',time.time()-start_time
    print 'cont: ',cont
    # device0.stopRecordingData()
    device0.stopStreaming()
    device1.stopStreaming()
    device0.close()
    device1.close()



