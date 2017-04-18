#! /usr/bin/python

# import our modules
from classes import *
from functions import *
import levels
#from gifimage import *

import time, os, sys

def main():
    global cameraX, cameraY
    global RESET_LEVEL_FLAG
    RESET_LEVEL_FLAG = False
    pygame.mixer.pre_init(44100,16,2,4096)
    pygame.init()

    print ("Game loaded.")
    loading = False
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    hud = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    timer = pygame.time.Clock()

    # definitions
    up = down = left = right = running = False
    bullet = None

    current_level = 1 # start at level 1
    level = get_level(current_level)

    # helps draw background
    CURRENT_WIN_WIDTH = copy(WIN_WIDTH)
    camera_state = 0

    # loads background music
    pygame.mixer.music.load(MUSIC_DIRECTORY + "background/noah_background.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    bg = pygame.image.load(levels.BACKGROUNDS[current_level])

    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    bg = bg.convert_alpha()

    entities = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    collision_block_sprites = pygame.sprite.Group()
    indestructibles = pygame.sprite.Group()
    coin_sprites = pygame.sprite.Group()

    platforms = []
    collision_blocks = []
    enemies = []
    coins = []

     # create list of different block types
    block_types = [
    Unbreakable1(), Unbreakable2(), BaigeBlock(),\
    NeonRedBlock(), NeonWhiteBlock(), NeonBlueBlock(), NeonYellowBlock(), NeonOrangeBlock(), NeonGreenBlock(),\
    BlueBlock(), GrayBlock(), BrightBlueBlock(), BrownBlock(),
    CollisionBlock(), CornerPatrolBlock()
    ]

    __FPS = 70

    # pack arg list to build level
    args = current_level, level, enemies, enemy_sprites, platforms, blocks,\
    entities, Platform, block_types, collision_blocks,\
    collision_block_sprites, indestructibles, coins, coin_sprites

    # build level and unpack return values
    platforms, blocks, entities, enemies, enemy_sprites,\
    collision_block_sprites, indestructibles, collision_blocks,\
    coins, coin_sprites = build_level(*args)

    # generate size of level and set camera
    pygame.total_level_width  = len(level[0])*32
    pygame.total_level_height = len(level)*32
    camera = Camera(complex_camera, pygame.total_level_width, pygame.total_level_height)

    elapsed_playtime = 0 # keeps track of play time in seconds
    current_life_playtime = 0
    current_score, score = 0, 0
    lives = copy(MAX_LIVES)
    player = Player(levels.SPAWN_POINT_LEVEL[1][0], levels.SPAWN_POINT_LEVEL[1][1])
    entities.add(player) # adds player to the list of entities

    """ main game loop """
    main_loop = True
    game_over = False
    while main_loop:
        """ handle fps and elapsed_playtime counter """
        fps = timer.tick(__FPS) # max fps
        elapsed_playtime += fps / 1000.0
        current_life_playtime += fps / 1000.0
        time_remaining = float(levels.MAX_PLAYTIME_PER_LEVEL[current_level]-current_life_playtime)

        """ display fps and playtime on window """
        text_display = "Time remaining: %.1f" % time_remaining + "s"
        text_display += "          Current score: " + str(current_score).zfill(8)
        text_display += "                                  "
        text_display += "FPS: {0:.2f}          Elapsed time: {1:.1f}s".format(timer.get_fps(), elapsed_playtime)
        pygame.display.set_caption(text_display)

        """ PLAYER BEAT THE LEVEL """
        if RESET_LEVEL_FLAG == True:
            # moves to next level
            current_level += 1
            # changes background
            bg = pygame.image.load(levels.BACKGROUNDS[current_level])
            bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
            bg = bg.convert_alpha()

            current_life_playtime = 0
            camera_state = 0
            RESET_LEVEL_FLAG = False
            level = get_level(current_level)
            # package arguments for reset level
            args = screen, player, level, current_level, platforms, bullets,\
            blocks, entities, enemies, enemy_sprites, Platform,\
            block_types, collision_blocks, collision_block_sprites, indestructibles, levels.SPAWN_POINT_LEVEL
            # call reset level
            player, platforms, blocks, collision_blocks, collision_block_sprites,\
            entities, enemies, enemy_sprites, indestructibles = reset_level(*args)
            # reset camera
            pygame.total_level_width  = len(level[0])*32
            pygame.total_level_height = len(level)*32
            camera = Camera(complex_camera, pygame.total_level_width, pygame.total_level_height)

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
            #if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or\
            #(e.type == KEYUP and e.key == K_SPACE):
            #    bullet = Bullet(pygame.mouse.get_pos(),\
            #    [player.rect.x, player.rect.y, player.attack_height], camera.state, player.facing_right)
            #    # spawns bullet at the center of the player
            #    bullet.rect.x = player.rect.x + player.attack_height/2
            #    bullet.rect.y = player.rect.y - player.attack_height/2
            #    entities.add(bullet)
            #    bullets.add(bullet)
            if e.type == KEYDOWN and e.key == K_f and not left and not right:# and player.facing_right == True):
                bullet = Bullet(pygame.mouse.get_pos(),\
                [player.rect.x, player.rect.y, player.attack_height], camera.state, player.facing_right, 'strong')
                if player.facing_right:
                    bullet.rect.x = player.rect.x + player.attack_height/2 + 10# - player.height/2# / 2
                else:
                    bullet.rect.x = player.rect.x - player.attack_height/2 - 10
                bullet.rect.y = player.rect.y - player.attack_height/2 + 10# + player.height/2# / 2
                entities.add(bullet)
                bullets.add(bullet)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                # if right click, print mouse coordinates for testing purposes
                print(pygame.mouse.get_pos())

        """ move background while camera moves """
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
            if type(enemy).__name__ == "GarbageCollector" or \
               isinstance(enemy, PySnake) or \
               isinstance(enemy, Ghost):
                enemy.update(platforms, collision_blocks, blocks, entities)
                if enemy.dead():
                    delete_enemy(enemy, enemy_sprites, enemies, entities)
#                if (isinstance(enemy, PySnake) and enemy.hit and enemy.dying_counter >= 55) or \
#                   (isinstance(enemy, Ghost) and outOfLevel(enemy.rect, pygame.total_level_width, pygame.total_level_height)):
#                    deleteEnemy(enemy, enemy_sprites, enemies, entities)
            else:
                enemy.update()

        # update coins
        for c in coins:
            if c.update(player):
                coins.remove(c)
                coin_sprites.remove(c)
                entities.remove(c)
                current_score += 10

        # update any additional entities
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # handle bullet collision
        if len(bullets) > 0:
            args = bullets, blocks, platforms, entities, enemies, enemy_sprites, indestructibles, score
            bullets, entities, platforms, blocks, enemies, enemy_sprites, score = bullet_collision(*args)

        # display loading when screen lags
        if timer.get_fps() < 60 and not loading and lives > 0:
            #loading(screen, cache)
            print('Loading...')
            loading = True
        elif timer.get_fps() >= 60 and loading and lives > 0:
            loading = False

        # if player has fallen off screen or hit an enemy, player has died
        if player.rect.y > 1000 or player.health <= 0 or time_remaining <= 0:

            CURRENT_WIN_WIDTH = copy(WIN_WIDTH)
            lives -= 1 # count number of deaths
            # if player has run out of lives, set player back to level 1 and reset score
            if lives <= 0:
                current_level = 1
                bg = pygame.image.load(levels.BACKGROUNDS[current_level])
                bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
                bg = bg.convert_alpha()
                current_score, score, current_level, lives = 0, 0, 1, MAX_LIVES
                level = get_level(current_level)
                # generate size of level and set camera
                pygame.total_level_width  = len(level[0])*32
                pygame.total_level_height = len(level)*32
                camera = Camera(complex_camera, pygame.total_level_width, pygame.total_level_height)
                gameOver(screen, cache)
            else:
                text = get_msg('Try again bruh...', cache)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])
            # build argument list
            args = screen, player, level, current_level, platforms, bullets,\
            blocks, entities, enemies, enemy_sprites, Platform,\
            block_types, collision_blocks, collision_block_sprites, indestructibles, levels.SPAWN_POINT_LEVEL,\
            coins, coin_sprites
            # call reset level function with *args
            player, platforms, blocks, collision_blocks, collision_block_sprites,\
            entities, enemies, enemy_sprites, indestructibles, coins, coin_sprites = reset_level(*args)

            current_life_playtime = 0


        
        #current_score = scrollScore(current_score, score) # animate scrolling effect on score
        #current_score = score # score no scrolling

        # display player healthbar, timer, score, and lives
        healthBar(player.health, screen, cache)
        #displayTimer(screen, "%.1f" % time_remaining + "s", current_score, cache)
        displayLives(screen, lives, cache)
        # display enemy healthbar
        for enemy in enemies:
            if enemy.healthTrigger == True:
                if type(enemy).__name__ != "GarbageCollector":
                    enemyHealthBar(enemy.health, enemy, screen, camera.state)
                else:
                    garbageCollectorHealthBar(enemy, screen, camera.state)

        # refresh screen at end of each frame
        pygame.display.flip()

    # draw game over and end the game
    gameOver(screen, cache)
    pygame.quit()
    print "Game terminated..\nTotal Runtime: " + str(elapsed_playtime) + "s."

if __name__ == "__main__":
    main()
