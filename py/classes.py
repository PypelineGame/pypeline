#! /usr/bin/python

# import pygame modules
import pygame
from pygame import *

# import additional python modules
from math import sqrt
from random import randrange
from copy import copy

# Define screen borders
WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
RESET_LEVEL_FLAG = False

PLAYER_STARTER_HEALTH = 200

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Define display and camera flags
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

# Define animation frames for classes
GARBAGE_COLLECTOR_MAX_FRAMES = 8
PYSNAKE_MAX_FRAMES = 8
PLAYER_DAMAGE_FRAMES = 20

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
        self.xvel = 0 # current x velocity
        self.yvel = 0 # current y velocity
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image_copy = self.image.copy()
        self.transparent_image = pygame.Surface([32, 32], pygame.SRCALPHA, 32)
        self.transparent_image = self.transparent_image.convert_alpha()
        self.image.convert()
        self.rect = Rect(x, y, 31.5, 31.5)
        self.height = 32
        self.health = PLAYER_STARTER_HEALTH
        self.melee_attack = 25
        self.range_attack = 50
        self.num_of_bullets = 10
        self.damage_frame = 0 # counts # of frames until max damage frames
        self.enemy_collision = False
        self.knockback_left = False
        self.knockback_right = False
        self.flicker = False

    def damage(self, attack, enemy, camera):
        """ performs damage reduction on player's HP upon enemy collision """
        if self.damage_frame >= PLAYER_DAMAGE_FRAMES:
            self.damage_frame = 0 # resets damage frame counter
            self.health -= attack
            if self.yvel >= 0:
                self.yvel -= 10 # causes player to jump if player is on ground
                self.onGround = False
            self.flicker = True # causes player to flicker

    def update(self, up, down, left, right, running, platforms, enemies, enemy_sprites, bullets, camera, collision_blocks):
        """ updates the player on every frame of main game loop """
        self.damage_frame += 1 # increments damage_frame every frame of game

        # flicker player when player is knocked back
        if self.flicker:
            if self.image is self.transparent_image:
                self.image = self.image_copy
            else:
                self.image = self.transparent_image

        # handle knock back collision
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.enemy_collision = True
                self.damage(enemy.attack, enemy, camera)
                # enable knock-back left or knock-back right
                if self.xvel <= 0: # defaults to knock-back left
                    self.knockback_right = True
                elif self.xvel > 0:
                    self.knockback_left = True

        # perform knock back collision
        if self.enemy_collision == True:
            if self.knockback_left:
                self.xvel = -8
            if self.knockback_right:
                self.xvel = 8
            # end knock back once we reach specified frames
            if PLAYER_DAMAGE_FRAMES <= self.damage_frame:
                self.enemy_collision = False
                self.knockback_left = False
                self.knockback_right = False
                self.flicker = False
                self.image = self.image_copy

        # handle player movements
        else:
            if up:
                # only jump if on the ground
                if self.onGround: self.yvel -= 10
            if down:
                pass # we can eventually implement crouching
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
            if not(left or right):
                self.xvel = 0

        # only accelerate with gravity if in the air and no knockback
        if not self.onGround:
            self.yvel += 0.6 # increment falling velocity
            if self.yvel > 100:
                self.yvel = 100 # max falling speed

        self.rect.left += self.xvel # Modifies player's position in X direction

        """ x collision is currently commented out; not sure why its bugging out? """
        #self.collide(self.xvel, 0, platforms) # do x-axis collisions

        self.rect.top += self.yvel # Modifies player's position in Y direction
        self.onGround = False; # assuming we're in the air
        self.collide(0, self.yvel, platforms) # do y-axis collisions

        # handles level changing
        for c in collision_blocks:
            if pygame.sprite.collide_rect(self, c):
                if isinstance(c, ExitBlock):
                    RESET_LEVEL_FLAG = True
                    print "NEXT LEVEL"

    def collide(self, xvel, yvel, platforms):
        """ handles platform collision for player """
        for p in platforms:
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                    self.onGround = True
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
        # SRC ALPHA BUG IS PROBABLY HERE ^^^
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
        self.image = pygame.image.load("../sprites/blocks/baige_block.png")
    def update(self):
        pass

class BrownBlock(BlockType):
    """ brown block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/brown_block.png")
    def update(self):
        pass

class BlueBlock(BlockType):
    """ blue block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/blue_block.png")
    def update(self):
        pass

class BrightBlueBlock(BlockType):
    """ bright blue block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/bright_blue_block.png")
    def update(self):
        pass

class GrayBlock(BlockType):
    """ gray block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/gray_block.png")
    def update(self):
        pass

class TopLeftStoneBlock(BlockType):
    """ top left stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/top_left_brick.png")
    def update(self):
        pass

class TopRightStoneBlock(BlockType):
    """ top right stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/top_right_brick.png")
    def update(self):
        pass

class RightStoneBlock(BlockType):
    """ right stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/right_brick.png")
    def update(self):
        pass

class LeftStoneBlock(BlockType):
    """ left stone block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load("../sprites/blocks/left_brick.png")
    def update(self):
        pass

class CollisionBlock(BlockType):
    """ blank block used to detect collisions """
    def __init__(self):
        BlockType.__init__(self)
    def update(self):
        pass

class ExitBlock(BlockType):
    """ invisible block used to detect level endings """
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
        self.attack = 0

"""                                 Enemies                                 """

class GarbageCollector(Enemy):
    """ GarbageCollector Enemy object """

    def __init__(self, x, y):
        Enemy.__init__(self)
        self.rect = Rect(x, y, 69.5, 69.5)
        self.counter = 0 # used for alternating sprite images
        self.frame_counter = 0 # used for counting frame rate

        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.reverse = False
        self.attack = 10

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
            self.yvel += 0.4 # increase falling distance
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

					
					
class PySnake(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self)
        self.rect = Rect(x, y, 85, 70)
        self.counter = 0 # used for alternating sprite images
        self.frame_counter = 0 # used for counting frame rate

        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.reverse = False
        self.attack = 25
        self.health = 100

        # establish list of sprite images
        self.images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png', '11.png', '12.png']
        for index, x in enumerate(self.images):
            self.images[index] =  "../sprites/PySnake/green_snake/" + x
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
            self.xvel = -2
        else:
            self.xvel = 2

         # only accelerate with gravity if in the air
        if not self.onGround:
            self.yvel += 0.4 # increase falling distance
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
        """ handles PySnake collision """
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0: # moving right, hit left side of wall
                    self.rect.right = p.rect.left
                    if p in blocks:
                        pass
                if xvel < 0: # moving left, hit right side of wall
                    self.rect.left = p.rect.right
                    if p in blocks:
                        pass
                if yvel > 0: # moving down, hit top of wall
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0: # moving up, hit bottom side of wall
                    self.rect.top = p.rect.bottom

"""                              end of Enemies                              """