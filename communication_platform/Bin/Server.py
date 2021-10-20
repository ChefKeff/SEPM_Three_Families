# File containing Server classes
# Imports of external packages
import socket
from _thread import *
import threading
import json
import time
import os

from communication_platform.Bin.Tournament import Tournament

print_lock = threading.Lock()

# Imports of internal packages

class Server:
    connectedPlayer = 0  # this static variable is to compute the number of player connected to assign ID
    def __init__(self, port):
        # Define what port to use, this should be entered by the host
        self.port = port
        # Dict for storing player's sockets
        self.players = {}

        self.connections = []
        self.tournament = Tournament()

        # Initiate the Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the given port on localhost
        self.s.bind((socket.gethostname(), port))
        print("socket binded to port", port)

        self.listenThread = threading.Thread(target=self.listenForConnections)
        self.listenThread.start()
        self.last_sent = None

        return

    def listenForConnections(self):
        # Define how many unanswered connections the socket will allow to queue
        self.s.listen(8)
        print("socket is listening")
        # Start listening to connections
        # For now, this loop will continue until manually terminated
        while True:
            # Accept an incomming connection

            clientSocket, address = self.s.accept()
            if len(self.players) >= 8:
                print('Game is full')
                continue

            # Print the address for logging purposes
            name = clientSocket.recv(1024*8)
            name = json.loads(name)  # This is the received name

            addedPlayerName = self.tournament.addPlayer(name['name'], address, Server.connectedPlayer) # This is the name after a client being added

            if addedPlayerName is not False and addedPlayerName != name['name']:
                dict = {}
                dict['fileType'] = "ERROR_LOG"
                dict['errorType'] = "DUPLICATE_NAME"
                dict['error_msg_for_client'] = f'{name} already taken, new name is {addedPlayerName}'
                errFilePath = f'client_{address}_ErrorLog.json'
                with open(errFilePath, "w") as outfile:
                    json.dump(dict, outfile)
                # We know that the name has been taken. Now we need to inform the client
                self.sendFile(clientSocket, errFilePath)
                os.remove(errFilePath)
                name['name'] = addedPlayerName

            Server.connectedPlayer += 1

            self.players.update({name['name']: clientSocket})
            # print_lock.acquire()
            print('Connected to :', address[0], ':', address[1], ': player', name['name'])

            connection = Connection(self, address[1], clientSocket)
            self.connections.append(connection)


        return

    def closeSocket(self):
        self.s.close()

    # Function for sending files through the socket
    def sendFile(self, clientSocket, filePath):
        # Define how many bytes to send at a time
        bufferSize = 4096
        # Open the file that is to be transferred
        with open(filePath, 'rb') as f:
            while True:
                # Read the given amount of data from the file
                bytesRead = f.read(bufferSize)
                # If no new data is read, all is sent. Break the loop
                if not bytesRead:
                    break
                # Send the read data through the socket
                clientSocket.sendall(bytesRead)
        return True

    def receiveFile(self, filePath, data):
        # Open or create a file at the given address
        with open(filePath, "wb") as f:
            # Write the data to the file
            f.write(data)
        return True

    def sendTournamentFile(self):
        filePath = 'tournamentFile.json'
        isGoing = self.tournament.generateTournamentFile(filePath)
        #Converts JSON file into JSON object
        f = open(filePath, )
        data = json.load(f)
        print("hejheghasdsad")
        print(data)
        
        for player in self.players.values():
            print(f'Sending to {player}')
            self.sendFile(player, filePath)
        if not isGoing:
            return(False)
        return(True)

    def handleFile(self, filePath):
        print('Handling file')
        with open(filePath, 'r+') as f:
            dictionary = json.load(f)
            
            if dictionary['fileType'] == 'GAMEFILE':

                ### adding some details to make sure that it's not sent twice to the same player
                testing = str(self.players[dictionary['TPLAYER']])
                split_list = testing.split(' ')
                for element in split_list:
                    if 'fd' in element:
                        new_port = element.replace('fd=', '')
                        new_port = new_port.replace(',', '')

                if self.last_sent == new_port:
                    return
                    #return dictionary['GAMEDONE'] == 1

                else:
                    self.sendFile(self.players[dictionary['TPLAYER']], filePath)
                    print('Forwarded gamefile to ' + dictionary['TPLAYER'])
                    self.last_sent = new_port
                    return dictionary['GAMEDONE'] == 1

            else:
                print(f'Received unknown file type ' + dictionary['fileType'])
                return
        return

def host():
    main()
    


class Connection:
    def __init__(self, server, port, clientSocket):
        self.server = server

        self.sendQueue = []
        self.clientSocket = clientSocket
        self.port = port
        y = threading.Thread(target=self.recvThread)
        y.start()
        x = threading.Thread(target=self.sendThread)
        x.start()

    def recvThread(self):
        filePath = 'receivedFile.json'
        while True:
            data = self.clientSocket.recv(1024*8)
            if not data:
                return
            # self.send(data.decode("utf-8"))
            self.server.receiveFile(filePath, data)
            isGameDone = self.server.handleFile(filePath)
            if isGameDone:
                isTournamentGoing = self.server.sendTournamentFile()
                if not isTournamentGoing:
                    self.server.closeSocket()

    def sendThread(self):
        while True:
            time.sleep(0.01)
            while len(self.sendQueue) != 0:
                self.clientSocket.send(self.sendQueue.pop(0))

    def send(self, msg):
        self.sendQueue.append(msg.encode("utf-8"))

    def onMsg(self, msg):
        print(msg.decode("utf-8"))


    

def main():
    # print("before initiation")
    server_port = input('Choose server port: ')
    server = Server(int(server_port))

    startGame = False
    while not startGame:
        if len(server.tournament.players) == 0:
            print('Waiting for players to connect...')
            time.sleep(5)
            continue
        if len(server.tournament.players) == 1:
            print('Currently only one player connected, waiting for at least one more...')
            time.sleep(5)
            continue
        print(f'Currently {len(server.tournament.players)} player(s) has joined.')
        print(server.tournament.players)
        act = input('Options: start - start the game, ref - refresh the count: ')
        if act == 'start':
            server.tournament.generateMatchColor()  # this is to predefine color of player for each match
            
            server.sendTournamentFile()
            #server.tournament.handleGameFile("testGameFile.json")
            #server.tournament.handleGameFile("testGameFile.txt")
            break
        elif act == 'ref':
            continue
        else:
            print(f'\'{act}\' is not a valid input.')


if __name__ == '__main__':
    main()
