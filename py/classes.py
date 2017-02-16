#! /usr/bin/python

# import pygame modules
import pygame
from pygame import *

# import additional python modules
from math import sqrt
from random import randrange

# Define screen borders
WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define display and camera flags
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

# Define animation frames for classes
GARBAGE_COLLECTOR_MAX_FRAMES = 8

# Define class keywords
GARBAGE_COLLECTOR = "Garbage_Collector"

# import our functions
from functions import *

class Camera(object):
    """ Camera object """
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    """ Player object """
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
        self.height = 32

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if left:
            if running:
                self.xvel = -5
            else:
                self.xvel = -4
        if right:
            if running:
                self.xvel = 5
            else:
                self.xvel = 4
        # only accelerate with gravity if in the air
        if not self.onGround:
            self.yvel += 0.6
             # max falling speed
            if self.yvel > 100:
                self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        """ handles platform collision """
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                #if isinstance(p, ExitBlock):
                #    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    #print "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    #print "collide left"
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, mouse, player, camera_state):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        # calculate center of bullet
        self.center_y = (player[1] - player[2]/2)
        self.center_x = (player[0] - player[2]/2)
        # grab mouse coordinates
        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        self.image = pygame.Surface([4, 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # offset camera state on x coordinates
        self.mouse_x -= camera_state[0]

    def update(self):
        """ Move the bullet. """
        speed = 7
        range = 200
        # generate bullet vector
        distance = [self.mouse_x - self.center_x, self.mouse_y - self.center_y]
        norm = sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * speed, direction[1] * speed]

        self.rect.x += bullet_vector[0]
        self.rect.y += bullet_vector[1]

"""                                 Platforms and Blocks                                 """

class Platform(Entity):
    """ Generates a 32x32 platform at x,y with a given BlockType """
    def __init__(self, x, y, BlockType):
        Entity.__init__(self)
        self.rect = Rect(x, y, 32, 32)
        self.image = BlockType.image
    def update(self):
        pass

class BlockType(Entity):
    """ abstract blocktype class """
    def __init__(self):
        Entity.__init__(self)
    def update(self):
        pass

class MossyBlock(BlockType):
    """ mossyblock class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/mossy_block.png")
    def update(self):
        pass

class BaigeBlock(BlockType):
    """ baigeblock class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/baige_block.png")
    def update(self):
        pass

class BaigeRoundBlock(BlockType):
    """ baige round block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/baige_round_block.png")
    def update(self):
        pass

class Enemy(Entity):
    """ Abstract enemy object """
    def __init__(self):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0

"""                                 Enemies                                 """

class GarbageCollector(Enemy):
    """ GarbageCollector Enemy object """

    def __init__(self, x, y):
        Enemy.__init__(self)
        self.rect = Rect(x, y, 70, 70)

        self.counter = 1 # used for alternating images
        self.frame_counter = 0 # used for counting frame rate

        self.xvel = 0
        self.onGround = False

        # establish list of sprite images
        self.images = ['1.png', '2.png', '3.png', '4.png']
        for index, x in enumerate(self.images):
            self.images[index] =  "../sprites/garbage_collector/" + x
        self.image = pygame.image.load(self.images[0]) # start on first image

    def update(self, platforms):
        """ update garbage collector """
        self.frame_counter += 1
        if self.frame_counter == GARBAGE_COLLECTOR_MAX_FRAMES:
            self.frame_counter = 0
            self.image = pygame.image.load(self.images[self.counter])
            self.counter = (self.counter + 1) % len(self.images)

        self.xvel = 1
        # increment in x and y direction
        self.rect.left += self.xvel
        self.rect.top += self.yvel

         # only accelerate with gravity if in the air
        if not self.onGround:
            self.yvel += 0.6 # turn around insted
             # max falling speed
            if self.yvel > 100:
                self.yvel = 100
        #if not(left or right):
        self.xvel = 0
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(self.xvel, 0, platforms)
        self.collide(self.yvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        """ handles garbage collector collision """
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                #if isinstance(p, ExitBlock):
                #    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    #print "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    #print "collide left"
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom