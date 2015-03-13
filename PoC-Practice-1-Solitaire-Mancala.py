"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self.board = []
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self.board = configuration[:]
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        return str(self.board[::-1])
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self.board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        return sum(self.board[1:]) == 0
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        return self.board[house_num] == house_num and house_num != 0

    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):
            # adding +1 to each position lying in front of (and excluding) house_num
            for position in xrange(len(self.board[:house_num])):
                self.board[position] += 1
            # current house (house_num) is then emptied
            self.board[house_num] = 0
        else:
            print 'This is an illegal move!'

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        index = 0
        # checking through each position backwards just to arrive at closest one
        for num in range(len(self.board))[::-1]:
            if self.is_legal_move(num):
                index = num
        return index
    
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        legal_moves = []
        # game isn't won yet and there is still at least one legal move
        while not self.is_game_won() and self.choose_move() != 0:
            # make a note of and apply every possible move suggested
            legal_moves.append(self.choose_move())
            self.apply_move(self.choose_move())
        return legal_moves
 

# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1)   
    
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]

    # add more tests here
    
test_mancala()


# Import GUI code once you feel your code is correct
# import poc_mancala_gui
# poc_mancala_gui.run_gui(SolitaireMancala())

