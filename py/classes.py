#! /usr/bin/python

#import matplotlib.pyplot as plt

# import pygame modules
import pygame
from pygame import *

# import additional python modules
from math import sqrt, hypot, sin, radians
from random import randrange
from copy import copy


#out_of_level()
SPRITES_DIRECTORY = "../assets/sprites/"
MUSIC_DIRECTORY = "../assets/music/"

# Define screen borders
WIN_WIDTH = 800
WIN_HEIGHT = 450 # 400 # 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
RESET_LEVEL_FLAG = False

PLAYER_STARTER_HEALTH = 200
MAX_LIVES = 3

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

POISON = (160,32,240)

# Define display and camera flags
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

# Define animation frames for classes
GARBAGE_COLLECTOR_MAX_FRAMES = 8
MAX_HEALTH_FRAMES = 210
PYSNAKE_MAX_FRAMES = 8
COIN_MAX_FRAMES = 8
PLAYER_DAMAGE_FRAMES = 20
PLAYER_MAX_RUN_FRAMES = 8
PLAYER_MAX_STANDING_FRAMES = 20
PLAYER_MAX_ATTACK_FRAMES = 5

cache = {}
#Player position
PLAYER_X = 0
PLAYER_Y = 0

# import our functions
import functions

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
        self.xvel, self.yvel = 0, 0 # current x and y velocity
        self.onGround, self.jump = False, False
        self.strong_attack, self.melee_attack = False, False
        self.standing_size = (45, 57)
        #self.attack_size = (80, 60)
        self.attack_box = Rect(x, y, self.standing_size[0]/2, self.standing_size[1]/2)

        #self.SURFACE = Surface(self.standing_size[0], self.standing_size[1]/2)
        #self.SURFACE.fill(RED)
        #self.SURFACE.convert_alpha()
        #self.attack_box.fill(RED, rect=self.attack_box, special_flags=0)

        self.rect = Rect(x, y, self.standing_size[0], self.standing_size[1])
        self.enemy_collision, self.knockback_left, self.knockback_right, self.flicker = False, False, False, False
        self.attack_height = 32 # used for calculating height of ranged attack
        self.health = PLAYER_STARTER_HEALTH
        self.melee_damage, self.range_attack = 25, 50
        self.rangeattack_cooldown = 0
        self.damage_frame = 0 # counts # of frames until max damage frames
        self.frame_counter, self.counter, self.jump_counter = 0, 0, 0
        self.attack_counter = 0
        self.running = [SPRITES_DIRECTORY + 'player/running/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7, 8]]
        self.standing = [SPRITES_DIRECTORY + 'player/standing/' + str(x) + '.png' for x in [1, 2, 3, 4]]#, 5, 6]]#, 7, 8, 9]]
        self.jumping = [SPRITES_DIRECTORY + 'player/jumping/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7]]
        self.attacking = [SPRITES_DIRECTORY + 'player/attack/' + str(x) + '.png' for x in [1, 2, 3, 4]]#, 5, 6, 7]]
        self.images = self.standing # by default
        self.image = pygame.image.load(self.images[0])
        self.facing_right = True # used to determine strong attack's direction
        self.image_knockback = pygame.image.load(self.jumping[2])#self.image.copy()
        self.transparent_image = pygame.Surface([32, 32], pygame.SRCALPHA, 32)
        self.transparent_image = self.transparent_image.convert_alpha()
        self.image.convert_alpha()

        #Sound effects
        #self.sound_jump = pygame.mixer.Sound(MUSIC_DIRECTORY + 'sound_effects/player/jump_sound.wav')

        #poison implementation 
        self.poison = False;    
        self.poison_frames = 0;

    def damage(self, attack, enemy, camera):
        """ performs damage reduction on player's HP upon enemy collision """
        if self.damage_frame >= PLAYER_DAMAGE_FRAMES:
            self.damage_frame = 0 # resets damage frame counter
            self.health -= attack
            if self.yvel >= 0:
                self.yvel -= 10 # causes player to jump if player is on ground
                self.onGround = False
            self.flicker = True # causes player to flicker

    def update(self, up, down, left, right, running, platforms, enemies, enemy_sprites, bullets, camera, collision_blocks, RESET_LEVEL_FLAG, entities, blocks):
        global PLAYER_X, PLAYER_Y
        """ updates the player on every frame of main game loop """
        self.damage_frame += 1 # increments damage_frame every frame of game
        self.frame_counter += 1 # increments frame counter

        if self.poison:
            self.poison_frames += 1
            if self.poison_frames >= 210:
                if self.health > 11:
                    self.health = self.health - 10
                    self.poison_frames = 0     
                else:
                    self.health = 5
        
        
        # handle running while jumping
        if self.yvel < 0 and self.jump_counter < 35:
            self.jump = True
        if left or right:
            if not self.jump:
                self.images = self.running
                #self.rect.width, self.rect.height = self.running_size
            if left:
                self.facing_right = False
            elif right:
                self.facing_right = True
        elif not left and not right:
            self.images = self.standing
            #self.rect.width, self.rect.height = self.standing_size

        # standing still while jumping
        if self.jump:
            self.jump_counter += 1
            if self.onGround:
                self.jump = False
                self.jump_counter, self.counter, self.frame_counter = 0, 0, PLAYER_MAX_STANDING_FRAMES
                self.images = self.standing
            else:
                self.images = self.jumping
                #self.rect.width, self.rect.height = self.jumping_size

        if self.strong_attack or self.melee_attack:
            self.images = self.attacking
            self.attack_box.y = self.rect.y
            if self.facing_right:
                self.attack_box.x = self.rect.x + self.standing_size[0]
                #print(self.rect.x)
                #print(self.attack_box.x)
            else:
                self.attack_box.x = self.rect.x - self.standing_size[0]
            if self.attack_counter >= 4:
                self.melee_attack = False
                self.strong_attack = False
                self.attack_counter = 0
                self.frame_counter, self.counter = 0, 0
            if self.frame_counter >= PLAYER_MAX_ATTACK_FRAMES:
                self.attack_counter += 1
                self.frame_counter = 0
                self.counter = (self.counter + 1) % len(self.images)
                self.image = pygame.image.load(self.images[self.counter]).convert_alpha()

                # reverse images if player is facing left
                if self.facing_right == False:
                    self.image = transform.flip(self.image, 1, 0)

            # See if it hit a block
            for block in blocks:
                if self.attack_box.colliderect(block.rect):
                    platforms.remove(block)
                    blocks.remove(block)
                    entities.remove(block)

            for enemy in enemies:
                if self.attack_box.colliderect(enemy.rect):
                    enemy.healthTrigger = True
                    if type(enemy).__name__ != "GarbageCollector":
                        if isinstance(enemy, PySnake):
                            if type(enemy).__name__=="GreenPysnake":
                                enemy.attack *= 2
                            if enemy.health <= 0:
                                enemy.hit = True
                                enemy.counter = 0
                                if not enemy.inflated:
                                    enemy.rect.inflate_ip(-15,18)
                                    enemy.inflated = True
                            else:
                                enemy.health -= self.melee_damage
                                #score += 10
                        else:
                            functions.delete_enemy(enemy, enemy_sprites, enemies, entities)


        # cycle jumping and running frames
        elif self.frame_counter >= PLAYER_MAX_RUN_FRAMES and (self.images == self.running or self.images == self.jumping):
            self.frame_counter = 0
            self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
            self.counter = (self.counter + 1) % (len(self.images)-1)

            # reverse images if player is facing left
            if self.facing_right == False:
                self.image = transform.flip(self.image, 1, 0)

        # cycle standing frames
        elif self.images == self.standing and self.frame_counter >= PLAYER_MAX_STANDING_FRAMES:
            #self.rect.width, self.rect.height = self.standing_size
            self.frame_counter = 0
            self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
            self.counter = (self.counter + 1) % len(self.images)

            if self.facing_right == False:
                self.image = transform.flip(self.image, 1, 0)

        # flicker player when player is knocked back
        if self.flicker:
            if self.image is self.transparent_image:
                self.image = self.image_knockback
            else:
                self.image = self.transparent_image

        # handle knock back collision
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                if type(enemy).__name__ == "PurplePysnake":
                     self.poison = True
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
                self.image = self.image_knockback

        # handle player movements
        else:
            if up:
                # only jump if on the ground
                if self.onGround:
                    self.yvel -= 10
                    #self.sound_jump.play()
            if down:
                pass # we can eventually implement crouching
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
            if not(left or right):
                self.xvel = 0

        # only accelerate with gravity if in the air and no knockback
        if not self.onGround:
            self.yvel += 0.6 # increment falling velocity
            if self.yvel > 100:
                self.yvel = 100 # max falling speed

        self.rect.left += self.xvel # Modifies player's position in X direction
        PLAYER_X = self.rect.left #  Global Position Update:

        self.collide(self.xvel, 0, platforms) # do x-axis collisions

        self.rect.top += self.yvel  # Modifies player's position in Y direction
        PLAYER_Y = self.rect.top  # Global Position Update

        self.onGround = False; # assuming we're in the air
        self.collide(0, self.yvel, platforms) # do y-axis collisions

        # handles level changing
        for c in collision_blocks:
            if pygame.sprite.collide_rect(self, c):
                #print type(c).__name__
                if type(c).__name__ == "BlankPlatform":
                    return c
                elif type(c).__name__ == "ExitBlock":#isinstance(c, ExitBlock):
                    return "Reset Level"

    def collide(self, xvel, yvel, platforms):
        """ handles platform collision for player """
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
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
    def __init__(self, mouse, player, camera_state, direction, strength = None):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # grab mouse coordinates
        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        if strength == "strong":
            # calculate center of bullet
            self.center_y = player[1]/2 + player[2]/2 + 10# + player[2] - player[2]/2)
            self.center_x = player[0]/2 + player[2]/2 + 10
            self.image = pygame.image.load(SPRITES_DIRECTORY + 'player/blade_wave.png')
            if not direction:
                self.image = transform.flip(self.image, 1, 0)
        else:
            self.image = pygame.Surface([4, 4])
            self.image.fill(WHITE)
            # calculate center of bullet
            self.center_y = (player[1]/2 + player[2]/2)
            self.center_x = (player[0]/2 - player[2]/2)
        self.rect = self.image.get_rect()
        #self.rect = Rect(x, y, 60, 60)
        # offset camera state on x coordinates
        self.mouse_x -= camera_state[0]
        self.strength = strength
        self.direction = direction
        # might need to offset camera in y coordinates in the future
        # .. add here

    def update(self):
        """ Move the bullet. """
        speed = 7
        range = 200
        # generate bullet vector
        if self.strength == None:
            distance = [self.mouse_x - self.center_x, self.mouse_y - self.center_y]
            norm = sqrt(distance[0] ** 2 + distance[1] ** 2)
            direction = [distance[0] / norm, distance[1] / norm]
            bullet_vector = [direction[0] * speed, direction[1] * speed]
            self.rect.x += bullet_vector[0]
            self.rect.y += bullet_vector[1]
        else:
            if self.direction == True:
                self.rect.x += 4
            else:
                self.rect.x -= 4

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
    def __init__(self, x, y, BlockType, patrol):
        Entity.__init__(self)
        self.rect = Rect(x, y, 32, 32)
        self.image = pygame.Surface([32, 32], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.patrol = patrol
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
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/baige_block.png").convert_alpha()
    def update(self):
        pass

class BrownBlock(BlockType):
    """ brown block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/brown_block.png").convert_alpha()
    def update(self):
        pass

class NeonRedBlock(BlockType):
    """ neon red block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/neon_red.png").convert_alpha()
    def update(self):
        pass

class NeonWhiteBlock(BlockType):
    """ neon white block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/neon_white.png").convert_alpha()
    def update(self):
        pass

class NeonBlueBlock(BlockType):
    """ neon blue block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/neon_blue.png").convert_alpha()
    def update(self):
        pass

class NeonYellowBlock(BlockType):
    """ neon yellow block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/neon_yellow.png").convert_alpha()
    def update(self):
        pass

class NeonOrangeBlock(BlockType):
    """ neon orange block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/neon_orange.png").convert_alpha()
    def update(self):
        pass

class NeonGreenBlock(BlockType):
    """ neon green block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/neon_green.png").convert_alpha()
    def update(self):
        pass

class BlueBlock(BlockType):
    """ blue block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/blue_block.png").convert_alpha()
    def update(self):
        pass

class BrightBlueBlock(BlockType):
    """ bright blue block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/bright_blue_block.png").convert_alpha()
    def update(self):
        pass

class GrayBlock(BlockType):
    """ gray block class """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/gray_block.png").convert_alpha()
    def update(self):
        pass

class Unbreakable1(BlockType):
    """ brown unbreakable block """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/unbreakable1.png").convert_alpha()

    def update(self):
        pass

class Unbreakable2(BlockType):
    """ grey brick unbreakable block """
    def __init__(self):
        BlockType.__init__(self)
        self.image = pygame.image.load(SPRITES_DIRECTORY + "blocks/unbreakable2.png").convert_alpha()
    def update(self):
        pass

class CollisionBlock(BlockType):
    """ blank block used to detect collisions """
    def __init__(self):
        BlockType.__init__(self)
    def update(self):
        pass

class CornerPatrolBlock(CollisionBlock):
    """ unremovable corner patrol block """
    def __init__(self):
        CollisionBlock.__init__(self)
    def update(self):
        pass

class ExitBlock(BlockType):
    """ invisible block used to detect level endings """
    def __init__(self, x, y, top):
        BlockType.__init__(self)
        self.rect = Rect(x, y, 32, 32)
        #self.image = pygame.Surface([32, 32], pygame.SRCALPHA, 32)
        if top == "X":
            self.image = pygame.image.load(SPRITES_DIRECTORY + "door/top_door.png")
        elif top == "Y":
            self.image = pygame.image.load(SPRITES_DIRECTORY + "door/bottom_door.png")

        # SRC ALPHA BUG IS PROBABLY HERE ^^^
        self.image = self.image.convert_alpha()
    def update(self):
        pass

class Enemy(Entity):
    """ Abstract enemy object """
    def __init__(self):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.attack = 0
        self.reverse = False
        self.onGround = False
        self.frame_counter = 0
        self.counter = 0
        self.health_counter = 0
        self.healthTrigger = False

    def dead(self):
        return False

"""                                 Enemies                                 """

class GarbageCollector(Enemy):
    """ GarbageCollector Enemy object """

    def __init__(self, x, y):
        Enemy.__init__(self)
        self.rect = Rect(x, y, 69.5, 69.5)

        # establish attack for garbage collector
        self.attack = 100

        # establish list of sprite images
        self.images = [SPRITES_DIRECTORY + 'garbage_collector/' + str(x) + '.png' for x in [1, 2, 3, 4]]
        self.image = pygame.image.load(self.images[0]) # start on first images

    def update(self, platforms, blank_platforms, blocks, entities):
        """ update garbage collector """
        self.frame_counter += 1
        # switch frames
        if self.frame_counter == GARBAGE_COLLECTOR_MAX_FRAMES:
            self.frame_counter = 0
            self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
            # reverse frames if enemy is walking in reverse
            if self.reverse:
                self.image = transform.flip(self.image, 1, 0)
            self.counter = (self.counter + 1) % len(self.images)

        # count frames to display healthbar
        self.health_counter += 1

        # set velocity
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

        # establishes attack for pysnake
        self.attack = 25

        # max health and health should start at the same constant
        self.max_health = 100
        self.health = 100

        # establish list of sprite images
        self.images = [SPRITES_DIRECTORY + 'PySnake/default_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
        self.dying = [SPRITES_DIRECTORY + 'PySnake/default_snake/default_dead_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7]]
        self.image = pygame.image.load(self.images[0]) # start on first image
        self.hit = False
        self.kill = False
        self.dying_counter = 0
        self.inflated = False # for handeling resizing on death

    def update(self, platforms, blank_platforms, blocks, entities):
        """ update garbage collector """
        self.frame_counter += 1
        if self.frame_counter == GARBAGE_COLLECTOR_MAX_FRAMES:
            self.frame_counter = 0
            self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
            if self.reverse:
                self.image = transform.flip(self.image, 1, 0)
            self.counter = (self.counter + 1) % len(self.images)
        if self.hit:
            self.xvel = 0
            self.images = self.dying
            #self.counter = 0
            self.dying_counter += 1
        if not self.hit:
            if not self.reverse:
                self.xvel = -2
            elif self.reverse:
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
        if self.dying_counter < 30:
            self.collide(self.xvel, 0, platforms, blocks, entities)

        # increment in y direction
        self.rect.top += self.yvel
        self.onGround = False;

        # do y-axis collision
        if self.dying_counter < 30:
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
                    #if p in blocks:
                    #    pass
                if xvel < 0: # moving left, hit right side of wall
                    self.rect.left = p.rect.right
                    #if p in blocks:
                    #    pass
                if yvel > 0: # moving down, hit top of wall
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0: # moving up, hit bottom side of wall
                    self.rect.top = p.rect.bottom

    def dead(self):
        return self.hit and self.dying_counter >= 55

class GreenPysnake(PySnake):
    """ green pysnake enemy """
    def __init__(self, x, y):
        PySnake.__init__(self, x, y)
        self.images = [SPRITES_DIRECTORY + 'PySnake/green_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
        self.image = pygame.image.load(self.images[0]) # start on first image
        self.dying = [SPRITES_DIRECTORY + 'PySnake/green_snake/green_dead_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7]]

    #def collide(self, xvel, yvel, platforms, blocks, entities, player):
    #   PySnake.collide(self, xvel, yvel, platforms, blocks, entities)

class RedPysnake(PySnake):
    """ red pysnake enemy """
    def __init__(self, x, y):
        PySnake.__init__(self, x, y)
        self.images = [SPRITES_DIRECTORY + 'PySnake/red_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
        self.image = pygame.image.load(self.images[0]) # start on first image
        self.dying = [SPRITES_DIRECTORY + 'PySnake/red_snake/red_dead_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7]]

class PurplePysnake(PySnake):
    """ purple pysnake enemy """
    def __init__(self, x, y):
        PySnake.__init__(self, x, y)
        self.images = [SPRITES_DIRECTORY + 'PySnake/purple_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
        self.image = pygame.image.load(self.images[0]) # start on first image
        self.dying = [SPRITES_DIRECTORY + 'PySnake/purple_snake/purple_dead_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7]]

class BluePysnake(PySnake):
    """ blue pysnake enemy """
    def __init__(self, x, y):
        PySnake.__init__(self, x, y)
        self.images = [SPRITES_DIRECTORY + 'PySnake/blue_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
        self.image = pygame.image.load(self.images[0]) # start on first image
        self.dying = [SPRITES_DIRECTORY + 'PySnake/blue_snake/blue_dead_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7]]

class Ghost(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self)
        self.rect = Rect(x, y, 25, 25)
        self.image = pygame.image.load(SPRITES_DIRECTORY + 'ghosts/boo/normal/1.png')
        self.reverse = False

        # establishes attack for pysnake
        self.attack = 25

        # max health and health should start at the same constant
        self.max_health = 100
        self.health = 100

        #direction
        self.xdir = -1
        self.ydir = 1

        #velocity
        self.xvel = 2
        self.yvel = 2

        #flag to start moving
        self.visible = False
        # establish list of sprite images
        #self.images = [SPRITES_DIRECTORY + 'PySnake/default_snake/' + str(x) + '.png' for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
        #self.image = pygame.image.load(self.images[0]) # start on first image


    def update(self, platforms, blank_platforms, blocks, entities):
        """ update garbage collector """
        #self.frame_counter += 1
        #if self.frame_counter == GARBAGE_COLLECTOR_MAX_FRAMES:
        #    self.frame_counter = 0
        #    self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
        #    self.counter = (self.counter + 1) % len(self.images)

        #  # only accelerate with gravity if in the air
        # if not self.onGround:
        #     self.yvel += 0.4 # increase falling distance
        #      # max falling speed
        #     if self.yvel > 100:
        #         self.yvel = 100

        # Flip image and set reverse flag
        if self.xdir < 0 and self.reverse:
            self.reverse = False
            self.image = transform.flip(self.image, 1, 0)
        if self.xdir > 0 and not self.reverse:
            self.reverse = True
            self.image = transform.flip(self.image, 1, 0)

        # increment in x direction
        self.rect.left += int(round(self.xdir * self.xvel))

        # do x-axis collision
        self.collide(self.xvel, 0, platforms, blocks, entities)

        # increment in y direction
        self.rect.top += int(round(self.ydir * self.yvel))
        self.onGround = False;

        # do y-axis collision
        self.collide(0, self.yvel, platforms, blocks, entities)

    def collide(self, xvel, yvel, platforms, blocks, entities):
        pass

    def dead(self):
        return functions.out_of_level(self.rect, pygame.total_level_width, pygame.total_level_height)

class WhiteGhost(Ghost):
    def __init__(self, x, y):
        Ghost.__init__(self, x, y)
        #Setting initial_rect
        self.top_bound = self.rect.top - 100
        self.bot_bound = self.rect.top + 100

        #arrays for testing
        self.x_arr = []
        self.y_arr = []

    def update(self, platforms, blank_platforms, blocks, entities):
        Ghost.update(self, platforms, blank_platforms, blocks, entities)

        #self.ydir = sin(radians(self.rect.left))

        if self.rect.top <= self.top_bound:
            self.ydir = 1
            self.image = pygame.image.load(SPRITES_DIRECTORY + 'ghosts/boo/normal/1.png')
            # self.ydir = sin(radians(self.rect.left))
            # self.xdir = sin(radians(self.rect.left))
        elif self.rect.top >= self.bot_bound:
            self.ydir = -1
            self.image = pygame.image.load(SPRITES_DIRECTORY + 'ghosts/boo/normal/2.png')
            # self.ydir = sin(radians(self.rect.left))
            # self.xdir = -sin(radians(self.rect.left))

        #if self.rect.left < 0:
        #    #plt.plot(self.x_arr,self.y_arr)
        #    #plt.show()
        #    #pygame.quit()
        self.x_arr.append(self.rect.left)
        self.y_arr.append(self.rect.top)

class RedGhost(Ghost):
    def __init__(self, x, y):
        Ghost.__init__(self, x, y)
        self.radius = 500       # View radius, for chasing player
        self.chasing = False    # Chasing movement flag
        self.move_away = False  # Move away from overlapping ghost flag

    def update(self, platforms, blank_platforms, blocks, entities):
        global PLAYER_X, PLAYER_Y
        Ghost.update(self, platforms, blank_platforms, blocks, entities)
        # Chasing Functionality
        if self.chasing:
            # find normalized direction vector (dx, dy) between enemy and player
            dx, dy = self.rect.left - PLAYER_X, self.rect.top - PLAYER_Y
            dist = hypot(dx, dy)
            self.xdir, self.ydir = -1 * dx / dist, -1 * dy / dist # direction are reversed
            # move along this normalized vector towards the player at current speed

        if self.move_away:
            pass

    def collide(self, xvel, yvel, platforms, blocks, entities):
        for e in entities:
            if isinstance(e,Player):
                player_in_view = pygame.sprite.collide_circle(self,e)
                if player_in_view and not self.chasing:
                    self.chasing = True
                elif not player_in_view and self.chasing:
                    self.chasing = False
            elif isinstance(e,RedGhost):
                overlapping_ghosts = pygame.sprite.collide_rect(self,e)
                if overlapping_ghosts and not self.move_away:
                    self.move_away = True
                elif not overlapping_ghosts and self.move_away:
                    self.move_away = False

    def dead(self):
        return False

""" END OF ENEMIES """

class Coin(Entity):
    """ Coin block class """
    def __init__(self, x, y):
        Entity.__init__(self)
        self.rect = Rect(x, y, 32, 32)
        self.counter, self.frame_counter = 0, 0
        self.images = [SPRITES_DIRECTORY + '/coin/' + str(x) + '.png' for x in [1, 2, 3, 4]]
        self.image = pygame.image.load(self.images[0]).convert_alpha() # start on first image
    def update(self, player):
        self.frame_counter += 1
        if self.frame_counter == COIN_MAX_FRAMES:
            self.frame_counter = 0
            self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
            self.counter = (self.counter + 1) % len(self.images)
        if pygame.sprite.collide_rect(self, player):
            return True
        else:
            return False
            
class PurpleCoin(Coin):
        def __init__(self, x, y):
            Coin.__init__(self, x, y)
            self.images = [SPRITES_DIRECTORY + '/coin/purple_coin/' + str(x) + '.png' for x in [1, 2, 3, 4]]
        def update(self, player):
            Coin.update(self, player)
            if pygame.sprite.collide_rect(self, player):
                 player.poison = False
                 if player.health < PLAYER_STARTER_HEALTH - 25:
                    player.health = player.health + 25
                 return True
            else:
                 return False