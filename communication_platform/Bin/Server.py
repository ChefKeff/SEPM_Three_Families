# File containing Server classes
# Imports of external packages
import socket
from _thread import *
import threading
import json
import time

from Tournament import Tournament

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
            name = clientSocket.recv(1024)
            name = json.loads(name)

            self.tournament.addPlayer(name['name'], address, Server.connectedPlayer)
            Server.connectedPlayer += 1

            self.players.update({name['name']:clientSocket})
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
            # Receive data from the socket
            # bytesRead = clientSocket.recv(self.bufferSize)
            # Write the data to the file
            f.write(data)
        return True

    def sendTournamentFile(self):
        filePath = 'tournamentFile.txt'
        self.tournament.generateTournamentFile(filePath)
        for player in self.players.values():
            print(f'Sending to {player}')
            self.sendFile(player, filePath)
        return True

    def handleFile(self, filePath):
        with open(filePath, 'r+') as f:
            if f.readline() == 'GAMEFILE':
                self.tournament.handleGameFile(filePath)
                for line in f.readlines():
                    line = line.split()
                    if line[0].rstrip() == 'TPLAYER':
                        self.sendFile(self.players[line[1].rstrip()], filePath)
                        return f'Forwarded gamefile to {self.players[line[1].rstrip()]}'
        return


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
        filePath = 'tempFile.txt'
        while True:
            data = self.clientSocket.recv(1024)
            #self.send(data.decode("utf-8"))
            self.server.receiveFile(filePath, data)
            self.server.handleFile(filePath)

    def sendThread(self):
        while True:
            time.sleep(0.01)
            while len(self.sendQueue) != 0:
                self.clientSocket.send(self.sendQueue.pop(0))
                #self.clientSocket.send(f"Hallo {self.port}".encode("utf-8"))
            #print_lock.release()

    def send(self, msg):
        self.sendQueue.append(msg.encode("utf-8"))

    def onMsg(self, msg):
        print(msg.decode("utf-8"))


def main():
    print("before initiation")
    server = Server(2232)

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
            print('Initializing Torunament')
            server.tournament.generateMatchColor()  # this is to predefine color of player for each match
            server.sendTournamentFile()
            break
        elif act == 'ref':
            continue
        else:
            print(f'\'{act}\' is not a valid input.')


if __name__ == '__main__':
    main()
