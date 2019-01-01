import urllib2
import time
import urllib

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
