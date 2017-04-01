#! /usr/bin/python

# import our modules
from functions import *
import levels
from classes import *
#from gifimage import *

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

    current_level = 1 # start at level 1
    level = get_level(current_level)

    # Define list of backgrounds for the levels
    BACKGROUNDS = [0, 'background2.png', 'sample_background.jpg']
    for i in range(1, len(BACKGROUNDS)):
        BACKGROUNDS[i] = '../sprites/backgrounds/' + BACKGROUNDS[i]

    # helps draw background
    CURRENT_WIN_WIDTH = copy(WIN_WIDTH)
    camera_state = 0

    bg = pygame.image.load(BACKGROUNDS[current_level])
    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    bg = bg.convert_alpha()

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
    TopRightStoneBlock(), TopLeftStoneBlock(), CollisionBlock(), CornerPatrolBlock()
    ]

    __FPS = 70

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
    current_score, score = 0, 0
    lives = copy(MAX_LIVES)
    MAX_PLAYTIME_PER_LEVEL = [0, 16, 360] # max time allowed before time runs out per level
    SPAWN_POINT_LEVEL = [0, (64, 135), (64, 64)] # x,y coordinates for each level spawn

    player = Player(SPAWN_POINT_LEVEL[1][0], SPAWN_POINT_LEVEL[1][1])
    entities.add(player) # adds player to the list of entities

    """ main game loop """
    main_loop = True
    game_over = False
    while main_loop:

        """ handle fps and elapsed_playtime counter """
        fps = timer.tick(__FPS) # max fps
        elapsed_playtime += fps / 1000.0
        current_life_playtime += fps / 1000.0
        time_remaining = float(MAX_PLAYTIME_PER_LEVEL[current_level]-current_life_playtime)

        """ display fps and playtime on window """
        text_display = "{0:.2f}fps    {1:.1f}s".format(timer.get_fps(), elapsed_playtime)
        pygame.display.set_caption(text_display)

        """ PLAYER BEAT THE LEVEL """
        if RESET_LEVEL_FLAG == True:
            # moves to next level
            current_level += 1
            # changes background
            bg = pygame.image.load(BACKGROUNDS[current_level])
            bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
            bg = bg.convert_alpha()
            current_life_playtime = 0
            camera_state = 0
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
            

        """ event handler """
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                game_over = True
                main_loop = False
            if e.type == KEYDOWN and e.key == K_w:
                up = True
                player.jump = True
                player.images = player.jumping
                player.frame_counter, player.counter = 0, 0
            if e.type == KEYDOWN and e.key == K_s:
                down = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
                player.images = player.running
                player.frame_counter, player.counter = 0, 0
            if e.type == KEYDOWN and e.key == K_d:
                right = True
                player.images = player.running
                player.frame_counter, player.counter = 0, 0
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYUP and e.key == K_s:
                down = False
            if e.type == KEYUP and e.key == K_d:
                right = False
                player.images = player.standing
                player.frame_counter, player.counter = 0, 0
            if e.type == KEYUP and e.key == K_a:
                left = False
                player.images = player.standing
                player.frame_counter, player.counter = 0, 0
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False
            if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or\
            (e.type == KEYUP and e.key == K_SPACE):
                bullet = Bullet(pygame.mouse.get_pos(),\
                [player.rect.x, player.rect.y, player.height], camera.state)
                # spawns bullet at the center of the player
                bullet.rect.x = player.rect.x + player.height/2
                bullet.rect.y = player.rect.y + player.height/2
                entities.add(bullet)
                bullets.add(bullet)
            if (e.type == KEYDOWN and e.key == K_f):
                bullet = Bullet(pygame.mouse.get_pos(),\
                [player.rect.x, player.rect.y, player.height], camera.state, 'strong')
                bullet.rect.x = player.rect.x + player.height - player.height/2# / 2
                bullet.rect.y = player.rect.y - player.height + player.height/2# / 2
                entities.add(bullet)
                bullets.add(bullet)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                # if right click, print mouse coordinates for testing purposes
                print(pygame.mouse.get_pos())

        """ move background """
        if -1 * camera.state[0] >= CURRENT_WIN_WIDTH:#_RIGHT:
            CURRENT_WIN_WIDTH += WIN_WIDTH
            camera_state = camera.state[0]
        elif -1 * camera.state[0] < CURRENT_WIN_WIDTH:#_LEFT:
            CURRENT_WIN_WIDTH -= WIN_WIDTH
            camera_state = camera.state[0]

        """ DRAW BACKGROUND """
        # if player is moving right
        if camera.state[0] <= camera_state:
            camera_state = camera.state[0]
            screen.blit(bg, (CURRENT_WIN_WIDTH - WIN_WIDTH + camera.state[0],0))
            screen.blit(bg,(CURRENT_WIN_WIDTH + camera.state[0],0))
        # if player is moving left
        elif camera.state[0] > camera_state:
            camera_state = camera.state[0]
            screen.blit(bg, (CURRENT_WIN_WIDTH - WIN_WIDTH + camera.state[0],0))
            screen.blit(bg,(CURRENT_WIN_WIDTH + camera.state[0],0))

        """ update bullets, camera """
        bullets.update()
        camera.update(player)

        """ update player and check if reached next level """
        args = up, down, left, right, running, platforms, enemies, enemy_sprites, bullets, camera, collision_blocks, RESET_LEVEL_FLAG, entities
        result = player.update(*args)
        # remove patrol blocks, but not corner colision blocks
        if result != None and result in collision_blocks:
            if result.patrol == False:
                collision_blocks.remove(result)
                collision_block_sprites.remove(result)
                entities.remove(result)
        # reset level if player reached end of level
        elif result != None and result == "Reset Level":
            RESET_LEVEL_FLAG = True

        # update enemies
        for enemy in enemies:
            # count frames to stop displaying healthbar
            enemy.health_counter += 1
            if enemy.health_counter >= MAX_HEALTH_FRAMES:
                enemy.health_counter = 0
                enemy.healthTrigger = False
            if type(enemy).__name__ == "GarbageCollector" or type(enemy).__name__== "PySnake":
                enemy.update(platforms, collision_blocks, blocks, entities)
            else:
                enemy.update()

        # update any additional entities
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # handle bullet collision
        if len(bullets) > 0:
            args = bullets, blocks, platforms, entities, enemies, enemy_sprites, indestructibles, score
            bullets, entities, platforms, blocks, enemies, enemy_sprites, score = bullet_collision(*args)

        # if player has fallen off screen or hit an enemy, player has died
        if player.rect.y > 1000 or player.health <= 0 or time_remaining <= 0:
            font = pygame.font.Font(None, 36)
            CURRENT_WIN_WIDTH = copy(WIN_WIDTH)
            lives -= 1 # count number of deaths
            # if player has run out of lives, set player back to level 1 and reset score
            if lives <= 0:
                current_level = 1
                current_score, score, current_level, lives = 0, 0, 1, MAX_LIVES
                level = get_level(current_level)
                # generate size of level and set camera
                total_level_width  = len(level[0])*32
                total_level_height = len(level)*32
                camera = Camera(complex_camera, total_level_width, total_level_height)
                gameOver(screen)
            else:
                text = font.render("Try again bruh...", True, WHITE)
            # build argument list
            args = screen, player, level, current_level, platforms, bullets,\
            blocks, entities, enemies, enemy_sprites, Platform,\
            block_types, collision_blocks, collision_block_sprites, indestructibles, SPAWN_POINT_LEVEL
            # call player_has_died function with *args
            player, platforms, blocks, collision_blocks, collision_block_sprites,\
            entities, enemies, enemy_sprites, indestructibles = reset_level(*args)
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
            current_life_playtime = 0
            

        # animate scrolling effect on score
        current_score = scrollScore(current_score, score)

        # display player healthbar, enemy healthbar, timer, score, and lives
        healthBar(player.health, screen)
        #display_timer_text = "%.1f" % time_remaining + "s"
        displayTimer(screen, "%.1f" % time_remaining + "s", current_score)
        displayLives(screen, lives)
        for enemy in enemies:
            if enemy.healthTrigger == True:
                if type(enemy).__name__ != "GarbageCollector":
                    enemyHealthBar(enemy.health, enemy, screen, camera.state)
                else:
                    garbageCollectorHealthBar(enemy, screen, camera.state)
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
