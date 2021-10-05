# File containing client classes
# Imports of external packages
import socket
from _thread import *
import threading
import json
import time


print_lock = threading.Lock()

# Class for handling everyting on the client side
class Client:
    def __init__(self, serverAddress, serverPort, pname):

        # Set how many bytes to accept from a socket
        self.ID = 0
        self.bufferSize = 4096
        # Set playername in game
        self.pname = pname
        # Inititate a Socket
        self.s = socket.socket()
        # Connect to a socket with a given address and port
        # For now it's localhost per default
        self.s.connect((socket.gethostname(),serverPort))
        # Receive a file that is sent instantly from the server
        # self.receiveFile(self.s,'testReceive.txt')
        self.s.send(str.encode(json.dumps({'name': self.pname})))

        # start_new_thread(self.threaded, (self.s, ))

        x = threading.Thread(target=self.listeningThread)
        x.start()

        return

    # Function for receiving a file from a socket
    # This function assumes that all data is sent in one transmission, ie the file isn't bigger than bufferSize
    def receiveFile(self, filePath, data):
        # Open or create a file at the given address
        with open(filePath, "wb") as f:
            # Write the data to the file
            f.write(data)
        return True

    def sendFile(self, msg):
        self.s.send(msg.encode("utf-8"))

    def sendFile(self, filePath):
        with open(filePath, 'rb') as f:
            content = f.read()
            self.s.send(content)
        return print(f'Sent {filePath}')

    def listeningThread(self):
        while True:

            # data received from client
            data = self.s.recv(1024)
            #print("efter data")
            if not data:
                print('Bye')
                break
                # lock released on exit

            filePath = str(time.localtime())+'.txt'
            self.receiveFile(filePath, data)

            #print_lock.release()

        self.s.close()

    def closeClient(self):
        self.s.close()
        print_lock.release()

def main():
    #addr = str(input('Enter server address: '))
    #port = int(input('Enter server port: '))
    pname = str(input('Enter player name (without blankspaces): '))
    addr = '127.0.0.1'
    port = 2232

    #pname='Player1'
    client = Client(addr, port, pname)
    time.sleep(15)
    print('sending')
    client.s.send(f'From {pname}.'.encode('ascii'))
    return


if __name__ == '__main__':
    main()
