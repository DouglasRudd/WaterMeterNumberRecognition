import urllib2
import time
import os

def get_raw_image_and_save_it(path_to_folder, device_url):
    f = urllib2.urlopen(device_url)
    image = f.read()
    __make_directory_if_not_exists(path_to_folder)
    newFile = open(path_to_folder+'img.raw', "wb")
    newFile.write(image)
    newFile.close()

def __make_directory_if_not_exists(path_to_folder):
    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)


if __name__ == '__main__':
    start = time.time()
    f = urllib2.urlopen('http://192.168.1.66')

    #
    # Here we request that bytes 18000--19000 be downloaded.
    # The range is inclusive, and starts at 0.
    #
    #req = urllib2.Request('http://www.izbori.hr/izbori/ws.nsf/2F197AFC895013B9C1257F07004066B5/$FILE/konacni_sluzbeni_rezultati_Sabor_2015.pdf')
    #req.headers['Range'] = 'bytes=%s-%s' % (0, 369199)
    #f = urllib2.urlopen(req)
    image = f.read()
    print ("--- %s seconds ---" % (time.time() - start))
    newFile = open("img.raw", "wb")
    newFile.write(image)
    newFile.close()
