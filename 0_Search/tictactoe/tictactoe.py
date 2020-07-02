"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    X gets the first move (in the initial game state).
    If game over, any return value is acceptable.

    Agrs:
        board: a board state.
    Returns:
        which player's turn it is (either X or O)
    """
    X_count = sum([row.count("X") for row in board])
    O_count = sum([row.count("O") for row in board])

    if X_count > O_count:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Possible moves: any cells that do not have X or O.
    If game over, any return value is acceptable.

    Args:
        board: a board state.

    Returns:
        set of (i, j):  i = 0, 1, 2 corresponds to the row of the move.
                        j = 0, 1, 2 corresponds to the cell in the row.
    """
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                actions.add((i, j))

    if len(actions) == 0:
        actions.add(None)

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Do not modify the original board. Might want to use a deep copy of input board.
    More on deep copy: https://docs.python.org/3/library/copy.html#copy.deepcopy
    If action is not valid, raise an exception.

    Args:
        board: a board state.
        action: action to be taken on the board state.

    Returns:
        a new board state.
    """
    valid_actions = actions(board)

    if action not in valid_actions:
        raise Exception("Invalid action.")
    
    board_copy = copy.deepcopy(board)
    current_player = player(board)

    board_copy[action[0]][action[1]] = current_player
    
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.

    Args:
        board: a board state.
    
    Returns:
        the winner (X or O) or None if no winner.
    """
    # Check horizontally
    for i in range(3):
        if board[i][0] != None:
            if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
                return board[i][0]
    
    # Check vertically
    for j in range(3):
        if board[0][j] != None:
            if board[0][j] == board[1][j] and board[1][j] == board[2][j]:
                return board[0][j]
    
    # Check diagonally (left to right)
    if board[0][0] != None:
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
    
    # Check diagonally (right to left)
    if board[0][2] != None:
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]
    
    # If no winner is found, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    Args:
        board: a board state.
    
    Returns:
        whether the game is over (boolean):
            True: a winner is found or all cells are filled without a winner.
            False: game still in progress.
    """
    if sum([row.count(EMPTY) for row in board]) != 0 and winner(board) == None:
        return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Input board is assumed to be terminal.

    Args:
        board: a terminal board state.

    Returns:
        utility of the board:
    """
    winner_of_game = winner(board)

    if winner_of_game == X:
        return 1
    elif winner_of_game == O:
        return -1
    else:
        return 0


def max_value(board, alpha, beta):
    """
    Returns the maximum value of a given board state.

    Args:
        board: a board state.
        alpha: the best value that we can have at the current level for max
        beta: the best value that we can have at the current level for min

    Returns:
        the maximum value.
    """
    if terminal(board):
        return utility(board)
    
    value = -math.inf

    for action in actions(board):
        value = max(value, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, value)

        if beta <= alpha:
            break

    return value


def min_value(board, alpha, beta):
    """
    Returns the minimum value of a given board state.

    Args:
        board: a board state.
        alpha: the best value that we can have at the current level for max
        beta: the best value that we can have at the current level for min

    Returns:
        the minimum value.
    """
    if terminal(board):
        return utility(board)

    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action), alpha, beta))
        beta = min(beta, value)

        if alpha >= beta:
            break

    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    If input board is terminal, return None.

    Args:
        board: a board state.
    
    Returns:
        (i, j): optimal move for the current player.
    """
    if terminal(board):
        return None

    current_player = player(board)
    optimal_move = None
    alpha = -math.inf
    beta = math.inf

    if current_player == X:
        value = -math.inf
        for action in actions(board):
            max_v = min_value(result(board, action), alpha, beta)
            alpha = max(value, max_v)
            if max_v > value:
                value = max_v
                optimal_move = action
    
    else:
        value = math.inf
        for action in actions(board):
            min_v = max_value(result(board, action), alpha, beta)
            beta = min(value, min_v)
            if min_v < value:
                value = min_v
                optimal_move = action
    
    return optimal_move