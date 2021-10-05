# File containing Tournament classes

# Imports
import random
import os.path

# Tournament class
class Tournament:
    def __init__(self, win=3, draw=1, loss=0):
        # Dict for storing settings
        self.settings = {"win": int(win), "draw": int(draw), "loss": int(loss)}
        # Dict for storing player scores
        self.scores = {}
        # Dict for storing player names, addresses and playerId
        self.players = {}
        # Dict for keeping matchup history
        self.matchups = {}
        # Dict for keeping colouring history
        self.colours = {}
        # Dict for keeping game history
        self.history = {}
        # Int for keeping track of number of games
        self.gamesPlayed = 0
        # Boolean for keeping track of first game
        self.firstGame = True
        # This is the lookup table to define colors of player. See generateMatchColor function for more details
        self.matchingColor = []


        ### read game history from server (such as last move made) from txt file

        ### let player make her/his move

        ### store the data for that players move and send to server

        ## if game finish ->
            # let host decide point format? (not sure what this is for)
            # let everyone know that game is over and the results
            # return
        return

    # Function for adding a player to the tournament
    def addPlayer(self, playerName, playerAddress, playerID=0):
        # Check if player is new
        for address_ID in self.players.values():
            if address_ID[0][1] == playerAddress:
                # if playerAddress in self.players.values():
                print(playerAddress)
                # If not, print for logging and return False
                print(f'{playerAddress} already registered!')
                return False
        # Check if player name is already taken
        if playerName in self.players.keys():
            # If so, print for logging and give a new name
            print(f'{playerName} already taken, new name is {playerName + str(len(self.players))}')
            playerName = playerName + str(len(self.players))
        # If new, add player to dict
        self.players.update({playerName: [playerAddress, playerID]})
        self.matchups.update({playerName: []})
        self.colours.update({playerName: []})
        self.scores.update({playerName: 0})
        return playerName

    # Function for reading a game file sent between players
    # Returns a dict with player names, gamescore and game status
    def readGameFile(self, filePath):
        # Define empty dict
        content = {
        'fplayer': "",
        'tplayer': "",
        "gamescore": "",
        "gamedone": ""}
        # Open gamefile (already received and stored locally)
        # Open with read only
        with open(filePath, 'r+') as f:
            # Split the file into lines
            lines = f.readlines()
            # Iterate over each line
            for line in lines:
                # Strip the line of trailing blankspaces
                line.rstrip()
                # Split the line into a list of words
                # Splitting is done on blanksplace as default
                line = line.split()
                # If line is empty, skip it
                if line == []:
                    continue
                # Check if line starts with tournament keyword
                # If so, add information to dict
                if line[0] == "FPLAYER:":
                    content['fplayer'] = line[1]
                if line[0] == "FPCOLOUR:":
                    content['fpcolour'] = line[1]
                if line[0] == 'TPLAYER:':
                    content['tplayer'] = line[1]
                if line[0] == 'TPCOLOUR:':
                    content['tpcolour'] = line[1]
                if line[0] == 'GAMESCORE:':
                    content['gamescore'] = int(line[1])
                if line[0] == 'GAMEDONE:':
                    if line[1] == '1':
                        content['gamedone'] = True
                    else:
                        content['gamedone'] = False
            # When all lines are read, file is closed
        # Return dict
        return content

    # Function for handling content of a game file sent between active players
    def handleGameFile(self, filePath):
        # Extract the relevant content without altering the file
        fileContent = self.readGameFile(filePath)
        # If game is still active, return false (no action required)
        if fileContent['gamedone'] != True:
            return False
        # Add one to games played
        self.gamesPlayed += 1
        self.history.update({self.gamesPlayed: {
        "players": [fileContent['fplayer'], fileContent['tplayer']],
        "score": fileContent['gamescore']
        }})
        # If game is over and final score is greater than zero, add one point to sending player's score
        # Also update game history
        if fileContent['gamescore'] > 0:
            self.scores[fileContent['fplayer']] += self.settings['win']
            self.scores[fileContent['tplayer']] += self.settings['loss']

            self.history[self.gamesPlayed].update({'winner': fileContent['fplayer']})
        # If final score is lower than zero, add one point to receiving player's score
        elif fileContent['gamescore'] < 0:
            self.scores[fileContent['tplayer']] += self.settings['win']
            self.scores[fileContent['fplayer']] += self.settings['loss']

            self.history[self.gamesPlayed].update({'winner': fileContent['tplayer']})
        elif fileContent['gamescore'] == 0:
            self.scores[fileContent['fplayer']] += self.settings['draw']
            self.scores[fileContent['tplayer']] += self.settings['draw']

            self.history[self.gamesPlayed].update({'winner': 'draw'})
        # Update player colours
        self.colours[fileContent['fplayer']].append(fileContent['fpcolour'])
        self.colours[fileContent['tplayer']].append(fileContent['tpcolour'])
        # Return true
        return True

    # Function for generating a sorted scoreboard dict
    def generateSortedScores(self):
        return dict(sorted(self.scores.items(), key=lambda item: item[1]))

    def generateNextMatchup(self):
        # Initiate list for keeping track of candidates checked
        checkedP1 = []
        checkedP2 = []
        # Initiate booleans for loops
        newP1 = True
        newP2 = True

        while newP1:
            # Generate a random p1
            p1 = random.choice(list(self.players.keys()))
            # Add p1 to list of checked
            if p1 not in checkedP1:
                checkedP1.append(p1)
                # If all players has been checked, tournament is over
                if len(checkedP1)==len(self.players.keys()):
                    return False
            print('Player1:', p1)
            # Assume p1 is valid
            newP1 = False
            # Check if p1 has any new matchups
            if len(self.matchups[p1]) >= len(self.players.items())-1:
                # If not, find a new p1
                newP1 = True

        while newP2:
            # Generate a random p2
            p2 = random.choice(list(self.players.keys()))
            # Add to list of checked if not already there
            if p2 not in checkedP2:
                checkedP2.append(p2)
                # Check if all players has been checked for player2
                if len(checkedP2) == len(self.players.keys()):
                    print('ERROR: In generateNextMatchup - All players checked for player 2, this shouldnt happen')
                    return False
            print('Player2', p2)
            # Assume p2 is valid
            newP2 = False
            # Check if p2 is the same as p1
            if p2 == p1:
                newP2 = True
            # Check if p2 already met p1
            if p2 in self.matchups[p1]:
                newP2 = True
            # Check if p2 has any matchups left
            if len(self.matchups[p2]) >= len(self.players.items())-1:
                newP2 = True
        return {'player1': p1, 'player2': p2}

    # Function for generating data about the next game to be sent to the players
    def generateNextGameData(self):
        # If it is the first game
        print(f'In generate, {self.firstGame}')
        if self.firstGame:
            # Randomly pick players
            player1 = random.choice(list(self.players.keys()))
            player2 = random.choice(list(self.players.keys()))
            # Make sure they're not the same player
            while player2 == player1:
                player2 = random.choice(list(self.players.keys()))
            # Create dict
            nextGame = {'player1': player1, 'player1Colour': 'B', 'player2': player2, 'player2Colour': "W"}
            # After this it won't be the first game
            self.firstGame = False
            # Return dict
            return nextGame
        # If  it's not the first game, generate a valid matchup
        nextGame = self.generateNextMatchup()
        # Generate placeholder colours
        player1ID = self.players[nextGame['player1']][1]
        player2ID = self.players[nextGame['player1']][1]
        player1ColorCode = self.matchingColor[player1ID][player2ID]
        player2ColorCode = 1 - player1ColorCode  # because we just have 2 color.
        nextGame.update({'player1Colour': self.colorParser(player1ColorCode), 'player2Colour': player2ColorCode})
        return nextGame

    def generateMatchColor(self):
        """
        This function is to generate all matching pair color
        for example: if player0 meets player1
        result[0][1] is the color for player0
        result[1][0] is the color for player1

        result[i][j] = 1 -> players i is black in the match against player j
        result[i][j] = 0 -> players i is white in the match against player j

        """
        numberOfPlayer = len(self.players)
        result = [[-1 for _ in range(numberOfPlayer)] for _ in range(numberOfPlayer)]
        for i in range(numberOfPlayer):
            prevNum = i % 2
            for j in range(numberOfPlayer):
                if i == j:
                    continue
                if prevNum == 0:
                    prevNum = result[i][j] = 1
                    continue
                prevNum = result[i][j] = 0
        self.matchingColor = result
        return

    def colorParser(self, num):
        """this function is to return the color of a player given a code"""
        if num == 0:
            return "W"
        if num == 1:
            return "B"

    # Function for generating the tournament data file sent to the players
    def generateTournamentFile(self, filePath):
        print('In Tournament')
        # Get the sorted scoreboard
        sortedScores = self.generateSortedScores()
        # Generate data about next game
        nextGame = self.generateNextGameData()
        # Open a writable file
        with open(filePath, 'w+') as f:
            print(f'Opened {filePath}')
            # Add how many games has been played
            f.write(f'GAMESPLAYED: {self.gamesPlayed}\n')
            # Iterate over each player in the dict with sorted scores
            for player, score in sortedScores.items():
                # Add them in order to the file, one line per player
                f.write(f'PLAYERSCORE: {player} {score}\n')
            # Add next players tag
            f.write('NEXTPLAYERS: ')
            # Iterate over all key-value pairs in the nextgame dict
            for key, val in nextGame.items():
                # If the colour field, add the colour to the player
                if 'Colour' in key:
                    f.write(val+' ')
                # If not colour field, it's the player field. Add the player
                else:
                    f.write(val+':')
            # Finish next player with a newline
            f.write('\n')
        # Close the file and exit function
        return True


def main():

    ## plan the color order of games to make sure everyone gets to play both colors

    ### prompt players to initiate game
    tournament = Tournament()
    tournament.addPlayer('Player1', 12344)
    tournament.addPlayer('Player2', 1235)
    tournament.addPlayer('Player3', 1236)
    print(tournament.players)
    tournament.generateTournamentFile('testTournamentFile.txt')
    tournament.handleGameFile('testGameFile.txt')
    tournament.handleGameFile('testGameFile0.txt')
    print(tournament.scores)
    print(tournament.history)
    print(tournament.colours)
    tournament.generateTournamentFile('testTournamentFile0.txt')
    # store the results in the tournament data in local variable
    # tournament_data += tournament
    # send out tournamnet data


if __name__ == '__main__':
    main()
