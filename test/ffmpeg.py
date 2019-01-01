import subprocess as sp
import numpy as np
import cv2

__author__ = 'Krtalici'

def saveImageInMemory():
    command = [FFMPEG_BIN,
        '-f','rawvideo',
        '-s','640x480',
        '-pix_fmt', 'bayer_bggr8',
        '-i','img.raw',
        '-f','image2pipe',
        '-pix_fmt','rgb24',
        '-vcodec','rawvideo',
        '-']

    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=660*490*3)

    rawImage = pipe.stdout.read(640*480*3)
    image = np.fromstring(rawImage, dtype='uint8')
    pipe.stdout.flush()
    image = image.reshape((480, 640, 3))

    cv2.imshow("Slicica", image)
    cv2.waitKey(0)

def saveImageOnDisk():
    command = [FFMPEG_BIN,
        '-f','rawvideo',
        '-s','640x480',
        '-pix_fmt', 'bayer_bggr8',
        '-i','img.raw',
        '-f','image2',
        '-vcodec', 'png',
        'image.png']

    pipe = sp.Popen(command, stdout=sp.PIPE)
    rawImage = pipe.stdout.read(640*480*3)
    image = np.fromstring(rawImage, dtype='uint8')
    pipe.stdout.flush()
    #image = image.reshape((480,640,3))
    image = cv2.imread('image.png')

    cv2.imshow("Slikica", image)
    cv2.waitKey(0)


def saveImageOnDiskQqvga():
    command = [FFMPEG_BIN,
        '-f','rawvideo',
        '-s','160x120',
        '-pix_fmt', 'yuyv422',
        '-i','image.raw',
        '-f','image2',
        '-vcodec', 'png',
        'imgqqvga.png']

    pipe = sp.Popen(command, stdout=sp.PIPE)
    rawImage = pipe.stdout.read(160*120*3)
    image = np.fromstring(rawImage, dtype='uint8')
    pipe.stdout.flush()
    #image = image.reshape((480,640,3))
    image = cv2.imread('imgqqvga.png')

    cv2.imshow("Slikica", image)
    cv2.waitKey(0)

def saveImageOnDiskQqvga():
    command = [FFMPEG_BIN,
        '-f','rawvideo',
        '-s','320x240',
        '-pix_fmt', 'yuyv422',
        '-i','img.yuv',
        '-f','image2',
        '-vcodec', 'png',
        'imgqvga.png']

    pipe = sp.Popen(command, stdout=sp.PIPE)
    rawImage = pipe.stdout.read(320*240*3)
    image = np.fromstring(rawImage, dtype='uint8')
    pipe.stdout.flush()
    #image = image.reshape((480,640,3))
    image = cv2.imread('imgqvga.png')

    cv2.imshow("Slikica", image)
    cv2.waitKey(0)



if __name__ == '__main__':

    FFMPEG_BIN = "ffmpeg.exe"

    #saveImageInMemory()

    saveImageOnDisk()

    #saveImageOnDiskQqvga()

    #saveImageOnDiskQqvga()


