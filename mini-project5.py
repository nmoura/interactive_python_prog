# implementation of card game - Memory

import simplegui
import random

frame_size = [800, 100]
card_size = [50, 100]
cards_separator = []
card_interval = 0
exposed = []
last_checked_idx = [0, 0, 0]
moves = 0

# helper function to initialize globals
def init():
    global state, numbers, card_interval, exposed, moves, last_checked_idx
    state = 0
    exposed = []
    moves = 0
    last_checked_idx = [0, 0, 0]
    numbers = range(0,8) + range(0,8)
    random.shuffle(numbers)
    label.set_text("Moves = "+ str(moves))
    for n in range(0,16):
        cards_separator.append(card_interval)
        card_interval += card_size[0]
        exposed.append(False)

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, last_checked_idx, moves
    for n in range(0,16):
        if (pos[0] > cards_separator[n]) and (pos[0] < cards_separator[n] + card_size[0]) and pos[0] != cards_separator[n] and pos[0] != cards_separator[n] + 1 and pos[0] != cards_separator[n] + 2:
            if not exposed[n]:
                exposed[n] = True
                last_checked_idx[2] = last_checked_idx[1]
                last_checked_idx[1] = last_checked_idx[0]
                last_checked_idx[0] = n
                if state == 0:
                    state = 1
                elif state == 1:
                    state = 2
                    moves += 1
                    label.set_text("Moves = "+ str(moves))
                else:
                    state = 1
                    if numbers[last_checked_idx[1]] <> numbers[last_checked_idx[2]]:
                        exposed[last_checked_idx[1]] = False
                        exposed[last_checked_idx[2]] = False

# cards are logically 50x100 pixels in size
def draw(canvas):
    global card_interval
    for n in range(0,16):
        card_interval = cards_separator[n]
        canvas.draw_line([card_interval, 0], [card_interval, card_size[1]], 1, "Brown")
        canvas.draw_line([card_interval + card_size[0] / 2, 0], [card_interval + card_size[0] / 2, card_size[1]], 48, "Green")
        if exposed[n]:
            number = str(numbers[n])
            canvas.draw_line([card_interval + card_size[0] / 2, 0], [card_interval + card_size[0] / 2, card_size[1]], 48, "Black")
            canvas.draw_text(number, [card_interval + 15, 60], 36, "White", "sans-serif")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", frame_size[0], frame_size[1])
frame.add_button("Reset", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
