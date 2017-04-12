#! /usr/bin/python

import levels
import classes
import os, time
import pygame

def simple_camera(camera, target_rect):
    """ simple camera class """
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+classes.HALF_WIDTH, -t+classes.HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    """ complex camera class """
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+classes.HALF_WIDTH, -t+classes.HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-classes.WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-classes.WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)

def get_level(level_num):
    """ retrieve levels """
    return levels.get_levels[level_num]

#def get_enemies(level_num):
#    """ retreieve enemies """
#    return levels.get_enemies[level_num]

def build_level(*args):
    """ build level passed in """
    # unpackage arguments
    current_level, level, enemies, enemy_sprites, platforms, blocks, entities,\
    Platform, block_types, collision_blocks,\
    collision_block_sprites, indestructibles = (x for x in args)

    # unpackage block_types
    Unbreakable1, Unbreakable2, BaigeBlock,\
    NeonRedBlock, NeonWhiteBlock, NeonBlueBlock, NeonYellowBlock, NeonOrangeBlock, NeonGreenBlock,\
    BlueBlock, GrayBlock, BrightBlueBlock, BrownBlock,\
    CollisionBlock, CornerPatrolBlock = (x for x in block_types)

    enemy = None

    x, y = 0, 0
    # build the level
    for row in level:
        for col in row:
            if col != " ":
                if col == "E":
                    which_block = BaigeBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "C":
                    which_block = BrownBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "A":
                    which_block = BlueBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "B":
                    which_block = BrightBlueBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "D":
                    which_block = GrayBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "r":
                    which_block = NeonRedBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "w":
                    which_block = NeonWhiteBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "b":
                    which_block = NeonBlueBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "y":
                    which_block = NeonYellowBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "o":
                    which_block = NeonOrangeBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "g":
                    which_block = NeonGreenBlock
                    p = classes.Platform(x, y, which_block)
                    platforms, blocks, entities = InsertPlatform(p, platforms, blocks, entities)
                elif col == "n":
                    which_block = Unbreakable1
                    # add indestructible manually to sprite lists
                    p = classes.Platform(x, y, which_block)
                    indestructibles.add(p)
                    entities.add(p)
                    platforms.append(p)
                elif col == "m":
                    which_block = Unbreakable1
                    # add indestructible manually to sprite lists
                    p = classes.Platform(x, y, which_block)
                    indestructibles.add(p)
                    entities.add(p)
                    platforms.append(p)
                elif col == "O":
                    which_block = CollisionBlock
                    # add collision block manually to sprite lists
                    p = classes.BlankPlatform(x, y, which_block, False)
                    collision_blocks.append(p)
                    collision_block_sprites.add(p)
                    entities.add(p)
                elif col == "Q":
                    which_block = CornerPatrolBlock
                    p = classes.BlankPlatform(x, y, which_block, True)
                    collision_blocks.append(p)
                    collision_block_sprites.add(p)
                    entities.add(p)
                elif col == "X":
                    # add exit block manually to sprite lists
                    p = classes.ExitBlock(x, y)
                    collision_blocks.append(p)
                    collision_block_sprites.add(p)
                    entities.add(p)
                # spawn enemies
                elif col in list('1234567'):
                    if col == "1":
                        enemy = classes.GarbageCollector(x-32, y-64)
                    elif col == "2":
                        enemy = classes.GreenPysnake(x-32, y-64)
                    elif col == "3":
                        enemy = classes.RedPysnake(x-32, y-64)
                    elif col == "4":
                        enemy = classes.BluePysnake(x-32, y-64)
                    elif col == "5":
                        enemy = classes.PurplePysnake(x-32, y-64)
                    elif col == "6":
                        enemy = classes.RedGhost(x, y)
                    elif col == "7":
                        enemy = classes.WhiteGhost(x, y)
                    entities.add(enemy)
                    enemies.append(enemy)
                    enemy_sprites.add(enemy)
            x += 32 # index by 32 bits
        y += 32
        x = 0

    #for enemy in get_enemies(current_level):
    #    # re-calls enemy's constructor
    #    enemy = type(enemy)(enemy.rect.x, enemy.rect.y)
    #    entities.add(enemy)
    #    enemy_sprites.add(enemy)
    #    enemies.append(enemy)

    return platforms, blocks, entities, enemies,\
    enemy_sprites, collision_block_sprites, indestructibles, collision_blocks

def InsertPlatform(p, platforms, blocks, entities):
    platforms.append(p)
    blocks.add(p)
    entities.add(p)
    return platforms, blocks, entities

def bullet_collision(*args):
    """ handles bullet collision """

    # unpackage arguments
    bullets, blocks, platforms, entities,\
    enemies, enemy_sprites, indestructibles, score = (x for x in args)

    # See if it hit a block
    block_hit_list, bullet_hit_list = [], []
    for bullet in bullets:
        hit_block = pygame.sprite.spritecollide(bullet, blocks, True)
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
        hit_enemy = pygame.sprite.spritecollide(bullet, enemy_sprites, False)
        enemy_hit_list += hit_enemy
        if bool(hit_enemy):
            bullets.remove(bullet)
            entities.remove(bullet)

    # If we hit an enemy, destroy it (unless garbage collector)
    for enemy in enemy_hit_list:
        enemy.healthTrigger = True
        if type(enemy).__name__ != "GarbageCollector":
            if isinstance(enemy, classes.PySnake):
                if type(enemy).__name__=="GreenPysnake":
                    enemy.attack *= 2
                if enemy.health <= 0:
                    enemy.hit = True
                    enemy.counter = 0
                    if not enemy.inflated:
                        enemy.rect.inflate_ip(-15,18)
                        enemy.inflated = True
                else:
                    enemy.health -= 20
                    score += 20
            else:
                enemies.remove(enemy)
                enemy_sprites.remove(enemy)
                entities.remove(enemy)

    # See if we hit an indestructible block
    for bullet in bullets:
        if bool(pygame.sprite.spritecollide(bullet, indestructibles, False)):
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

    return bullets, entities, platforms, blocks, enemies, enemy_sprites, score

def reset_level(*args):
    """ respawn player and rebuild layer if player dies """

    # unpackage arguments
    screen, player, level, current_level, platforms, bullets, blocks,\
    entities, enemies, enemy_sprites, Platform,\
    block_types, collision_blocks, collision_block_sprites,\
    indestructibles, SPAWN_POINT_LEVEL = (x for x in args)

    # reset sprites and re-add player to game
    platforms = []
    indestructibles.empty()
    entities.empty()
    blocks.empty()
    bullets.empty()
    collision_blocks = []
    collision_block_sprites.empty()
    enemy_sprites.empty()
    enemies = []

    # build up arg list for build_level function
    args = current_level, level, enemies, enemy_sprites, platforms, blocks,\
    entities, Platform, block_types, collision_blocks,\
    collision_block_sprites, indestructibles

    # rebuild level
    platforms, blocks, entities, enemies, enemy_sprites,\
    collision_block_sprites, indestructibles, collision_blocks = build_level(*args)

    # respawn player at these coordinates
    player.kill()
    x, y = SPAWN_POINT_LEVEL[current_level][0], SPAWN_POINT_LEVEL[current_level][1]
    player = classes.Player(x, y)
    entities.add(player)

    return player, platforms, blocks, collision_blocks, collision_block_sprites,\
    entities, enemies, enemy_sprites, indestructibles

def healthBar(player_health, screen, cache):
    """ displays player's health bar at top right of screen """
    if player_health > classes.PLAYER_STARTER_HEALTH * 0.75:
        player_health_color = classes.GREEN
    elif player_health > classes.PLAYER_STARTER_HEALTH* 0.40:
        player_health_color = classes.YELLOW
    else:
        player_health_color = classes.RED
    """ pygame.draw.rect(screen, color, (x,y,width,height), thickness) """
    pygame.draw.rect(screen, player_health_color, (549,25,player_health,25), 0)
    pygame.draw.rect(screen, classes.WHITE, (549,25,classes.PLAYER_STARTER_HEALTH,25), 3)
    font = pygame.font.Font(None, 18)
    text = font.render("HP " + str(player_health), True, player_health_color)
    #text = get_msg("HP " + str(player_health), cache, player_health_color)
    text_rect = text.get_rect()
    text_x = 549
    text_y = screen.get_height() / 10 - text_rect.height / 2 + 20
    screen.blit(text, [text_x, text_y])

def enemyHealthBar(enemy_health, enemy, screen, camera_state):
    """ displays health bar above enemy """
    if enemy_health > enemy.max_health * 0.75:
        enemy_health_color = classes.GREEN
    elif enemy_health > enemy.max_health * 0.40:
        enemy_health_color = classes.YELLOW
    else:
        enemy_health_color = classes.RED
    """ pygame.draw.rect(screen, color, (x,y,width,height), thickness) """
    pygame.draw.rect(screen, enemy_health_color,\
    (enemy.rect.left + camera_state[0],\
    enemy.rect.top - enemy.rect.height + camera_state[1] + 35, enemy_health, 10), 0)
    pygame.draw.rect(screen, classes.WHITE,\
    (enemy.rect.left + camera_state[0],\
    enemy.rect.top - enemy.rect.height + camera_state[1] + 35, enemy.max_health, 10), 1)

def garbageCollectorHealthBar(enemy, screen, camera_state):
    """ displays garbage collectors health bar """
    pygame.draw.rect(screen, classes.WHITE,\
    (enemy.rect.x + camera_state[0],\
    enemy.rect.top-enemy.rect.height + camera_state[1] + 35, 75,10), 0)

def get_msg(msg, cache, color = None):
    """ a cache for font objects """
    if not msg.strip(' ') in cache:
        msg = msg.strip(' ')
        if msg == 'Game Over' or msg == 'Try again bruh...':
            font = pygame.font.Font(None, 36)
            cache[msg] = font.render(msg, True, classes.WHITE)
        elif color != None:
            font = pygame.font.Font(None, 18)
            cache[msg] = font.render(msg, True, color)
        else:
            font = pygame.font.Font(None, 24)
            cache[msg] = font.render(msg, True, classes.WHITE)
    #cache[msg] = fontobj.render(msg, False , pygame.Color('green'))
    return cache[msg]

def gameOver(screen, cache):
    """ displays gameover message in center of screen """
    #font = pygame.font.Font(None, 36)
    #text = font.render("Game Over", True, WHITE)
    text = get_msg('Game Over', cache)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])
    pygame.display.flip()
    pygame.time.delay(1000)

def loading(screen, cache):
    """ displays loading message in center of screen """
    #font = pygame.font.Font(None, 24)
    #text = font.render("Loading...", True, WHITE)
    text = get_msg('Loading...', cache)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])
    #pygame.time.delay(1000)

def displayTimer(screen, time_left, current_score, cache):
    """ displays countdown timer and score """
    # display timer text
    #font = pygame.font.Font(None, 24)
    #text = font.render('Timer: ', True, WHITE)
    text = get_msg('Timer:', cache)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 8 - text_rect.width / 2 - 45 # + text_rect.width - 40
    text_y = screen.get_height() / 16 + 10
    text_width, text_height = text_x, 17
    screen.blit(text, [text_x, text_y])
    # display elapsed timer
    text = get_msg(time_left, cache)
    #text = font.render(time_left, True, WHITE)
    text_rect = text.get_rect()
    text_x = text_x + 57 #screen.get_width() / 8 - #text_rect.width / 2 + 12 # + text_rect.width - 40
    text_y = screen.get_height() / 16 + 10
    text_width, text_height = text_x, 17
    screen.blit(text, [text_x, text_y])
    # display score
    text = get_msg('Score: ' + str(current_score).zfill(8), cache)
    #text = font.render('Score: ' + str(current_score).zfill(8), True, WHITE)
    text_rect = text.get_rect()
    text_x = screen.get_width() / 8 - text_rect.width / 2
    text_y = screen.get_height() / 16 - 5
    text_width, text_height = text_x, 17
    screen.blit(text, [text_x, text_y])

def displayLives(screen, lives):
    if lives == 3:
        image = pygame.image.load("../sprites/lives/3hearts.png").convert_alpha()
    elif lives == 2:
        image = pygame.image.load("../sprites/lives/2hearts.png").convert_alpha()
    elif lives == 1:
        image = pygame.image.load("../sprites/lives/1heart.png").convert_alpha()
    else:
        image = pygame.image.load("../sprites/lives/0hearts.png").convert_alpha()
    imagerect = image.get_rect()
    image = pygame.transform.scale(image, (75, 25))
    image_x = 675
    image_y = 55
    screen.blit(image, [image_x, image_y])

def scrollScore(current_score, score):
    if current_score < score:
        current_score += 1
    return current_score

def delete_enemy(target, enemy_sprites, enemies, entities):
    enemy_sprites.remove(target)
    enemies.remove(target)
    entities.remove(target)

def out_of_level(rect, max_x, max_y):
    return rect.left < 0 or rect.left > max_x or \
           rect.top < 0 or rect.top > max_y
