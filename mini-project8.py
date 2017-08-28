# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 0
time = 0.5
keys = {"left" : False, "right" : False, "up" : False, "space" : False}
key_names = keys.keys()
collisions = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50, 4)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# to try to implement later, a ship explosion when it collides with a rock
# maybe, in the future, try to change too from rocks to asteroids tumbling, like showed in Joe's class.
#ship_explosion_info = ImageInfo([50, 50], [100, 100], 17, 24, True)
#ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
#ship_explosion_center = [50, 50]
#ship_explosion_size = [100, 100]
#ship_explosion_dim = [9, 9]

# animated ship explosion
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_center = [64, 64]
explosion_size = [128, 128]
explosion_dim = 24

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
evillaugh_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/Evillaugh.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] * 3, self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
#            ship_explosion_index = [self.age % ship_explosion_dim[0], (self.age // ship_explosion_dim[0])
#                                    % ship_explosion_dim[1]]
#            canvas.draw_image(ship_explosion_image, 
#                    [ship_explosion_center[0] + ship_explosion_index[0] * ship_explosion_size[0], 
#                     ship_explosion_center[1] + ship_explosion_index[1] * ship_explosion_size[1]], 
#                     ship_explosion_size, ship_explosion_center, ship_explosion_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()

    def update(self):
        global vector
        if keys["left"]:
            self.angle_vel -= 0.1
        elif keys["right"]:
            self.angle_vel += 0.1
        if keys["up"]:
            self.thrust = True
        elif not keys["up"]:
            self.thrust = False
        self.angle = self.angle_vel
        vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += vector[0] * 0.05
            self.vel[1] += vector[1] * 0.05
        else:
            if self.vel[0] != 0.0:
                self.vel[0] -= self.vel[0] * 0.01
            if self.vel[1] != 0.0:
                self.vel[1] -= self.vel[1] * 0.01

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.pos[0] = self.pos[0] % WIDTH
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.pos[1] = self.pos[1] % HEIGHT

    def shoot(self):
        global a_missile
        missile_sound.play()
        vector = angle_to_vector(self.angle)
        missile_pos = [vector[0] + (self.pos[0] + (vector[0] * self.radius)),
                       vector[1] + (self.pos[1] + (vector[1] * self.radius))]
        missile_vel = [0, 0]
        missile_vel[0] += 2 * vector[0] + self.vel[0]
        missile_vel[1] += 2 * vector[1] + self.vel[1]
        a_missile = Sprite([missile_pos[0], missile_pos[1]], [missile_vel[0],missile_vel[1]], 0, 0,
                           missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.animated == True:
            explosion_index = (self.age % explosion_dim) // 1
            current_explosion_center = [explosion_center[0] + explosion_index * explosion_size[0],
                                        explosion_center[1]]
            canvas.draw_image(explosion_image, current_explosion_center, explosion_size,
                              self.pos, explosion_size)

        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)


    def update(self):
        self.age += 1
        self.angle += self.angle_vel
        vector = angle_to_vector(self.angle)

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.pos[0] = self.pos[0] % WIDTH
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.pos[1] = self.pos[1] % HEIGHT

        if self.age >= self.lifespan:
            return True
        else:
            return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        self_pos = self.get_position()
        self_radius = self.get_radius()
        other_pos = other_object.get_position()
        other_radius = other_object.get_radius()
        
        distance = [absolute_value(self_pos[0] - other_pos[0]),
                    absolute_value(self_pos[1] - other_pos[1])]
        
        if distance[0] < self_radius + other_radius and distance[1] < self_radius + other_radius:
            return True

def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        for item in rock_group:
            rock_group.remove(item)

def draw(canvas):
    global time, lives, score, started

    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
    canvas.draw_text("Lives", (30, 30), 22, "White", "monospace")
    canvas.draw_text(str(lives), (115, 30), 22, "White", "monospace")
    canvas.draw_text("Score", (WIDTH - 120, 30), 22, "White", "monospace")
    canvas.draw_text(str(score), (WIDTH - 30, 30), 22, "White", "monospace")
    
    my_ship.draw(canvas)
    my_ship.update()
    
    if a_missile != None:
        process_sprite_group(missile_group, canvas)
        
    if started:
        process_sprite_group(explosion_group, canvas)
        process_sprite_group(rock_group, canvas)

    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
        if lives == 0:
            started = False
            evillaugh_sound.rewind()
            evillaugh_sound.play()
            for rock in rock_group:
                rock_group.remove(rock)

    if group_group_collide(rock_group, missile_group) > 0:
        score += 1

    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

def keydown(key):
    for i in range(0, len(keys)):
        if key == simplegui.KEY_MAP[key_names[i]]:
            keys[key_names[i]] = True
        if key == simplegui.KEY_MAP["space"]:
            my_ship.shoot()

def keyup(key):
    for i in range(0, len(keys)):
        if key == simplegui.KEY_MAP[key_names[i]]:
            keys[key_names[i]] = False

# timer handler that spawns a rock
def rock_spawner():
    if len(rock_group) <= 11 and started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        rock_radius = 40
        ship_pos = my_ship.get_position()
        ship_radius = my_ship.get_radius()

        distance = [absolute_value(rock_pos[0] - ship_pos[0]),
                    absolute_value(rock_pos[1] - ship_pos[1])]
        
        if not (distance[0] < rock_radius + ship_radius and distance[1] + 2 < rock_radius + ship_radius + 2):
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)

def process_sprite_group(a_set, canvas):
    newset = set([])
    for item in a_set:
        item.draw(canvas)
        if item.update():
            newset.add(item)
        a_set.difference_update(newset)            

def group_collide(group, other_object):
    localgroup = set([])
    collisions = 0
    for element in group:
        if element.collide(other_object):
            localgroup.add(element)
            collisions += 1
            explosion = Sprite(element.pos, element.vel, 0, 0, explosion_image, explosion_info)
            explosion_group.add(explosion)
            explosion_sound.rewind()
            explosion_sound.play()
    group.difference_update(localgroup)
    return collisions

def group_group_collide(group_one, group_two):
    localgroup = set([])
    localgroup2 = set([])
    collisions = 0
    for element in group_one:
        for element2 in group_two:
            if element.collide(element2):
                collisions += 1
                localgroup.add(element)
                localgroup2.add(element2)
                explosion = Sprite(element.pos, element.vel, 0, 0, explosion_image, explosion_info)
                explosion_group.add(explosion)
                explosion_sound.rewind()
                explosion_sound.play()
    group_one.difference_update(localgroup)
    group_two.difference_update(localgroup2)
    return collisions

def absolute_value(value):
    if value < 0:
        return - value
    else:
        return value

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship, sprites, etc.
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
a_missile = None
missile_group = set([])
explosion_group = set([])
soundtrack.play()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
