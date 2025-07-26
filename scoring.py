import random
import copy
import numpy as np  

def minimax(board: np.ndarray, depth: int, maximizing_player: bool) -> tuple:
    '''
    Remember how minimax works: The algorithm recursively explores all possible moves up to a certain depth. It picks a maximizing move, 
    then it assumes the opponent will pick the minimizing move, and so on. The depth is a limit to how many moves ahead the algorithm will look.

    The algorithm will then return a score of the board state for the maximizing player. If the maximizing player is the AI, it will return a positive score for a win,
    a negative score for a loss, and 0 for a draw. 
    '''
    valid_positions = get_valid_moves(board)

    if is_terminal_node(board) or depth == 0:
        if is_terminal_node(board):
            if board.win(2):
                return (None, float('inf'))
            elif board.win(1):
                return (None, float('-inf'))
            else:
                return (None, 0)  # Game is a draw
        else:  # Depth limit reached
            return (None, board.score_position(2) if maximizing_player else board.score_position(1)) # board.score_position should return a score based on the current board state for the given piece.
         # the number it returns will be used to 

    if maximizing_player:
        column = random.choice(valid_positions) # select a random column as a placeholder
        max_eval = float('-inf')

        for col in valid_positions: 
            row = board.next_open(col)
            board_copy = board.board.deepcopy()
            board_copy.drop_piece(row, col, 2)  # AI's piece
            
            new_eval = minimax(board_copy, depth - 1, False)[1]

            if new_eval > max_eval:
                max_eval = new_eval
                column = col

        return column, max_eval # final return statement

    else:  # Minimizing player's turn
        min_eval = float('inf')
        column = random.choice(valid_positions)

        for col in valid_positions:
            row = board.next_open(col)
            board_copy = board.board.deepcopy()
            board_copy.drop_piece(row, col, 1)  # Player's piece

            new_eval = minimax(board_copy, depth - 1, True)[1]

            if new_eval < min_eval:
                min_eval = new_eval
                column = col

        return column, min_eval # final return statement

def is_terminal_node(board):
    return board.win(1) or board.win(2) or len(get_valid_moves(board)) == 0

def get_valid_moves(board):
    return [c for c in range(board.COL_COUNT) if board.board[board.ROW_COUNT - 1][c] == 0]
