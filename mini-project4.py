# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
paddle1_vel = 0.0
paddle2_vel = 0.0
player1_pts = 0
player2_pts = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0, 0]
    if right:
        ball_vel[0] = random.randrange(120, 240) / 60
        ball_vel[1] = random.choice([random.randrange(60,180), random.randrange(-180, -60)]) / 100
    else:
        ball_vel[0] = - random.randrange(120, 240) / 60
        ball_vel[1] = random.choice([random.randrange(60,180), random.randrange(-180, -60)]) / 100

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global player1_pts, player2_pts  # these are ints
    paddle1_pos = HEIGHT/2 - PAD_HEIGHT/2
    paddle2_pos = HEIGHT/2 - PAD_HEIGHT/2
    paddle1_vel = 0.0
    paddle1_vel = 0.0
    player1_pts = 0
    player2_pts = 0
    side=random.choice([True,False])
    ball_init(side)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, player1_pts, player2_pts
 
    # update paddle's vertical position, keep paddle on the screen
    if not paddle1_pos + paddle1_vel <= 0 and not paddle1_pos + paddle1_vel >= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    elif paddle1_pos + paddle1_vel <= 0:
        paddle1_pos=0
    elif paddle1_pos + paddle1_vel >= HEIGHT - PAD_HEIGHT:
        paddle1_pos=HEIGHT - PAD_HEIGHT

    if not paddle2_pos + paddle2_vel <= 0 and not paddle2_pos + paddle2_vel >= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    elif paddle2_pos + paddle2_vel <= 0:
        paddle2_pos=0
    elif paddle2_pos + paddle2_vel >= HEIGHT - PAD_HEIGHT:
        paddle2_pos=HEIGHT - PAD_HEIGHT

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # draw paddles
    c.draw_line([HALF_PAD_WIDTH+1, paddle1_pos], [HALF_PAD_WIDTH+1, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "White")
    c.draw_line([600 - HALF_PAD_WIDTH - 1, paddle2_pos], [600 - HALF_PAD_WIDTH - 1, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[1] <= BALL_RADIUS or (ball_pos[1] + BALL_RADIUS) >= HEIGHT:
        ball_vel[1] = - ball_vel[1]

    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= (paddle1_pos + PAD_HEIGHT):
            ball_vel[0] = - (ball_vel[0] + ball_vel[0] * 0.10)
        else:
            player2_pts += 1
            ball_init(True)

    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= (paddle2_pos + PAD_HEIGHT):
            ball_vel[0] = - (ball_vel[0] + ball_vel[0] * 0.10)
        else:
            player1_pts += 1
            ball_init(False)

    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(player1_pts), (WIDTH / 4, 60), 36, "White", "sans-serif")
    c.draw_text(str(player2_pts), (WIDTH * 0.75, 60), 36, "White", "sans-serif")

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 4
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 4
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 4

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += 4
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= 4
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel += 4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= 4

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game, 120)

# start frame
frame.start()

new_game()
