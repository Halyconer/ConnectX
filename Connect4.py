import random
import numpy as np
from scipy.signal import convolve2d
import time

'''
Connect4 initial game implementation with the goal of implementing a basic minmax-based AI.
At the moment, the player always goes first, and the AI randomly selects a column

Need to work on implementing a scoring system.

Another objective is to have a 6x7x2x2 matrix: layered matricies to evaluate the board state, which will allow for a more sophisticated AI.
'''

class Connect4:
  ROW_COUNT = 6
  COL_COUNT = 7

  def __init__(self):
    self.board = self.create_board()
    self.game_over = False
    self.turn = 0

  def create_board(self):
    return np.zeros((self.ROW_COUNT, self.COL_COUNT))

  def drop_piece(self, row, col, piece):
    self.board[row][col] = piece

  def is_valid(self, col):
    """ Check if the top row of selected column is empty """
    return self.board[self.ROW_COUNT - 1][col] == 0

  def next_open(self, col):
    for row in range(self.ROW_COUNT):
      if self.board[row][col] == 0:
        return row
      
  def score_position(self, piece):
    """ 
    Scoring function to evaluate the board position for a given piece.
    This is a placeholder for future implementation of a scoring system.
    """
    score = 0
    # Implement scoring logic here
    return score

  def win(self, piece):
    """ 
    Checking for a win using 2D convolution. Like a mini neural network 
    It works by sliding each win pattern across the board with scipy's convolve2d function,
    then checking the resulting matrix for any values >= 4, which would indicate a win.

    Note to self:
    Passes work by first converting the board into a binary matrix where the player's pieces are represented as 1s,
    so even if the piece is 2, it is marked as 1 in the convolution check. 
    """
    # Defining the kernels for convolution to check for winning patterns
    win_patterns = [
        np.array([[1, 1, 1, 1]]),  # Horizontal
        np.array([[1], [1], [1], [1]]),  # Vertical
        np.eye(4, dtype=int),  # Positive diagonal
        np.fliplr(np.eye(4, dtype=int)),  # Negative diagonal
    ]
    # Use convolution to check for winning patterns
    player_board = (self.board == piece).astype(int)

    # Create kernels for convolution
    for kernel in win_patterns:
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
                self.turn = (self.turn + 1) % 2  # Switch turns
        else:
            print("Invalid move. Try another column.")
      
      elif self.turn == 1: 
        time.sleep(0.5)
        col = random.randint(0, self.COL_COUNT-1)
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
                self.turn = (self.turn + 1) % 2  # Switch turns
        else:
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
                    self.turn = (self.turn + 1) % 2  # Switch turns

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

# Run the game
if __name__ == "__main__":
    game = Connect4() # Initialize the game
    game.main_game_loop() # Start the main game loop
