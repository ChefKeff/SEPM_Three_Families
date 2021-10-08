# File containing client classes
# Imports of external packages
import socket
import os
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

    def sendFile(self, filePath):
        with open(filePath, 'rb') as f:
            content = f.read()
            self.s.send(content)
        return print(f'Sent {filePath}')

    def handleFile(self, filePath):
        with open(filePath, 'r+') as f:
            lines = f.readlines()
            if 'GAMEFILE' in lines[0]:
                print('Received a gamefile!')
                # Add functionality here.
                return
            elif 'TOURNAMENTFILE' in lines[0]:
                print('Received a tournamentfile!')
                # Add functionality here.
                return
            elif 'ERROR_LOG' in lines[0]:
                if 'DUPLICATE_NAME' in lines[1]:
                    print(lines[2])
                    content = lines[2].split()
                    self.pname = content[-1]
                    f.close()
                    os.remove(filePath)

            elif 'ENDFILE' in lines[0]:
                print('Received endfile!')
                self.closeClient()
                # Add functionality here.

            else:
                print(f'Received unknown file type: {lines[0]}')
            return


    def listeningThread(self):
        while True:

            # data received from client
            data = self.s.recv(1024)
            #print("efter data")
            if not data:
                print('Bye')
                break
                # lock released on exit

            filePath = self.pname+str(time.localtime())+'.txt'
            self.receiveFile(filePath, data)
            self.handleFile(filePath)

            #print_lock.release()

        self.s.close()

    def closeClient(self):
        self.s.close()

def main():
    #addr = str(input('Enter server address: '))
    #port = int(input('Enter server port: '))
    pname = str(input('Enter player name (without blankspaces): '))
    pname = pname.strip()
    addr = '127.0.0.1'
    port = 2232

    #pname='Player1'
    client = Client(addr, port, pname)
    time.sleep(15)
    if client.pname =='p1':
        print('sending')
        client.sendFile('testGameFile.txt')
    time.sleep(5)

    if client.pname =='p2':
        print('sending')
        client.sendFile('testGameFile0.txt')
    return


if __name__ == '__main__':
    main()
