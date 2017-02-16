#! /usr/bin/python

import levels
from classes import *
import os, time

def simple_camera(camera, target_rect):
    """ simple camera class """
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    """ complex camera class """
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

def get_level(level_num):
    """ retrieve levels """
    if level_num == 1:
        return levels.level_1
    else:
        return

def get_enemies(level_num):
    #if(level_num == 1):
    return levels.level_1_enemies

def build_level(*args):
    """ build level passed in """

    # unpackage arguments
    level, enemies, platforms, blocks, entities,\
    Platform, block_types = (x for x in args)

    # unpackage block_types
    BaigeBlock, MossyBlock, BaigeRoundBlock = (x for x in block_types)

    x, y = 0, 0
    # build the level
    for row in level:
        for col in row:
            if col != " ":
                if col == "B":
                    which_block = BaigeBlock
                elif col == "M":
                    which_block = MossyBlock
                elif col == "R":
                    which_block = BaigeRoundBlock
                p = Platform(x, y, which_block)
                platforms.append(p)
                blocks.add(p)
                entities.add(p)
            x += 32 # index by 32 bits
        y += 32
        x = 0

    # add enemies to list of entities
    for enemy in enemies:

        #if e[0] == GARBAGE_COLLECTOR:
        #    enemy = GarbageCollector(e[1], e[2])
        entities.add(enemy)

    return platforms, blocks, entities, enemies

def getFont(name = None, size = 20):
   '''Create a font object'''
   font = pygame.font.Font(name, size)
   return font

# Render the text
def putText(screen, fontOBJ, message = "Test", position = (10,10),
            forecolour = BLACK, backcolour = WHITE):
   '''Create a font object'''
   antialias = True
   text = fontOBJ.render(message, antialias, forecolour, backcolour)
   # Create a rectangle
   textRect = text.get_rect()
   textRect.topleft = position
   # Blit the text
   screen.blit(text, textRect)
   pygame.display.update()

def bullet_collision(*args):
    """ handles bullet collision """

    # unpackage arguments
    bullets, blocks, platforms, entities = (x for x in args)

    # See if it hit a block
    block_hit_list, bullet_hit_list = [], []
    for bullet in bullets:
        hit_block = sprite.spritecollide(bullet, blocks, True)
        block_hit_list += hit_block # keep track of hit blocks
        if bool(hit_block):
            bullet_hit_list.append(bullet)

    # For each block hit, cause a collision
    for block in block_hit_list:
            platforms.remove(block)
            blocks.remove(block)
            entities.remove(block)

    # remove each bullet that hits a block
    for bullet in bullet_hit_list:
            bullets.remove(bullet)
            entities.remove(bullet)

    # Remove the bullet if it flies off the screen
    for bullet in bullets:
        if bullet.rect.y > 1000:
            bullets.remove(bullet)
            entities.remove(bullet)

    return bullets, entities, platforms, blocks

def player_has_died(*args):
    """ respawn player and rebuild layer if player dies """

    # unpackage arguments
    screen, player, level, platforms, bullets, blocks,\
    entities, enemies, text, Platform, block_types = (x for x in args)

    # reset sprites and re-add player to game
    platforms = []
    blocks.empty()
    entities.empty()
    bullets.empty()
    entities.add(player)

    # rebuild level
    args = level, enemies, platforms, blocks,\
    entities, Platform, block_types #ExitBlock
    platforms, blocks, entities, enemies = build_level(*args)

    # respawn player at these coordinates
    x, y = 32, 32

    # render you died text
    bodylines = [
        [(140, 100), text]]
    bodyfont = getFont(None, 22)
    for line in bodylines:
       position, text = line
       putText(screen, bodyfont, text, position,
            forecolour = WHITE,
            backcolour = BLACK )
    time.sleep(1)
    return platforms, blocks, entities, enemies, x, y