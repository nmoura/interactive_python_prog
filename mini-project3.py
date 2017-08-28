# template for "Stopwatch: The Game"

import simplegui

# define global variables
interval=100
integer=0
stops=0
win_stops=0
tenths=0
on=False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    division = t / 600
    minutes = int(division)
    seconds = int((division - int(division)) * 60)
    if seconds < 10:
        seconds = '0' + str(seconds)
    global tenths
    tenths = t % 10
    return str(minutes) + ":" + str(seconds) + "." + str(tenths)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global on
    if not(timer.is_running()):
        timer.start()
        on=True

def stop():
    global on, stops, win_stops
    if on:
        timer.stop()
        on=False
        stops += 1
        if (integer % 10) == 0:
            win_stops += 1

def reset():
    global integer, stops, win_stops, seconds, tenths
    if timer.is_running():
        timer.stop()
    integer = 0
    stops=0
    win_stops=0
    tenths=0

# define event handler for timer with 0.1 sec interval
def update():
    global integer
    integer += 1

# define draw handler
def draw(canvas):
    str_integer = format(integer)
    global stops, win_stops
    result = str(win_stops) + "/" + str(stops)
    canvas.draw_text(str_integer, [70, 130], 45, "White", "sans-serif")
    canvas.draw_text(result, (180, 50), 24, "Green", "sans-serif")

# create frame and timer
frame = simplegui.create_frame("Stopwatch: The Game", 250, 250)
timer = simplegui.create_timer(100, update)
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)

# register event handlers
frame.set_draw_handler(draw)

# start frame
frame.start()
