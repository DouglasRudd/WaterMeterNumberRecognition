__author__ = 'Krtalici'
__name__='main'
import serial
import time
if __name__ == 'main':
    image_width = 160
    image_height = 120
    flag = False
    #image_width = 320
    #image_height = 240
    bytesPerPixel = 2
    ser = serial.Serial(
            port = "COM3",
            baudrate = 921600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
        )
    print ser.name          # check which port was really used
    #ser.open()
    print ser.isOpen()
    time.sleep(2)
    ser.readall()
    ser.write('vgap\n')
    #print ser.readall()
    time.sleep(2)
    ser.readall()
    ser.write('EdgeYes\n')
    #print ser.readall()
    time.sleep(2)
    ser.readall()
    ser.write('t\n')
    #time.sleep(4)
    #print ser.readall()
    #time.sleep(40)
    #print ser.readall()
    #time.sleep(4)
    #ser.write('send\n')
    start = time.time()
    buf = ser.readall()
    print ("--- %s seconds ---" % (time.time() - start))
    #while ser.inWaiting() > 0:
        #buf += ser.read(1)
    #byteArray = bytearray(buf)
    newFile = open ("allThatComes.raw", "w")
    newFile.write(buf)
    newFile.close()
    result = buf[(buf.index("<img>")+len("<img>")+2):buf.index("</img>")]
    buf = result

    newFile = open ("img.raw", "wb")
    newFile.write(buf)
    newFile.close()
    #while( True ):
        #line = ser.readline()
        #print line
    ser.close()
