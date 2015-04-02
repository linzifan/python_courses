# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck, exposed, nTurns, state, cInd1, cInd2
    deck = [x for x in range(8)] * 2
    random.shuffle(deck)
    exposed = [False] * 16
    nTurns = 0
    state = 0
    cInd1, cInd2 = -1, -1
    

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global nTurns, state, cInd1, cInd2
    cardInd = list(pos)[0] // 50
    if not exposed[cardInd]:
        if state == 0:
            cInd1 = cardInd
            exposed[cInd1] = True
            state = 1
        elif state == 1:
            cInd2 = cardInd
            exposed[cInd2] = True
            state = 2
            nTurns += 1
            label.set_text("Turns = " + str(nTurns))
        else:
            if deck[cInd1] != deck[cInd2]:
                exposed[cInd1], exposed[cInd2] = False, False
                cInd1, cInd2 = -1, -1
            cInd1 = cardInd
            exposed[cInd1] = True
            state = 1

            
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Black", "White")
            canvas.draw_text(str(deck[i]), (i*50+15, 65), 50, "Black")
        else:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Black", "Teal")
    label.set_text("Turns = " + str(nTurns))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric