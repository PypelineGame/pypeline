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
                self.xvel = -6
            else:
                self.xvel = -5
        if right:
            if running:
                self.xvel = 6
            else:
                self.xvel = 5
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
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
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
        # might need to offset camera in y coordinates in the future
        # .. add here

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

class BlankPlatform(Entity):
    """ Generates an invisible 32x32 platform at x,y with a given BlockType """
    def __init__(self, x, y, BlockType):
        Entity.__init__(self)
        self.rect = Rect(x, y, 32, 32)
        self.image = pygame.Surface([32, 32], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
    def update(self):
        pass

class BlockType(Entity):
    """ abstract blocktype class """
    def __init__(self):
        Entity.__init__(self)
    def update(self):
        pass

class BaigeBlock(BlockType):
    """ baigeblock class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/baige_block.png")
    def update(self):
        pass

class BrownBlock(BlockType):
    """ brown block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/brown_block.png")
    def update(self):
        pass

class BlueBlock(BlockType):
    """ blue block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blue_block.png")
    def update(self):
        pass

class BrightBlueBlock(BlockType):
    """ bright blue block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/bright_blue_block.png")
    def update(self):
        pass

class GrayBlock(BlockType):
    """ gray block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/gray_block.png")
    def update(self):
        pass

class TopLeftStoneBlock(BlockType):
    """ top left stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/top_left_brick.png")
    def update(self):
        pass

class TopRightStoneBlock(BlockType):
    """ top right stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/top_right_brick.png")
    def update(self):
        pass

class RightStoneBlock(BlockType):
    """ right stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/right_brick.png")
    def update(self):
        pass

class LeftStoneBlock(BlockType):
    """ left stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/left_brick.png")
    def update(self):
        pass

class CollisionBlock(BlockType):
    """ blank block used to detect collisions """
    def __init__(self):
        BlockType.__init__(self)
    def update(self):
        pass

class Enemy(Entity):
    """ Abstract enemy object """
    def __init__(self):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0

class HitBox(Entity):
    """ hitbox object """
    def __init__(self, x1, y1, x2, y2):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.rect = Rect(x1, y1, x2, y2)

"""                                 Enemies                                 """

class GarbageCollector(Enemy):
    """ GarbageCollector Enemy object """

    def __init__(self, x, y):
        Enemy.__init__(self)
        self.rect = Rect(x, y, 70, 70)
        self.counter = 0 # used for alternating sprite images
        self.frame_counter = 0 # used for counting frame rate

        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.reverse = False

        # establish list of sprite images
        self.images = ['1.png', '2.png', '3.png', '4.png']
        for index, x in enumerate(self.images):
            self.images[index] =  "../sprites/garbage_collector/" + x
        self.image = pygame.image.load(self.images[0]) # start on first image

    def update(self, platforms, blank_platforms, blocks, entities):
        """ update garbage collector """
        self.frame_counter += 1
        if self.frame_counter == GARBAGE_COLLECTOR_MAX_FRAMES:
            self.frame_counter = 0
            self.image = pygame.image.load(self.images[self.counter])
            if self.reverse:
                self.image = transform.flip(self.image, 1, 0)
            self.counter = (self.counter + 1) % len(self.images)

        if not self.reverse:
            self.xvel = 2
        else:
            self.xvel = -2

         # only accelerate with gravity if in the air
        if not self.onGround:
            self.yvel += 0.6 # turn around insted
             # max falling speed
            if self.yvel > 100:
                self.yvel = 100

        # increment in x direction
        self.rect.left += self.xvel

        # do x-axis collision
        self.collide(self.xvel, 0, platforms, blocks, entities)

        # increment in y direction
        self.rect.top += self.yvel
        self.onGround = False;

        # do y-axis collision
        self.collide(0, self.yvel, platforms, blocks, entities)

        # handle collisions for blank collision blocks
        for p in blank_platforms:
            if pygame.sprite.collide_rect(self, p):
                self.reverse = not self.reverse

    def collide(self, xvel, yvel, platforms, blocks, entities):
        """ handles garbage collector collision """
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0: # moving right, hit left side of wall
                    self.rect.right = p.rect.left
                    if p in blocks:
                        p.kill()
                        blocks.remove(p)
                        entities.remove(p)
                        platforms.remove(p)
                if xvel < 0: # moving left, hit right side of wall
                    self.rect.left = p.rect.right
                    if p in blocks:
                        p.kill()
                        blocks.remove(p)
                        entities.remove(p)
                        platforms.remove(p)
                if yvel > 0: # moving down, hit top of wall
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0: # moving up, hit bottom side of wall
                    self.rect.top = p.rect.bottom