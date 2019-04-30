"""
Junayd Anwar, 8959380
This is a Connect 4 module. The various functions throughout combine together 
to create a connect 4 program that can be played between 2 humans, a human 
against the computer, or the computer can simulate a game.
When referring to the rows and columns of the board, I will always use matrix
notation (i.e. i'th row and j'th column).
"""
from copy import deepcopy;
import random

#Task1: Initialise a new game
def newGame(player1,player2):
    """This function returns a dictionary game with keys player1, player2
    (corresponding to the names that player 1 and player 2 have given), who
    and board. who tells us which player has the current turn, and board 
    corresponds to the current setting of the game board."""
    game = {
        'player1' : player1,
        'player2' : player2,
        'who' : 1,
        'board' : [[0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
            }
    return game

def playerPiece(who):
    """This function takes the integer values of the board in the dictionary
    and returns empty spaces for 0, X for player1, and O for player2.""" 
    if who == 0:
        return " "
    elif who == 1:
        return "X"
    elif who == 2:
        return "O"

#Task2: Print a nicely formatted board
def printBoard(board):
    """This function prints the board in a nice format, with X's and O's for 
    player1 and player2 respectively, and spaces elsewhere."""
    print("\n|1|2|3|4|5|6|7|")
    print("+-"*7 + "+")
    for i in board:
        print("|"+"|".join(playerPiece(who) for who in i)+"|")
        
def correctBoard(board):
    """This function checks if the board given is in the correct format, i.e. a 
    a list containing 6 elements, and each of these elements being a list of 7 
    elements."""
    if len(board) != 6:
        return False
    else:
        for i in board:
            if len(i) != 7:
                return False
    return True     

#Task3: Load a game state
def loadGame():
    """This function reads the file game.txt and returns a game dictionary with
    the information from game.txt. If the game dictionary isn't in the correct
    format (i.e. like in newGame()), then an error is raised."""
    with open("game.txt",mode="rt",encoding="utf8") as gamesave:
        #checking if the game.txt contains 9 lines        
        if sum(1 for _ in gamesave) != 9:
            raise ValueError("Cannot load a valid game.")
    with open("game.txt",mode="rt",encoding="utf8") as gamesave:
        game = {}
        boardsave = []
        for i, line in enumerate(gamesave):
            #adding player1 and player2 to game
            if i == 0:
                game['player1']=line.strip()
            elif i == 1:
                game['player2']=line.strip()
            #adding who to game i.e. whose turn it was
            elif i == 2:
                game['who']=int(line.strip())
            #compiling the lines into a board and adding it as board to game
            else:
                boardsave.append([int(x) for x in line.strip().split(",")])
            game['board']=boardsave
        if game['who'] not in {1,2} or not correctBoard(game['board']):
            raise ValueError("Cannot load a valid game.")
    return game

def getName(game):
    """This function returns the name of the player who has the current
    turn."""
    if game['who'] == 1:
        return game['player1']
    elif game['who'] == 2:
        return game['player2']

#Task4: Get a list of all valid moves
def getValidMoves(board):
    """This function iterates through the board to find all the valid moves 
    (i.e. it excludes the columns that are filled) and returns the list of
    columns with valid moves."""
    validMoves = []
    for j in range(7):
        i = 5
        while validMoves.count(j) == 0 and i>=0:
            if board[i][j] == 0:
                validMoves.append(j)
            i -= 1    
    return validMoves

#Task5: Make a move
def makeMove(board,move,who):
    """This function places who's player piece in the move'th column and 
    returns the board."""
    for i in reversed(board):
        #from the bottom row up, it places a piece in the first zero it finds
        if i[move] == 0:
            i[move] = who
            return board
        
#Task6: Check for a winner        
def hasWon(board,who): 
    """This function returns True if player who has won, and false otherwise.
    It does so by checking all possible ways in which a win is possible."""
    #checking horizontals
    for i in range(6):
        for j in range(4):
            if board[i][j]==who and board[i][j+1]==who and board[i][j+2]==who and board[i][j+3]==who:
                return True
    #checking verticals
    for j in range(7):
        for i in range(3):
            if board[i][j]==who and board[i+1][j]==who and board[i+2][j]==who and board[i+3][j]==who:
                return True
    #checking positive diagonals
    for j in range(4):
        for i in range(3):
            if board[i][j]==who and board[i+1][j+1]==who and board[i+2][j+2]==who and board[i+3][j+3]==who:
                return True
    #checking negative diagonals
    for j in range(4):
        for i in range(5,2,-1):
            if board[i][j]==who and board[i-1][j+1]==who and board[i-2][j+2]==who and board[i-3][j+3]==who:
                return True
    return False

#Task9: Save a game
def saveGame(game):
    """This function saves the current setting of the game to game.txt. If the 
    game fails to save, a value error is raised."""
    if game['who'] not in {1,2} or not correctBoard(game['board']):
        raise ValueError
    else:
        with open("game.txt",mode="wt",encoding="utf8") as f:
            f.truncate()
            f.write(game['player1'] + "\n" + game['player2'] + "\n" + str(game['who']))
            for row in game["board"]:
                f.write("\n"+",".join(str(place) for place in row))
    return print("Your game has been saved.")
            
#Task7: An easy computer opponent
def suggestMove1(board,who):
    """This function contains a simple computer opponent which checks if it can
    immediately win the game. If it can't, it checks if it can block an 
    immediate win for its opponent. If this isn't possible either, it returns
    random move."""
    if who == 1:
        notwho = 2
    elif who == 2:
        notwho = 1
    winMoves = []
    blockMoves = []
    validMoves = getValidMoves(board)
    for move in validMoves:
        boardwho = deepcopy(board)
        boardnotwho = deepcopy(board)
        #list of winning moves
        if hasWon(makeMove(boardwho,move,who),who):
            winMoves.append(move)
        #list of blocking moves
        elif hasWon(makeMove(boardnotwho,move,notwho),notwho):
            blockMoves.append(move)
    if winMoves != []:
        return random.choice(winMoves)
    elif blockMoves != []:
        return random.choice(blockMoves)
    else:
        return random.choice(validMoves)
    
#Task10: A better computer opponent
def suggestMove2(board,who):
    """This function contains a simple computer opponent which checks if it can
    immediately win the game. If it can't, it checks if it can block an 
    immediate win for its opponent. If this isn't possible either, it returns
    random move."""
    if who == 1:
        notwho = 2
    elif who == 2:
        notwho = 1
    winMoves = []
    blockMoves = []
    validMoves = getValidMoves(board)
    for move in validMoves:
        boardwho = deepcopy(board)
        boardnotwho = deepcopy(board)
        #list of winning moves
        if hasWon(makeMove(boardwho,move,who),who):
            winMoves.append(move)
        #list of blocking moves
        elif hasWon(makeMove(boardnotwho,move,notwho),notwho):
            blockMoves.append(move)
    if winMoves != []:
        return random.choice(winMoves)
    elif blockMoves != []:
        return random.choice(blockMoves)
    else:
        return random.choice(validMoves)

# ------------------- Main function --------------------
#Task8: Play a game
def play():
    """This function allows you to play connect 4 using all the functions
    above. The game allows 2 humans, human vs computer or computer 
    """
    print("*"*55)
    print("***"+" "*8+"WELCOME TO JAY'S CONNECT FOUR!"+" "*8+"***")
    print("*"*55,"\n")
    print("Enter the players' names, or type 'C' or 'L',\n")
    print("'C' is for a computer opponent while 'L' loads a saved game. \n")
    player1 = input("What is your name, player 1? ").capitalize()
    #if player1 is called L, load a saved game
    if player1 == "L":
        game = loadGame()
    else:
        if player1 == "C":
            print("Player 1 will be the computer.")
        else:    
            print("Hi, {}!".format(player1))
        player2 = input("What is your name, player 2? ").capitalize()
        if player2 == "C":
            print("Player 2 will be the computer.")
        else:
            print("Hi, {}!".format(player2))
        game = newGame(player1,player2)
    printBoard(game['board'])
    if game['who'] == 1:
        notwho = 2
    elif game['who'] == 2:
        notwho = 1
    while getValidMoves(game['board']) != []:
        validMoves = getValidMoves(game['board'])
        while True:
            #if player is "C", then run suggestMove1
            if getName(game) == "C":
                print("\nPlayer 1 is thinking...")
                move = suggestMove1(game['board'],game['who'])
                break
            else:    
                turn = True
                while turn:
                    try:
                        pm = input("Where would you like to go, {}? ".format(getName(game))).capitalize()
                        if pm == "S":
                            #if the game doesn't save, continue                            
                            try:
                                saveGame(game)
                            except:
                                print("Game cannot be saved.")
                            break
                        #if pm isn't an integer, it asks again
                        move = int(pm) - 1
                    except ValueError:
                        print("That wasn't a valid move.")
                        continue
                    #if move isn't a valid move, it asks again
                    if validMoves.count(move) == 0:
                        print("That wasn't a valid move.")
                    elif validMoves.count(move) == 1:
                        turn = False
                        break
                break
        #if the game was saved, don't make a move
        if getName(game) != "C" and pm == "s":
            pass
        else:    
            makeMove(game['board'],move,game['who'])
        printBoard(game["board"])
        #checking if who has won
        if hasWon(game['board'],game['who']):
            if getName(game) == "C":
                return print("\nPlayer {} has won!".format(game['who']))    
            else:
                return print("\nCongratulations {}, you won!".format(getName(game)))
        #if the game was saved, don't give the turn to the other player
        elif getName(game) != "C" and pm == "s":
            pass
        else:
            (game['who'],notwho)=(notwho,game['who'])
    #if the board is full and nobody has won, print a tie message
    return print("\nCongratulations, you tied.")
    
    
if __name__ == '__main__' or __name__ == 'builtins':
    play()