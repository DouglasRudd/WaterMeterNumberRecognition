__author__ = 'Krtalici'
#!/usr/bin/env python

# Display images from the MSP430<->OV7670 project

import pygame
import sys
import serial
import time
from PIL import Image
import numpy as np

def parsergb565(byte1, byte2):
    byte12 = byte1 << 8 | byte2

    byte12 = byte1 << 8 | byte2

    red = byte12 >> 8+3
    green = (byte12 >> 5) & 0x3f
    blue = byte12 & 0x1f

    red *= 8
    green *= 4
    blue *= 8

    return (red, green, blue)

def camera_capture():
    writeslow('qqvga\n',ser)
    time.sleep(2)
    writeslow('t\n',ser)
    time.sleep(5)
    #l = ser.readline().strip()

def camera_rrst():
    l = ''
    while l != 'OK':
        writeslow('rrst\r')
        time.sleep(0.1)
        l = ser.readline().strip()



# the software uart on the ov7670 project is not perfect...
def writeslow(s, ser):
    for c in s:
        ser.write(c)
        time.sleep(0.01)

def drawimage( buf, image_height, image_width ):
    for y in range(0, image_height):
        i = 0
        for x in range(0, image_width):
            color = parsergb565(
                ord(buf[y][i]),
                ord(buf[y][i + 1]))
            i += 2

            screen.set_at((x, y), color)
            #screen.set_at((2 * x + 1, 2 * y), color)
            #screen.set_at((2 * x, 2 * y + 1), color)
            #screen.set_at((2 * x + 1, 2 * y + 1), color)

def getImage(buf, image_width, image_height):
    arr = np.fromstring(buf,dtype=np.uint16).astype(np.uint32)
    arr = ((arr & 0xF800) << 16) + ((arr & 0x07E0) << 13) + ((arr & 0x001F) << 11) + 0xFF
    return Image.frombuffer('RGBA', (image_width,image_height), arr, 'raw', 'RGBA', 0, 1)

if __name__ == '__main__':
    image_width = 160
    image_height = 120
    flag = False
    #image_width = 320
    #image_height = 240
    bytesPerPixel = 2
    buf = [None] * image_height

    ser = serial.Serial(
            port = 4,
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
        )
    ser.close()
    ser.open()
    ser.isOpen()
    print 'Serial port open'

    print 'Reading image from camera...'
    starttime = time.time()
    #buf = readimage()
    camera_capture()
    time.sleep(2)
    for y in range(0, image_height):
        buf[y] = ser.read(image_width*bytesPerPixel)
    print 'Read complete in %.3f seconds' % (time.time() - starttime)

    print 'Opening window'
    width = image_width
    height = image_height*image_height
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    running = True
    while running:
        drawimage(buf, image_height, image_width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    #buf = readimage()
                    pass
        pygame.display.flip()

        clock.tick(240)