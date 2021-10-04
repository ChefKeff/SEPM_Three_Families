'''
This module consists of helping functions.

(C) 2021 Group G
'''

import time
import random


def clear_screen():
    '''Clears the screen from output.'''
    print('\n'*50)


def print_ascii(filename):
    '''Prints an ascii design by its filename.'''
    with open('ascii/'+filename, 'r', encoding='utf-8') as file:
        data = file.read()
    print(data)


def print_piece_count(w_count=0, b_count=0, pieces_in_hand=0, turns=0):
    '''Prints information box about players' pieces count

        Parameters:
            w_count (int): White player pieces count
            b_count (int): Black player pieces count

        Returns:
            None

    '''
    print('')
    print('┏' + '━'*52 + '┓')
    print('┃  ' + 'White Pieces: ' + str(w_count) + '/'+str(pieces_in_hand) + ' ' *
          (46-len('White Pieces:') - len(str(w_count))) + '┃')
    print('┃  ' + 'Black Pieces: ' + str(b_count) + '/'+str(pieces_in_hand) + ' ' *
          (46-len('Black Pieces:') - len(str(b_count))) + '┃')
    print('┃  ' + 'Turns: ' + str(turns) + '   ' + ' ' *
          (46-len('Turns:') - len(str(turns))) + '┃')


def print_boxed_message(message="", choices=[], shortcuts=[], pieces_count = True, w_count=-1, b_count=-1, pieces_in_hand=-1, turns=-1):
    '''Prints information box with message and choices

Parameters:
            message (str): White player pieces count
            choices (array): Choices in string format
            shortcuts (array): Shortcuts for choices in string format

Returns:
            None

    '''
    optionsstring = ""
    for i, choice in enumerate(choices):
        if len(shortcuts) > 0 and len(choices) == len(shortcuts):
            optionsstring = optionsstring + ">" + \
                choice.capitalize()+" ("+shortcuts[i]+")"+"    "
        else:
            optionsstring = optionsstring + ">" + choice.capitalize()+"    "

    if pieces_count == False:
        print('┏' + '━'*52 + '┓')
        print('┃  ' + message + ' '*(50-len(message)) + '┃')
        print('┣' + '━'*52 + '┫')
        print('┃' + ' '*52 + '┃')
        print('┃  ' + optionsstring + ' '*(50-len(optionsstring)) + '┃')
        print('┃' + ' '*52 + '┃')
        print('┗' + '━'*52 + '┛')
        
    else:
        if turns % 2  == 1:
            w_arrow = [">> ", " <<"]
            b_arrow = ["   ", "   "]
        else:
            w_arrow = ["   ", "   "]
            b_arrow = [">> ", " <<"]            
        
        #print("")
        print('┏' + '━'*70 + '┓ '                                        + '┏' + '━'*28 + '┓')
        print('┃  ' + message + ' '*(68-len(message)) + '┃ '             + '┃  Turns: ' + str(turns) + ' ' * (25-len('Turns:') - len(str(turns))) + '┃')
        print('┣' + '━'*70 + '┫ '                                        + '┣' + '━'*28 + '┫' )
        print('┃' + ' '*70 + '┃ '                                        + '┃  ' + w_arrow[0] + 'White Pieces: ' + str(w_count) + '/'+str(pieces_in_hand) +  w_arrow[1] + '  ┃')
        print('┃  ' + optionsstring + ' '*(68-len(optionsstring)) + '┃ ' + '┃  ' + b_arrow[0] + 'Black Pieces: ' + str(b_count) + '/'+str(pieces_in_hand) +  b_arrow[1] + '  ┃')
        print('┃' + ' '*70 + '┃ '                                        + '┃' + ' '*28 + '┃' )
        print('┗' + '━'*70 + '┛ '                                        + '┗' + '━'*28 + '┛' )



def boxed_output(message=""):
    '''Prints message in an information box

        Parameters:
            message (str): White player pieces count

        Returns:
            user input (str): Input from user

    '''
    print('┏' + '━'*52 + '┓')
    print('┃  ' + message + ' '*(50-len(message)) + '┃')
    print('┗' + '━'*52 + '┛')

    # Sleep in order to have time to show the error message
    time.sleep(1.5)

def prompt(message="", choices=None, shortcuts=None, callbacks=None, has_top=True):
    '''Prompts the user with message and choices and accepts only input existing in choices

        Parameters:
            message (str): The message to be displayed
            choices (array): Choices in string format
            shortcuts (array): Shortcuts for choices in string format
            callbacks (array): Callback functions tied to each choice in choices (in order)

        Returns:
            answer (str): User input
            None: If neither callbacks and choices are empty

    '''
    cleaned_choices = []
    cleaned_shortcuts = []
    if shortcuts is not None and len(choices) == len(shortcuts):
        for choice, shortcut in zip(choices, shortcuts):
            cleaned_choices.append(str(choice).lower())
            cleaned_shortcuts.append(str(shortcut).lower())
        choices = cleaned_choices
        shortcuts = cleaned_shortcuts
    elif choices is not None:
        for choice in choices:
            cleaned_choices.append(str(choice).lower())
        choices = cleaned_choices

    done = False

    while not done:
        index = None
        print_ascii('logo.txt')
        print_boxed_message(message, choices, shortcuts, has_top)

        answer = input().lower()

        if answer in choices or answer in shortcuts:
            if answer in choices:
                index = choices.index(answer)
            else:
                index = shortcuts.index(answer)
        elif len(choices) == 0:
            index = -1
        else:
            clear_screen()
            print("> Error: Please choose a valid option")
            continue

        if index is not None and index != -1 and callbacks is not None:
            callbacks[index]()
        elif index == -1:
            if len(callbacks) > 0:
                callbacks[0](answer)
            else:
                return answer

        done = True


def notification(message="", choices=None, w_count=-1, b_count=-1, pieces_in_hand=-1, turns=-1):
    '''Prompts the user with message and choices

        Parameters:
            message (str): The message to be displayed
            choices (array): Choices in string format

        Returns:
            answer (str): User input

    '''
    #if w_count != -1 and b_count != -1 and pieces_in_hand != -1 and turns != -1:
        #print_piece_count(w_count, b_count, pieces_in_hand, turns)
    print_boxed_message(message, choices, [] , True, w_count, b_count, pieces_in_hand, turns)
    answer = input()
    return answer


def print_complete_rules():
    '''Prints the full game rules.'''
    print('''
    UU Game Rules
    1. The game is played by two people.
    2. One player holds white pieces and the other holds black pieces.
    3. At the beginning, each player has 11 pieces in hand.
    4. White always start first.
    5. A player can either perform a move or a remove action
       in each round (if possible).
    6. Only one piece can exist on each empty position on the board at the same time
    7. The move action is divided into three stages.
         First stage - When the game start
            7.1 You can place one of your pieces on any position on the board.
            7.2 Enter second stage when there are no pieces to place.

         Second stage
            7.3 You can move your pieces on the board one step along the line
            7.4 Enter third stage when you only have three pieces left on the board.

         Third stage
            7.5 You can move one of your pieces to any position on the board.

    8. Remove action
         8.1 If after the move action, the piece you moved is in the same
             straight line with the other two pieces of yours, you can remove
             any opponent's piece on the board that does not belong to Rule 7.2.
         8.2 If the opponent's pieces have three in a straight line, then you
             cannot remove those three pieces. (#####)

    9. Victory conditions
         After second stage if there are two opponent's pieces left on the board,
         you win the game.
    10. Tie conditions
         In the second stage, if any player cannot move, the game is a tie. (#####)''')


def show_rules():
    '''Prints the complete rules and waits for user to press enter to go back.'''
    clear_screen()
    print_complete_rules()
    print('Press <Enter> to continue')
    input()


def board_design(choice='default'):
    '''Returns requested board design. Cyberpunk or default.'''
    design = 'cyberpunk.txt' if choice == 'cyberpunk' else 'default.txt'
    with open('ascii/'+design, 'r', encoding='utf-8') as file:
        data = file.read()
    return data


def validate_game_input(answer):
    '''Checks where answer is a valid number.'''
    if answer is not None:
        try:
            float(answer)
            return True
        except ValueError:
            return False

    return False


def check_input_int(answer):
    '''Check if answer is an int/digit.'''
    if isinstance(answer, int):
        return True

    if not answer.isdigit():
        return False

    return True


def suggest_placement(board):
    '''Suggests a random placement between 1 and number of nodes.'''
    return "Ex: " + str(random.randrange(1, board.number_of_nodes))
