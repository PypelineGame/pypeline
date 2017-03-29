#! /usr/bin/python

# import our modules
from functions import *
import levels
from classes import *

import time, os, sys

def main():
    global cameraX, cameraY
    global RESET_LEVEL_FLAG
    RESET_LEVEL_FLAG = False
    pygame.init()

    print ("Game loaded.")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    hud = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    timer = pygame.time.Clock()

    # definitions
    up = down = left = right = running = False
    bullet = None
    bg = Surface((32,32))
    bg.convert()
    bg.fill(BLACK)
    entities = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    collision_block_sprites = pygame.sprite.Group()
    indestructibles = pygame.sprite.Group()

    platforms = []
    collision_blocks = []
    enemies = []

     # create list of different block types
    block_types = [
    BaigeBlock(), LeftStoneBlock(), RightStoneBlock(),\
    BlueBlock(), GrayBlock(), BrightBlueBlock(), BrownBlock(),
    TopRightStoneBlock(), TopLeftStoneBlock(), CollisionBlock()
    ]

    __FPS = 70

    current_level = 1 # start at level 1
    level = get_level(current_level)

    # pack arg list to build level
    args = current_level, level, enemies, enemy_sprites, platforms, blocks,\
    entities, Platform, block_types, collision_blocks,\
    collision_block_sprites, indestructibles

    # build level and unpack return values
    platforms, blocks, entities, enemies, enemy_sprites,\
    collision_block_sprites, indestructibles, collision_blocks = build_level(*args)

    # generate size of level and set camera
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)

    elapsed_playtime = 0 # keeps track of play time in seconds
    current_life_playtime = 0
    MAX_PLAYTIME_PER_LEVEL = [0, 100, 220] # max time allowed before time runs out per level
    SPAWN_POINT_LEVEL = [0, (64, 135), (64, 64)] # x,y coordinates for each level spawn

    player = Player(SPAWN_POINT_LEVEL[1][0], SPAWN_POINT_LEVEL[1][1])
    entities.add(player) # adds player to the list of entities

    # main game loop
    main_loop = True
    game_over = False
    while main_loop:

        # handle fps and elapsed_playtime counter
        fps = timer.tick(__FPS) # max fps
        elapsed_playtime += fps / 1000.0
        current_life_playtime += fps / 1000.0
        time_remaining = float(MAX_PLAYTIME_PER_LEVEL[current_level]-current_life_playtime)

        # display fps and playtime on window
        text_display = "{0:.2f}fps    {1:.1f}s".format(timer.get_fps(), elapsed_playtime)
        pygame.display.set_caption(text_display)

        if RESET_LEVEL_FLAG == True:
            # moves to next level
            current_level += 1
            current_life_playtime = 0
            RESET_LEVEL_FLAG = False
            level = get_level(current_level)
            # package arguments for reset level
            args = screen, player, level, current_level, platforms, bullets,\
            blocks, entities, enemies, enemy_sprites, Platform,\
            block_types, collision_blocks, collision_block_sprites, indestructibles, SPAWN_POINT_LEVEL
            # call reset level
            player, platforms, blocks, collision_blocks, collision_block_sprites,\
            entities, enemies, enemy_sprites, indestructibles = reset_level(*args)
            # reset camera
            total_level_width  = len(level[0])*32
            total_level_height = len(level)*32
            camera = Camera(complex_camera, total_level_width, total_level_height)
            

        # event handler
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                game_over = True
                main_loop = False
            if e.type == KEYDOWN and e.key == K_w:
                up = True
            if e.type == KEYDOWN and e.key == K_s:
                down = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYUP and e.key == K_s:
                down = False
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False
            if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or\
            (e.type == KEYUP and e.key == K_SPACE):
                # fire on left mouse click or space bar
                bullet = Bullet(pygame.mouse.get_pos(),\
                [player.rect.x, player.rect.y, player.height], camera.state)
                # spawns bullet at the center of the player
                bullet.rect.x = player.rect.x + player.height / 2
                bullet.rect.y = player.rect.y + player.height / 2
                # adds bullet to list of bullets and list of entities
                entities.add(bullet)
                bullets.add(bullet)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                # if right click, print mouse coordinates for testing purposes
                print(pygame.mouse.get_pos())

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        # update bullets, camera, player
        bullets.update()
        camera.update(player)
        args = up, down, left, right, running, platforms, enemies, enemy_sprites, bullets, camera, collision_blocks, RESET_LEVEL_FLAG
        if player.update(*args) == "Reset Level":
            RESET_LEVEL_FLAG = True
        # update enemies
        for itr in enemies:
            if type(itr).__name__ == "GarbageCollector" or type(itr).__name__== "PySnake":
                itr.update(platforms, collision_blocks, blocks, entities)
            else:
                itr.update()

        # update any additional entities
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # handle bullet collision
        if len(bullets) > 0:
            args = bullets, blocks, platforms, entities, enemies, enemy_sprites, indestructibles
            bullets, entities, platforms, blocks, enemies, enemy_sprites = bullet_collision(*args)

        # if player has fallen off screen or hit an enemy, player has died
        if player.rect.y > 1000 or player.health <= 0 or time_remaining <= 0:
            # build argument list
            args = screen, player, level, current_level, platforms, bullets,\
            blocks, entities, enemies, enemy_sprites, Platform,\
            block_types, collision_blocks, collision_block_sprites, indestructibles, SPAWN_POINT_LEVEL
            # call player_has_died function with *args
            player, platforms, blocks, collision_blocks, collision_block_sprites,\
            entities, enemies, enemy_sprites, indestructibles = reset_level(*args)
            font = pygame.font.Font(None, 36)
            text = font.render("Try again bruh...", True, WHITE)
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
            current_life_playtime = 0

        # display player healthbar and timer
        healthBar(player.health, screen)
        display_timer_text = "%.1f" % time_remaining + "s"
        displayTimer(screen, display_timer_text)
        for enemy in enemies:
            if type(enemy).__name__ != "GarbageCollector":
                enemyHealthBar(enemy.health, enemy, screen)

        # refresh screen at end of each frame
        #pygame.display.update()
        pygame.display.flip()

    # draw game over and end the game
    gameOver(screen)
    pygame.quit()
    #raise SystemExit
    print "Game terminated..\nTotal Runtime: " + str(elapsed_playtime) + "s."

if __name__ == "__main__":
    main()
