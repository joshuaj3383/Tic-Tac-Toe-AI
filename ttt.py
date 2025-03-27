import random

# Prints out the tic tac toe board
def printBoard(board):
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

# Returns whether the space is free to play in
def isFree(sqr):
    return (sqr != "X") and (sqr != "O")

# Returns the next, raises exception
def getNextTurn(turn):
    if turn == "X":
        return "O"
    elif turn == "O":
        return "X"
    else:
        raise Exception("Turn must be 'X' or 'O'")

# Takes in the three numbers and returns if someone won
def rowOfThree(board, *num):
    count = 0

    for i in num:
        if (board[i] == 'X'):
            count += 1
        elif (board[i] == 'O'):
            count -= 1

    if count == 3:
        return 'X'
    elif count == -3:
        return 'O'
    else:
        return "0"

# Returns the winner of a board, 0 if it is continuing
def getWinner(board):
    # Look for a winner along the rows
    for i in range(3):
        res = rowOfThree(board, 3 * i, 3 * i + 1, 3 * i + 2)
        if res != "0":
            return res

    # Look for a winner along the columns
    for i in range(3):
        res = rowOfThree(board, i, i + 3, i + 6)
        if res != "0":
            return res

    # Look for a winner along first diagonal
    res = rowOfThree(board, 0, 4, 8)
    if res != "0":
        return res

    # Look for a winner along second diagonal
    res = rowOfThree(board, 2, 4, 6)
    if res != "0":
        return res

    # There is no winner. If there is an empty square that means the game is
    # still continuing and "0" will be returned
    for i in range(9):
        if board[i] != 'X' and board[i] != 'O':
            return '0'

    # If the game has ended and no one has won it is a tie
    return 'T'


# This function use recursion to calculate the value of a given position
# It is given the current turn of the player as well as the player who
# it is trying to maximize the score
def minimax(board, alpha, beta, maxPlayer, turn):
    # Base case: Returns evaluation of the board
    winner = getWinner(board)
    if (winner == maxPlayer):
        return 1;
    if (winner == getNextTurn(maxPlayer)):
        return -1;
    if (winner == 'T'):
        return 0;
    
    # If it is the turn of maximizing player maximize the score
    if maxPlayer == turn:
        maxEval = -10
        # For each child move
        for i in range(9):
            if isFree(board[i]):
                board[i] = turn
                testEval = minimax(board, alpha, beta, maxPlayer, getNextTurn(turn))
                maxEval = max(maxEval, testEval)
                board[i] = str(i + 1)

                alpha = max(alpha, testEval)
                if (beta <= alpha): 
                    break

        return maxEval
    else:
        minEval = 10

        # For each child move
        for i in range(9):
            if isFree(board[i]):
                board[i] = turn
                testEval = minimax(board, alpha, beta,
                                   maxPlayer, getNextTurn(turn))
                minEval = min(minEval, testEval)
                board[i] = str(i + 1)

                beta = min(beta, testEval)
                if (beta <= alpha):
                    break

        return minEval

# Looks through all possible moves and choses the one with
# the best score
def playBest(board, turn):
    bestMoveList = []
    numMoves = 0;
    bestEval = -100

    # Look through each possible move and find the one with the best score
    for i in range(9):
        if isFree(board[i]):
            board[i] = turn
            testEval = minimax(board, -100, 100, turn, getNextTurn(turn))
            board[i] = str(i + 1)

            if testEval > bestEval:
                bestEval = testEval
                numMoves = 1
                bestMoveList.clear()
                bestMoveList.append(i)
            elif testEval == bestEval:
                numMoves += 1
                bestMoveList.append(i)
                
    if numMoves != 0:
        board[bestMoveList[random.randint(0, numMoves - 1)]] = turn
    else:
        raise Exception("No valid move.")

# Main
board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
turn = input("Do you want to play as X or O (X goes first): ").strip().upper()

while (turn != 'X' and turn != 'O'):
    turn = input("Please enter X or O: ").strip().upper()

if turn == 'O':
    board[random.randint(0, 8)] = 'X'

while (getWinner(board) == '0'):
    # Execute the player's Turn
    printBoard(board)

    userInput = int(input(
        f"It is {turn}'s turn to play. Please enter the square (1-9) to play in: "))

    while (userInput < 1 or userInput > 9 or not isFree(board[userInput - 1])):
        if (userInput < 1 or userInput > 9):
            userInput = int(input("Please enter a valid number (1-9): "))
        else:
            userInput = int(input("Square is taken. Try again: "))

    board[userInput - 1] = turn

    # If the game is still going, AI Plays best move and swap turns
    if (getWinner(board) == '0'):
        turn = getNextTurn(turn)
        playBest(board, turn)
        turn = getNextTurn(turn)

printBoard(board)
print(f"Winner: {getWinner(board)}")
