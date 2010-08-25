from socket import *

hostname = ''
port = 10002

BUFFER_SIZE = 256

print "Creating socket..."
serverSocket = socket(AF_INET, SOCK_STREAM)
print "Binding socket..."
serverSocket.bind((hostname, port))
print "Listening for connections..."
serverSocket.listen(5)

sessionSocket, address = serverSocket.accept()
print "Client connected!"

data = sessionSocket.recv(BUFFER_SIZE)

if data:
    sessionSocket.send(data)

sessionSocket.close()