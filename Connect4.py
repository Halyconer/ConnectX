import numpy as np

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
    return self.board[self.ROW_COUNT - 1][col] == 0

  def next_open(self, col):
    for row in range(self.ROW_COUNT):
      if self.board[row][col] == 0:
        return row

  def win(self, piece):
    # Horizontal check
    for c in range(self.COL_COUNT - 3):
      for r in range(self.ROW_COUNT):
        if all(self.board[r][c+i] == piece for i in range(4)):
          return True

    # Vertical check
    for c in range(self.COL_COUNT):
      for r in range(self.ROW_COUNT - 3):
        if all(self.board[r+i][c] == piece for i in range(4)):
          return True

    # Positive diagonal check
    for c in range(self.COL_COUNT - 3):
      for r in range(self.ROW_COUNT - 3):
        if all(self.board[r+i][c+i] == piece for i in range(4)):
          return True

    # Negative diagonal check
    for c in range(self.COL_COUNT - 3):
      for r in range(3, self.ROW_COUNT):
        if all(self.board[r-i][c+i] == piece for i in range(4)):
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
      self.print_board()
      col = int(input(f"Player {self.turn + 1} make your selection (0-{self.COL_COUNT - 1}): "))

      if self.is_valid(col):
        row = self.next_open(col)
        self.drop_piece(row, col, self.turn + 1)

        if self.win(self.turn + 1):
          self.print_board()
          print(f"Player {self.turn + 1} wins!")
          self.game_over = True
        else:
          self.turn = (self.turn + 1) % 2 # Switch turns
      else:
        print("Invalid move. Try another column.")

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
