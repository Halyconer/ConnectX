import random
import numpy as np
from scipy.signal import convolve2d
import time
from scoring import minimax

'''
Connect4 initial game implementation with the goal of implementing a basic minmax-based AI.
At the moment, the player always goes first, and the AI randomly selects a column.

Another objective is to have a 6x7x2x2 matrix: layered matricies to evaluate the board state, which will allow for a more sophisticated AI.

To do list:
1. Move all scoring logic to scoring.py
2. Fix magic number issue

Notes:
- drop_piece method is kind of redundant, although it might be more efficient because it allows for a single method to handle the piece dropping logic. Need to 
make sure that it is implemented because some methods just use array assignment.
- Currently board references are very confusing as to when the numpy array or the Connect4 object is being referenced.
'''

class Connect4:
  ROW_COUNT = 6
  COL_COUNT = 7

  # For now Kernels should be consistent
  KERNELS = [
    np.array([[1, 1, 1, 1]]),  # Horizontal
    np.array([[1], [1], [1], [1]]),  # Vertical
    np.eye(4, dtype=int),  # Positive diagonal
    np.fliplr(np.eye(4, dtype=int)),  # Negative diagonal
  ]

  def __init__(self):
    self.board = self.create_board()
    self.game_over = False
    self.turn = 0
    self.valid_cols = [c for c in range(self.COL_COUNT)] 

  def create_board(self):
    return np.zeros((self.ROW_COUNT, self.COL_COUNT))

  def drop_piece(self, row, col, piece):
    self.board[row][col] = piece

  def is_valid(self, col):
    self.valid_cols = [c for c in range(self.COL_COUNT) if self.board[self.ROW_COUNT - 1][c] == 0] # Changed this implemntation to dynamically update alongside the AI
    return col in self.valid_cols # Will return True if the column is valid, otherwise False

  def next_open(self, col):
    for row in range(self.ROW_COUNT):
      if self.board[row][col] == 0:
        return row
      
  def score_position(self, piece):
    """ 
    Scoring function to evaluate the board position for a given piece.

    Next objective:
    Obviously improve the scoring logic.
    But ultimately, we want to use a convolutional neural network to evaluate the board state. This is because
    a CNN can learn to recognize patterns in the board state that lead to winning moves. Need to do research on how to implement this,
    and if we will maintain a minmax-based AI.
    """
    score = 0

    # Scoring Center Column because it is the most important column
    center_col = [int(i) for i in board[:, self.COL_COUNT // 2]] # a single column from the board at the moment
    center_count = center_col.count(piece) # Count the number of (AI) pieces in the center column
    score += 5 * center_count # So the more pieces in the center column, the higher the score

    # Scoring Horizontal
    for r in range(self.ROW_COUNT):
       for c in range(self.COL_COUNT - 3):
          window = [int(self.board[r][c+i]) for i in range(4)]
          score += self.window_score(window, piece)

    # Scoring Vertical
    for c in range(self.COL_COUNT):
        for r in range(self.ROW_COUNT - 3):
            window = [int(self.board[r+i][c]) for i in range(4)]
            score += self.window_score(window, piece)

    # Scoring Positive Diagonal
    for r in range(self.ROW_COUNT - 3):
        for c in range(self.COL_COUNT - 3):
            window = [int(self.board[r+i][c+i]) for i in range(4)]
            score += self.window_score(window, piece)

    # Scoring Negative Diagonal
    for r in range(3, self.ROW_COUNT):
        for c in range(self.COL_COUNT - 3):
            window = [int(self.board[r-i][c+i]) for i in range(4)]
            score += self.window_score(window, piece)

    return score
  
  def window_score(self, window, piece):
     """
     Works by evaluating a 4-piece window in the board.
     It will return a score based on the number of pieces in the window.
     If a potential drop allows for an opponent win, it will return a negative score.
     If a potential drop allows for a win, it will return a positive score.

     Remember that the scoring logic is not here, but in the score_position function.
     This is just a helper function to evaluate a 4-piece window.

     Basically game theory.

     Need to figure out a better negative scoring system.
     """

     # Just check if the piece is 1 or 2, and set the opponent accordingly. If piece is set to 2, then this is the AI, and the opponent is 1.
     if piece == 1:
         opponent = 2
     else:
         opponent = 1

     # AI threat scoring
     if window.count(piece) == 4:
        return 100
     elif window.count(piece) == 3 and window.count(0) == 1:
        return 10
     elif window.count(piece) == 2 and window.count(0) == 2:
        return 5
     
     # Player threat scoring
     if window.count(opponent) == 3 and window.count(0) == 1:
        return -80  
     
     return 0

  def win(self, piece):
    """ 
    Checking for a win using 2D convolution. Like a mini neural network 
    It works by sliding each win pattern across the board with scipy's convolve2d function,
    then checking the resulting matrix for any values >= 4, which would indicate a win.

    Note to self:
    Passes work by first converting the board into a binary matrix where the player's pieces are represented as 1s,
    so even if the piece is 2, it is marked as 1 in the convolution check. 
    """
    # Use convolution to check for winning patterns
    player_board = (self.board == piece).astype(int)

    # Create kernels for convolution
    for kernel in self.KERNELS:
      overlap = convolve2d(player_board, kernel, mode='valid')
      if np.any(overlap >= 4):
        return True
    return False

  def print_board(self):
    print(np.flip(self.board, 0))

  def reset_game(self):
    self.board = self.create_board()
    self.game_over = False
    self.turn = 0

  def play(self):
    while not self.game_over:
      if self.turn == 0:
        self.print_board()
        col = int(input(f"Make your selection (0-{self.COL_COUNT - 1}): "))

        if self.is_valid(col):
            row = self.next_open(col)
            self.drop_piece(row, col, self.turn + 1)
            if self.win(self.turn + 1):
                self.print_board()
                print(f"You win!")
                self.game_over = True
            else:
                self.turn = (self.turn + 1) % 2  
        else:
            print("Invalid move. Try another column.")
      
      # AI decision making
      elif self.turn == 1: 
        time.sleep(0.1)
        col = minimax(self.board, 2, True)[0]  # AI selects a column using minimax algorithm
        print(f"AI is making a move...")
        time.sleep(0.5)
        print(f"AI selects column {col}")

        if self.is_valid(col):
            row = self.next_open(col)
            self.drop_piece(row, col, self.turn + 1)
            if self.win(self.turn + 1):
                self.print_board()
                print(f"AI wins!")
                self.game_over = True
            else:
                self.turn = (self.turn + 1) % 2 

        else: # If the AI selects an invalid column, it will randomly select a valid column
            valid_cols = [c for c in range(self.COL_COUNT) if self.is_valid(c)] # Get all valid columns
            if valid_cols: # If there are valid columns, AI will pick one
                col = random.choice(valid_cols)
                row = self.next_open(col)
                self.drop_piece(row, col, self.turn + 1)
                if self.win(self.turn + 1):
                    self.print_board()
                    print(f"AI wins!")
                    self.game_over = True
                else:
                    self.turn = (self.turn + 1) % 2 

  def main_game_loop(self):
    """Main game loop that handles multiple games"""
    while True:
      self.play()
      print("Would you like to play again? (yes/no)")
      if input().lower() != "yes":
        print("Thanks for playing!")
        break
      else:
        self.reset_game()

'''
Note to self:
A main game loop is implemented to allow players to play more than one game without restarting the program and without
a recursive function call that could lead to a stack overflow.
'''

if __name__ == "__main__":
    game = Connect4() # Initialize the game
    game.main_game_loop() # Start the main game loop
