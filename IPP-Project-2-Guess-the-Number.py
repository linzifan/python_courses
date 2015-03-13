# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

range_min = 0
range_max = 100

remaining_guess = int(math.ceil(math.log(range_max - range_min + 1, 2)))  

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(range_min, range_max)
    global remaining_guess
    remaining_guess = int(math.ceil(math.log(range_max - range_min + 1, 2)))  
    print " "
    print "New game. Range is from", range_min, "to",  range_max
    print "Number of remaining guesses is", remaining_guess


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range_min, range_max
    range_min = 0
    range_max = 100
    new_game()


def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range_min, range_max
    range_min = 0
    range_max = 1000
    new_game()
    
    
def input_guess(guess):
    # main game logic goes here	
    global remaining_guess
    remaining_guess = remaining_guess - 1
    
    guess = int(guess)
    
    print " "
    print "Guess was", guess
    if secret_number > guess: 
        print "Number of remaining guesses is", remaining_guess
        print "Higher!"
    elif secret_number < guess: 
        print "Number of remaining guesses is", remaining_guess
        print "Lower!"
    else: 
        print "Number of remaining guesses is", remaining_guess
        print "Correct!"
        new_game()

    if remaining_guess <= 0:
        print "You ran out of guesses.  The number was", secret_number
        new_game()

    
# create frame
frame = simplegui.create_frame('Guess the number', 200, 150)


# register event handlers for control elements and start frame
frame.add_button('Range: [0, 100)', range100, 200)
frame.add_button('Range: [0, 1000)', range1000, 200)
frame.add_input('Enter your guess', input_guess, 200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric

