# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
import random

def number_to_name(number):
    # fill in your code below
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard'
    elif number == 4:
        name = 'scissors'
    else:
        name = 'ERROR: outside number of the permitted range.'
    return name

def name_to_number(name):
    # fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == 'rock':
        number = 0
    elif name == 'Spock':
        number = 1
    elif name == 'paper':
        number = 2
    elif name == 'lizard':
        number = 3
    elif name == 'scissors':
        number = 4
    else:
        number = 'ERROR: not acknowledge name.'
    return number

def rpsls(name): 
    # fill in your code below
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 4, 1)
    # compute difference of player_number and comp_number modulo five
    diff = (player_number - comp_number) % 5
    # use if/elif/else to determine winner
    if diff == 1 or diff == 2:
        winner = 'Player wins!'
    elif diff == 3 or diff == 4:
        winner = 'Computer wins!'
    elif diff == 0:
        winner = 'Player and computer tie!'
    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    print 'Player chooses ' + name
    print 'Computer chooses ' + comp_name
    # print results
    print winner
    print ' '
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
