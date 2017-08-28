# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
num_range = 100
random_number = random.randrange(0,num_range)

# define event handlers for control panel
def init():
    global random_number
    random_number = random.randrange(0,num_range)
    global max_tries
    max_tries = math.ceil(math.log(num_range,2))
    print "New game. Range is from 0 to", str(num_range) + "."
    print "Number of remaining guesses is", str(max_tries) + "."

def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    print ""
    init()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range = 1000
    print ""
    init()
    
def get_input(guess):
    # main game logic goes here
    print ""
    print "Guess was", guess + "."
    guess = int(guess)
    global max_tries
    max_tries -= 1
    if (guess == random_number):
        print "Correct!"
        print ""
        init()
    elif (guess < random_number):
        print "Higher!"
        print "Number of remaining guesses is", str(max_tries) + "."
    elif (guess > random_number):
        print "Lower!"
        print "Number of remaining guesses is", str(max_tries) + "."
    if max_tries == 0:
        print "You ran out of guesses. The number was", str(random_number) + "."
        print ""
        init()

# create frame
frame = simplegui.create_frame("Guess the number", 150, 180)

# register event handlers for control elements
frame.add_button("Range is [0,100)", range100, 150)
frame.add_button("Range is [0,1000)", range1000, 150)
frame.add_label("")
frame.add_input("Enter a guess:", get_input, 150)

# start frame
frame.start()
init()

# always remember to check your completed program against the grading rubric
