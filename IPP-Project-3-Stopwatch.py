# template for "Stopwatch: The Game"
import time
import simplegui


# define global variables
global current, game, win
current = 0
game = 0
win = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    return str((t//600))+':'+str((t%600)//100)+str((t%600)//10%10)+'.'+str((t%600)%10)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()

def stop_handler():
    global game, win
    if timer.is_running() == True:
        game += 1
        if (current%600)%10 == 0:
            win += 1
    timer.stop()
    
def reset_handler():
    global current, game, win
    current = 0
    game = 0
    win = 0
    if timer.is_running() == True:
        timer.stop()


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global current, game, win
    current +=1
    # stopwatch only works correctly up to 10 minutes
    # beyond that stopwatch will reset
    if current > 6000:
        current = 0
        game = 0
        win = 0
        timer.stop()


# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(current), (45, 70), 40, "Red")
    canvas.draw_text(str(win)+'/'+str(game), (160, 30), 20, "White")


# create frame
frame = simplegui.create_frame('Stopwatch', 200, 150)


# register event handlers
timer = simplegui.create_timer(100, timer_handler)

start = frame.add_button("Start", start_handler, 60)
stop = frame.add_button("Stop", stop_handler, 60)
reset = frame.add_button("Reset", reset_handler, 60)

frame.set_draw_handler(draw_handler)


# start frame
frame.start()


# Please remember to review the grading rubric

