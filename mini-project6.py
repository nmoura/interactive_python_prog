import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
count = 0
attempts = 3
time_count = 0

#constants
angle = math.pi/30 #one turn in second
acc = 7/60 # 10 pxs/sec in sec
dec = .4/60 # 40% in sec 
clock = {simplegui.KEY_MAP["left"] : False, simplegui.KEY_MAP["right"] : True}
av = (-math.pi/15, math.pi/15)
v = (-5, 5)


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

    

debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris3_brown.png")


nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")


splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")


ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")


missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")


asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")


explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")


soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


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
        self.thrusted_image_center = [self.image_center[0] + self.image_size[0],
                                      self.image_center[1]]
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, self.thrusted_image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    def update(self):
        self.vel[0] *= (1-dec)
        self.vel[1] *= (1-dec)
        if self.thrust:
            vector = angle_to_vector(self.angle)
            self.vel[0] += acc * vector[0]
            self.vel[1] += acc * vector[1]
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height
        self.angle += self.angle_vel
    def change_angle_vel(self, is_clock, down):
        if down:
            if is_clock:
                self.angle_vel += angle
            else:
                self.angle_vel -= angle
        else:
            if is_clock:
                self.angle_vel -= angle
            else:
                self.angle_vel += angle
    def thrusters_switch(self):
        self.thrust = not self.thrust
        if self.thrust:
            ship_thrust_sound.play()
            sound.start()
            #ship_thrust_sound.rewind()
        else:
            sound.stop()
            ship_thrust_sound.rewind()
    def shoot(self):
        global a_missile
        vector = angle_to_vector(self.angle)
        start_x = self.pos[0] + self.image_center[0] * vector[0]
        start_y = self.pos[1] + self.image_center[0] * vector[1]
        x_vel = self.vel[0] + math.sqrt(2) * vector[0]
        y_vel = self.vel[1] + math.sqrt(2) * vector[1]
        a_missile = Sprite([start_x, start_y], [x_vel, y_vel], 0, 0, missile_image, missile_info, missile_sound)


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
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % width
        self.angle += self.angle_vel

           
def draw(canvas):
    global time_count
    
    
    time_count += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime_count = (time_count / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime_count, center[1]], [size[0]-2*wtime_count, size[1]], 
                                [width/2+1.25*wtime_count, height/2], [width-2.5*wtime_count, height])
    canvas.draw_image(debris_image, [size[0]-wtime_count, center[1]], [2*wtime_count, size[1]], 
                                [1.25*wtime_count, height/2], [2.5*wtime_count, height])

    
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    
    
    canvas.draw_text("attempts", [20, 30], 20, "White")
    canvas.draw_text(str(attempts), [20, 60], 20, "White")
    
    canvas.draw_text("attempts", [720, 30], 20, "White")
    canvas.draw_text(str(attempts), [720, 60], 20, "White")
    
    
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
    
def rock_spawner():
    global a_rock
    x_vel = random.random() * (v[1] - v[0]) + v[0]
    y_vel = random.random() * (v[1] - v[0]) + v[0]
    angle = random.random() * 2 * math.pi
    angle_vel = random.random() * (av[1] - av[0]) + av[0]
    a_rock = Sprite([width * random.random(), height * random.random()], [x_vel, y_vel], angle,angle_vel, asteroid_image, asteroid_info)
    
def sound_restart():
    ship_thrust_sound.rewind()
    ship_thrust_sound.play()
    

def down(key):
    if key in clock.keys():
        my_ship.change_angle_vel(clock[key], True)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters_switch()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def up(key):
    if key in clock.keys():
        my_ship.change_angle_vel(clock[key], False)  
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters_switch()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)


my_ship = Ship([width / 2, height / 2], [0, 0], -math.pi/2, ship_image, ship_info)
a_rock = Sprite([width / 3, height / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * width / 3, 2 * height / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(down)
frame.set_keyup_handler(up)

time_countr = simplegui.create_time_countr(1000.0, rock_spawner)
sound = simplegui.create_time_countr(25000.0, sound_restart)


time_countr.start()
frame.start()
