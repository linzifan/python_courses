"""
Monte Carlo Tic-Tac-Toe Player
"""
# http://www.codeskulptor.org/#user39_vKUU4Cwa9N4Xja4.py


import random
import poc_ttt_gui
import poc_ttt_provided as provided


# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 20        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


# Add your functions here.

def mc_trial(board, player):
    """
    This function takes a current board and the next player
    to move. The function plays a game starting with the 
    given player by making random moves, alternating between
    players.
    """
    current_player = player
    # The game will continue until there is no empty cell
    while len(board.get_empty_squares()) >= 1 and board.check_win() == None:
        choice = random.choice(board.get_empty_squares())
        board.move(choice[0], choice[1], current_player)
        current_player = provided.switch_player(current_player)
 


def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) 
    with the same dimensions as the Tic-Tac-Toe board, a 
    board from a completed game, and which player the 
    machine player is. The function scores the completed 
    board and updates the scores grid.
    """
    for row in range(len(scores)):
        for col in range(len(scores[0])):
            if board.check_win() == player:
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER
            elif board.check_win() == provided.switch_player(player):
                if board.square(row, col) == player:
                    scores[row][col] -= SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER



                    
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. 
    The function finds all of the empty squares with the 
    maximum score and randomly return one of them as a (row, column)
    tuple.
    """
    empty_square_scores = []
    best_score = None
    best_empty_squares = []
    
    # find empty squares with their scores
    for square in board.get_empty_squares():
        empty_square_scores.append(scores[square[0]][square[1]])
    best_score = max(empty_square_scores)
    
    for row in range(len(scores)):
        for col in range(len(scores[0])):
            if scores[row][col] == best_score:
                if board.square(row, col) == provided.EMPTY:
                    best_empty_squares.append((row, col))
    
    # return best_move
    return random.choice(best_empty_squares)
    
    
    

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the 
    machine player is, and the number of trials to run. 
    The function uses the Monte Carlo simulation to return
    a move for the machine player in the form of a 
    (row, column) tuple.
    """
    # create score grid
    scores = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())] 

    for dummy_trial in range(trials):
        working_board = board.clone()
        mc_trial(working_board, player)
        mc_update_scores(scores, working_board, player)
    
    return get_best_move(board, scores)
    
    

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)                                   
                                     
                                    