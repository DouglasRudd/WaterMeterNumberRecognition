import socket              # Import socket module
if __name__ == '__main__':
    s = socket.socket()      # Create a socket object
    #host = s.gethostname() # Get local machine name
    port = 80                # Reserve a port for your service.

    s.connect(('192.168.1.66', port))
    image = s.recv(307200)
    newFile = open ("img.raw", "wb")
    newFile.write(image)
    newFile.close()

    s.close