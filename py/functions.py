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
    level, enemies, enemy_sprites, platforms, blocks, entities,\
    Platform, block_types, collision_blocks,\
    collision_block_sprites, indestructibles = (x for x in args)

    # unpackage block_types
    BaigeBlock, LeftStoneBlock, RightStoneBlock,\
    BlueBlock, GrayBlock, BrightBlueBlock, BrownBlock,\
    TopRightStoneBlock, TopLeftStoneBlock, CollisionBlock = (x for x in block_types)

    x, y = 0, 0
    # build the level
    for row in level:
        for col in row:
            if col != " ":
                if col == "E":
                    which_block = BaigeBlock
                    p = Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "C":
                    which_block = BrownBlock
                    p = Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "A":
                    which_block = BlueBlock
                    p = Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "B":
                    which_block = BrightBlueBlock
                    p = Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "D":
                    which_block = GrayBlock
                    p = Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "L":
                    which_block = TopLeftStoneBlock
                    p = Platform(x, y, which_block)
                    indestructibles.add(p)
                    entities.add(p)
                    platforms.append(p)
                elif col == "R":
                    which_block = TopRightStoneBlock
                    p = Platform(x, y, which_block)
                    indestructibles.add(p)
                    entities.add(p)
                    platforms.append(p)
                elif col == "M":
                    which_block = LeftStoneBlock
                    p = Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "N":
                    which_block = RightStoneBlock
                    p = Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "O":
                    which_block = CollisionBlock
                    p = BlankPlatform(x, y, which_block)
                    collision_blocks.append(p)
                    entities.add(p)
            x += 32 # index by 32 bits
        y += 32
        x = 0

    for enemy in get_enemies(level):
        # re-calls enemy's constructor
        enemy = type(enemy)(enemy.rect.x, enemy.rect.y)
        entities.add(enemy)
        enemy_sprites.add(enemy)
        enemies.append(enemy)

    return platforms, blocks, entities, enemies,\
    enemy_sprites, collision_block_sprites, indestructibles

def InsertPlatform(p, platforms, blocks, entities):
    platforms.append(p)
    blocks.add(p)
    entities.add(p)
    return platforms, blocks, entities

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
    bullets, blocks, platforms, entities,\
    enemies, enemy_sprites, indestructibles = (x for x in args)

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

    # See if we hit an enemy
    enemy_hit_list = []
    for bullet in bullets:
        hit_enemy = sprite.spritecollide(bullet, enemy_sprites, False)
        enemy_hit_list += hit_enemy
        if bool(hit_enemy):
            bullets.remove(bullet)
            entities.remove(bullet)

    # If we hit an enemy, destroy it (unless garbage collector)
    for enemy in enemy_hit_list:
        if type(enemy).__name__ != "GarbageCollector":
            enemies.remove(enemy)
            enemy_sprites.remove(enemy)
            entities.remove(enemy)

    # See if we hit an indestructible block
    for bullet in bullets:
        if bool(sprite.spritecollide(bullet, indestructibles, False)):
            bullets.remove(bullet)
            entities.remove(bullet)

    # remove each bullet that hits a block or enemy
    for bullet in bullet_hit_list:
            bullets.remove(bullet)
            entities.remove(bullet)

    # Remove the bullet if it flies off the screen
    for bullet in bullets:
        if bullet.rect.y > 1000:
            bullets.remove(bullet)
            entities.remove(bullet)

    return bullets, entities, platforms, blocks, enemies, enemy_sprites

def player_has_died(*args):
    """ respawn player and rebuild layer if player dies """

    # unpackage arguments
    screen, player, level, platforms, bullets, blocks,\
    entities, enemies, enemy_sprites, text, Platform,\
    block_types, collision_blocks, collision_block_sprites,\
    indestructibles = (x for x in args)

    # reset sprites and re-add player to game
    platforms = []
    indestructibles.empty()
    entities.empty()
    blocks.empty()
    bullets.empty()
    enemy_sprites.empty()
    enemies = []
    

    # build up arg list
    args = level, enemies, enemy_sprites, platforms, blocks,\
    entities, Platform, block_types, collision_blocks,\
    collision_block_sprites, indestructibles
    # rebuild level
    platforms, blocks, entities, enemies, enemy_sprites,\
    collision_block_sprites, indestructibles = build_level(*args)

    # respawn player at these coordinates

    player.kill()
    # level 1 spawn coordinates
    #if(level == 1):
    x, y = 64, 32
    player = Player(x, y)
    entities.add(player)

    player.health = 100

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
    return player, platforms, blocks, collision_blocks, collision_block_sprites,\
    entities, enemies, enemy_sprites, indestructibles

def healthBar(player_health, screen):
    if player_health > 75:
        player_health_color = GREEN
    elif player_health > 50:
        player_health_color = YELLOW
    else:
        player_health_color = RED
    pygame.draw.rect(screen, player_health_color, (660, 25, player_health, 25))
