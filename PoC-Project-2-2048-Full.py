"""
Clone of 2048 game.
"""
# http://www.codeskulptor.org/#user39_yzeUhKU7HHXunxt_1.py


import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    def put_zero(lst):
        """
        Put all non-zero tiles towards the beginning of list.
        """
        lstb = []
        for dummy_i in range(0,len(lst)):
            if lst[dummy_i]!=0: 
                lstb.append(lst[dummy_i])
        if len(lstb)<len(lst):
            lstb.extend([0]*(len(lst)-len(lstb)))
        return lstb


    def combine_pair(lst):
        """
        Combine pairs of tiles.
        """
        for dummy_i in range(0,len(lst)-1):
            if lst[dummy_i]==lst[dummy_i+1]:
                lst[dummy_i] = lst[dummy_i]*2
                lst[dummy_i+1] = 0
        return lst

    list_1 = put_zero(line)
    list_2 = combine_pair(list_1)
    list_3 = put_zero(list_2)
    return list_3


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._intial_tiles = {UP: [(0, dummy_i) for dummy_i in range(grid_width)],
                               DOWN: [(grid_height-1, dummy_i) for dummy_i in range(grid_width)],
                               LEFT: [(dummy_i, 0) for dummy_i in range(grid_height)],
                               RIGHT: [(dummy_i, grid_width-1) for dummy_i in range(grid_height)],
                             }
        self.reset()

        

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[ 0 for dummy_col in range(self._grid_width)] 
                      for dummy_row in range(self._grid_height)]
        if self.count_empty() > 0:
            self.new_tile()
        if self.count_empty() > 0:
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)

    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == 1 or direction == 2:
            for temp_start in self._intial_tiles[direction]:
                temp_list = []
                for dummy_i in range(0, self._grid_height):
                    temp_row = temp_start[0] + OFFSETS[direction][0]*dummy_i
                    temp_col = temp_start[1] + OFFSETS[direction][1]*dummy_i
                    temp_list.append(self.get_tile(temp_row, temp_col))
               
                list_res = merge(temp_list)
                for dummy_i in range(0, self._grid_height):
                    temp_row = temp_start[0] + OFFSETS[direction][0]*dummy_i
                    temp_col = temp_start[1] + OFFSETS[direction][1]*dummy_i
                    self.set_tile(temp_row, temp_col, list_res[dummy_i])
        else:
            for temp_start in self._intial_tiles[direction]:
                temp_list = []
                for dummy_i in range(0, self._grid_width):
                    temp_row = temp_start[0] + OFFSETS[direction][0]*dummy_i
                    temp_col = temp_start[1] + OFFSETS[direction][1]*dummy_i
                    temp_list.append(self.get_tile(temp_row, temp_col))
               
                list_res = merge(temp_list)
                for dummy_i in range(0, self._grid_width):
                    temp_row = temp_start[0] + OFFSETS[direction][0]*dummy_i
                    temp_col = temp_start[1] + OFFSETS[direction][1]*dummy_i
                    self.set_tile(temp_row, temp_col, list_res[dummy_i])            
        if self.count_empty() > 0:
            self.new_tile()
        
        
    def count_empty(self):
        """
        Conunt empty cells before create a new tile
        """
        zero_count = 0
        for dummy_i in range(0, self._grid_height):
            for dummy_j in range(0, self._grid_width):
                if self._grid[dummy_i][dummy_j] == 0:
                    zero_count = zero_count + 1
        return zero_count
        
        
        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """   
        random_row = random.randrange(0, self._grid_height)
        random_col = random.randrange(0, self._grid_width)
        if self._grid[random_row][random_col] == 0 :
            if int(random.random() * 100) < 90:
                self.set_tile(random_row, random_col, 2)
            else:
                self.set_tile(random_row, random_col, 4)
        else: self.new_tile()


    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
