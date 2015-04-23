"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) == 0:
            # All tiles in row i to the right of position (i,j) are positioned at their solved location.
            for col in range(target_col + 1, self.get_width()):
                if not (target_row, col) == self.current_position(target_row, col):
                    return False
            # All tiles in rows i+1 or below are positioned at their solved location.
            if not target_row + 1 == self.get_height():
                for col in range(0, self.get_width()):
                    if not (target_row + 1, col) == self.current_position(target_row + 1, col):
                        return False
            return True
        return False

    def move(self, target_row, target_col, row, col):
        """
        Place a tile at the target position
        Returns a move string
        """
        move_str = ''
        
        col_delta = target_col - col
        row_delta = target_row - row
        
        move_str += row_delta * 'u'
        if col_delta == 0:
            move_str += 'ld' + (row_delta - 1) * 'druld'
        else:
            if col_delta > 0:
                move_str += col_delta * 'l'
                if row == 0:
                    move_str += (abs(col_delta) - 1) * 'drrul'
                else:
                    move_str += (abs(col_delta) - 1) * 'urrdl'
            elif col_delta <0:
                move_str += (abs(col_delta) - 1) * 'r'
                if row == 0:
                    move_str += abs(col_delta) * 'rdllu'
                else:
                    move_str += abs(col_delta) * 'rulld'
            move_str += row_delta * 'druld'
        
        return move_str
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        row, col = self.current_position(target_row, target_col)
        move_str = self.move(target_row, target_col, row, col)
        self.update_puzzle(move_str)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        move_str = 'ur'
        self.update_puzzle(move_str)
        row, col = self.current_position(target_row, 0)
        if row == target_row and col == 0:
            step = (self.get_width() - 2) * 'r'
            self.update_puzzle(step)
            move_str += step
        else:
            step = self.move(target_row - 1, 1, row, col)
            step += 'ruldrdlurdluurddlu' + (self.get_width() - 1) * 'r'
            self.update_puzzle(step)
            move_str += step
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.get_number(0, target_col) == 0:
            return False
        for col in range(self.get_width()):
            for row in range(self.get_height()):
                if (row == 0 and col > target_col) or (row == 1 and col >= target_col) or row > 1:
                    if not (row, col) == self.current_position(row, col):
                        return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.lower_row_invariant(1, target_col):
            return False
        for col in range(0, self.get_width()):
            for row in range(2, self.get_height()):
                if not (row, col) == self.current_position(row, col):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_str = 'ld'
        self.update_puzzle(move_str)
        row, col = self.current_position(0, target_col)
        if row == 0 and col == target_col:
            return move_str
        else:
            step = self.move(1, target_col - 1, row, col)
            step += 'urdlurrdluldrruld'
            self.update_puzzle(step)
            move_str += step
        return move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        row, col = self.current_position(1, target_col)
        move_str = self.move(1, target_col, row, col)
        move_str += 'ur'
        self.update_puzzle(move_str)
        return move_str

    ###########################################################
    # Phase three methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_str = ''
        first_step = ''
        
        if self.get_number(1, 1) == 0:
            first_step += 'ul'
            self.update_puzzle(first_step)
            if (0, 1) == self.current_position(0, 1) and (1, 1) == self.current_position(1, 1):
                return first_step
            if self.get_number(0, 1) < self.get_number(1, 0):
                move_str += 'rdlu'
            else:
                move_str += 'drul'
            self.update_puzzle(move_str)
        return first_step + move_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_str = ''
        
        # first put 0 tile in the right lower corner
        row = self.get_height() - 1
        col = self.get_width() - 1
        row_current, col_current = self.current_position(0, 0)
        col_delta = col_current - col
        row_delta = row_current - row
        step = abs(col_delta) * 'r' + abs(row_delta) * 'd'
        self.update_puzzle(step)
        move_str += step
        # bottom m-2 rows in order from bottom to top and right to left
        for dummy_row in range(row, 1, -1):
            for dummy_col in range(col, 0, -1):
                move_str += self.solve_interior_tile(dummy_row, dummy_col)
            move_str += self.solve_col0_tile(dummy_row)
        # rightmost n-2 columns of the top two rows in order from bottom to top and right to left
        for dummy_col in range(col, 1, -1):
            move_str += self.solve_row1_tile(dummy_col)
            move_str += self.solve_row0_tile(dummy_col)
        # finally upper left 2*2 portion
        move_str += self.solve_2x2()
        
        return move_str
        
        

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))



