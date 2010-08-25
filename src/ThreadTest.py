import pygame
from socket import *

hostname = 'localhost'
port = 10000
BUFFER_SIZE = 256

from threading import Thread

class Connection(Thread):
    def __init__(self, id):
        Thread.__init__(self)

        #sessionSocket = socket(AF_INET, SOCK_STREAM)
        #sessionSocket.bind((hostname, 0))
        #sessionSocket.connect((hostname, port))
    
    def run(self):
        pass
    
    def update(self, message):
        pass
        #print "Thread" + self.id + ": " + str(self.count)

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.ConnectionList = []
        
        #serverSocket = socket(AF_INET, SOCK_STREAM)
        #serverSocket.bind((hostname, 0))
        #serverSocket.listen(5)
        
        for x in range(5):
            connection = Connection(str(x))
            connection.start()
            self.ConnectionList.append(connection)
        
    def __del__(self):
        for connection in self.ConnectionList:
            connection.join()
        
    def run(self):
        while (self.running):
            #pygame.time.Clock().tick(60)
            print "Updating"
            self.update()
            
    def end(self):
        self.running = False
            
    def update(self):
        for connection in self.ConnectionList:
            connection.update("#")
            
if __name__ == "__main__":
    s = Server()
    s.start()
    
    print "Hello"
    
    s.end()