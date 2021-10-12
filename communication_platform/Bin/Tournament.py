# File containing Tournament classes

# Imports
import random
import os.path
import json

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
            print(address_ID[0], playerAddress)
            if address_ID[0] == playerAddress:
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
    # Returns a dict with player names, GAMESCORE and game status
    def readGameFile(self, filePath):
        # Define empty dict
        content = {
        'FPLAYER': "",
        'TPLAYER': "",
        "GAMESCORE": "",
        "GAMEDONE": ""
        }
        # Open gamefile (already received and stored locally)
        # Open with read only
        with open(filePath, 'r+') as f:
            data = json.load(f)

            content['FPLAYER'] = data['FPLAYER']
            content['FPCOLOUR'] = data['FPCOLOUR']
            content['TPLAYER'] = data['TPLAYER']
            content['TPCOLOUR'] = data['TPCOLOUR']
            content['GAMESCORE'] = data['GAMESCORE']
            if data['GAMEDONE'] == '1':
                content['GAMEDONE'] = True
            else:
                content['GAMEDONE'] = False
        # Return dict
        return content

    # Function for handling content of a game file sent between active
    def handleGameFile(self, filePath):
        fileContent = {}
        if "json" in filePath:
            f = open(filePath, )
            data = json.load(f)
            fileContent = data
        else:
            fileContent = self.readGameFile(filePath)

        # Extract the relevant content without altering the file
        
        # print('Content: ', fileContent)
        # If game is still active, return false (no action required)
        if fileContent['GAMEDONE'] != True:
            return False
        # Add one to games played
        self.gamesPlayed += 1
        self.history.update({self.gamesPlayed: {
        "players": [fileContent['FPLAYER'], fileContent['TPLAYER']],
        "score": fileContent['GAMESCORE']
        }})
        # If game is over and final score is greater than zero, add one point to sending player's score
        # Also update game history
        if fileContent['GAMESCORE'] > 0:
            self.scores[fileContent['FPLAYER']] += self.settings['win']
            self.scores[fileContent['TPLAYER']] += self.settings['loss']

            self.history[self.gamesPlayed].update({'winner': fileContent['FPLAYER']})
        # If final score is lower than zero, add one point to receiving player's score
        elif fileContent['GAMESCORE'] < 0:
            self.scores[fileContent['TPLAYER']] += self.settings['win']
            self.scores[fileContent['FPLAYER']] += self.settings['loss']

            self.history[self.gamesPlayed].update({'winner': fileContent['TPLAYER']})
        elif fileContent['GAMESCORE'] == 0:
            self.scores[fileContent['FPLAYER']] += self.settings['draw']
            self.scores[fileContent['TPLAYER']] += self.settings['draw']

            self.history[self.gamesPlayed].update({'winner': 'draw'})
        # Update player colours
        self.colours[fileContent['FPLAYER']].append(fileContent['FPCOLOUR'])
        self.colours[fileContent['TPLAYER']].append(fileContent['TPCOLOUR'])
        # Return true
        return(True)

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
            if len(self.matchups[p1]) <= len(self.players.items())-1:
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
            if len(self.matchups[p2]) <= len(self.players.items())-1:
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
            
            player1ColorCode, player2ColorCode = self.generateColorCode(player1, player2)
            nextGame = {'player1': player1, 'player1Colour': self.colorParser(player1ColorCode),
                        'player2': player2, 'player2Colour': self.colorParser(player2ColorCode)}
            # After this it won't be the first game
            self.firstGame = False
            # Return dict
            return nextGame
        # If  it's not the first game, generate a valid matchup
        nextGame = self.generateNextMatchup()
        if nextGame == False:
            return(False)
        # Generate placeholder colours
        player1ColorCode, player2ColorCode = self.generateColorCode(nextGame['player1'], nextGame['player2'])
        nextGame.update({'player1Colour': self.colorParser(player1ColorCode),
                         'player2Colour': self.colorParser(player2ColorCode)})
        return nextGame

    def generateFinalFile(self, filePath):
        dict = {}
        dict["ENDFILE"] = {}
        dict["ENDFILE"]["PLAYERSCORE"] = {}
        sortedScores = self.generateSortedScores()
        for player, score in sortedScores.items():
            dict["ENDFILE"]["PLAYERSCORE"][player] = score

        with open(filePath, "w") as outfile:
            json.dump(dict, outfile)
        return True
        #with open(filePath, 'w+') as f:
        #    f.write('ENDFILE\n')
        #    sortedScores = self.generateSortedScores()
        #    for player, score in sortedScores.items():
        #        # Add them in order to the file, one line per player
        #        f.write(f'PLAYERSCORE: {player} {score}\n')
        #return(True)

    def generateColorCode(self, player1Name, player2Name):
        player1ID = self.players[player1Name][1]
        player2ID = self.players[player2Name][1]
        
        player1ColorCode = self.matchingColor[player1ID][player2ID]
        #print(self.matchingColor)
        #print(player1ID, player2ID)
        player2ColorCode = 1 - player1ColorCode  # because we just have 2 color.
        print(player1ColorCode, player2ColorCode)
        return player1ColorCode, player2ColorCode

    def generateMatchColor(self):
        """
        This function is to generate all matching pair color
        for example: if player0 meets player1
        result[0][1] is the color for player0
        result[1][0] is the color for player1

        result[i][j] = 1 -> players i is black in the match against player j
        result[i][j] = 0 -> players i is white in the match against player j

        """
        numberOFPLAYER = len(self.players)
        result = [[-1 for _ in range(numberOFPLAYER)] for _ in range(numberOFPLAYER)]
        for i in range(numberOFPLAYER):
            prevNum = i % 2
            for j in range(numberOFPLAYER):
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
        # Get the sorted scoreboard
        sortedScores = self.generateSortedScores()
        # Generate data about next game
        nextGame = self.generateNextGameData()
        print(nextGame)
        if nextGame == False:
            self.generateFinalFile(filePath)
            return(False)
        #DICT IN ORDER TO MAKE JSON FILE !!!!!
        dict = {}
        dict['fileType'] = 'TOURNAMENTFILE'
        dict["PLAYERSCORE"] = {}
        #dict["TOURNAMENTFILE"] = "hej"
        dict["GAMESPLAYED"] = str(self.gamesPlayed)
        for player, score in sortedScores.items():
            dict["PLAYERSCORE"][player] = score
        nexTPLAYERs = ""
        for key, val in nextGame.items():
            if 'Colour' in key: 
                nexTPLAYERs = nexTPLAYERs + (val+' ')
                # If not colour field, it's the player field. Add the player
            else:
                nexTPLAYERs = nexTPLAYERs + (val+":")

        # "erik:B gabriel:W"
        sep = nexTPLAYERs.strip().split(' ')
        # ['erik:B', 'gabriel:W']

        next_players_dict = {}

        for p in sep:
            name_color = p.split(':')
            next_players_dict[name_color[0]] = name_color[1]
            
        # dict["NEXTPLAYERS"] = nexTPLAYERs 
        dict["NEXTPLAYERS"] = next_players_dict
        with open(filePath, "w") as outfile:
            json.dump(dict, outfile)
        
        return True

def main():

    ## plan the color order of games to make sure everyone gets to play both colors

    ### prompt players to initiate game
    tournament = Tournament()
    tournament.addPlayer('Player1',1234)
    tournament.addPlayer('Player2', 1235)
    tournament.addPlayer('Player3', 1236)
    print(tournament.players)
    tournament.generateTournamentFile('testTournamentFile.txt')
    #tournament.handleGameFile('testGameFile.txt')
    #tournament.handleGameFile('testGameFile0.txt')
    print(tournament.scores)
    print(tournament.history)
    print(tournament.colours)
    tournament.generateTournamentFile('testTournamentFile0.txt')
    # store the results in the tournament data in local variable
    # tournament_data += tournament
    # send out tournamnet data

if __name__ == '__main__':
    main()
