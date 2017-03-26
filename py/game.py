#! /usr/bin/python

# import our modules
from functions import *
import levels
from classes import *


import time, os, sys

def main():
    global cameraX, cameraY
    pygame.init()

    # display loading splash screen
    print ("Loading game...")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.font.init()
    load = pygame.display.set_mode((500,80),pygame.NOFRAME)
    _background = pygame.Surface(load.get_size())
    
    #healthbar = pygame.Surface((WIN_WIDTH/4, WIN_HEIGHT/4))

    _background.fill((0,0,0))
    load.blit(_background, (0,0))
    load.blit(pygame.font.Font(None, 72)\
    .render('Loading...', 1, (255,255,255)),(90,10))
    pygame.display.update()
    time.sleep(1)

    print ("Game loaded.")
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)


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
    player = Player(64, 135)
    entities.add(player) # adds player to the list of entities
    platforms = []
    collision_blocks = []

     # create list of different block types
    block_types = [
    BaigeBlock(), LeftStoneBlock(), RightStoneBlock(),\
    BlueBlock(), GrayBlock(), BrightBlueBlock(), BrownBlock(),
    TopRightStoneBlock(), TopLeftStoneBlock(), CollisionBlock()
    ]
    __FPS = 70

    level = get_level(1) # set level
    #enemies = get_enemies(level) # set enemy list
    enemies = []
    # add enemies to sprite list

    # build arg list
    args = level, enemies, enemy_sprites, platforms, blocks,\
    entities, Platform, block_types, collision_blocks,\
    collision_block_sprites, indestructibles
    # build level
    platforms, blocks, entities, enemies,\
    enemy_sprites, collision_block_sprites, indestructibles = build_level(*args)

    # generate size of level and set camera
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    playtime = 0 # keeps track of play time in seconds

    # main game loop
    main_loop = True
    while main_loop:


        # handle fps and playtime counter
        fps = timer.tick(__FPS) # max fps
        playtime += fps / 1000.0 # add second to playtime
        text_display = "{0:.2f}fps    {1:.2f}s".format(timer.get_fps(), playtime)
        pygame.display.set_caption(text_display)

        # event handler
        for e in pygame.event.get():
            if e.type == QUIT:
                main_loop = False

            if e.type == KEYDOWN and e.key == K_ESCAPE:
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

            # fire on left mouse click or space bar
            if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or\
            (e.type == KEYUP and e.key == K_SPACE):
                bullet = Bullet(pygame.mouse.get_pos(),\
                [player.rect.x, player.rect.y, player.height], camera.state)
                # spawns bullet at the center of the player
                bullet.rect.x = player.rect.x + player.height / 2
                bullet.rect.y = player.rect.y + player.height / 2
                # adds bullet to list of bullets and list of entities
                entities.add(bullet)
                bullets.add(bullet)

            # if right click, print mouse coordinates for testing purposes
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                print(pygame.mouse.get_pos())

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        # update bullets, camera, player, and enemies
        bullets.update()
        camera.update(player)
        player.update(up, down, left, right, running, platforms, enemies, enemy_sprites, bullets)
        for itr in enemies:
            if type(itr).__name__ == "GarbageCollector":
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
        if player.rect.y > 1000 or player.health <= 0:#sprite.spritecollide(player, enemy_sprites, True):
            respawn_text = "Try again n00b..."
            # build argument list
            args = screen, player, level, platforms, bullets,\
            blocks, entities, enemies, enemy_sprites, respawn_text,\
            Platform, block_types, collision_blocks, collision_block_sprites, indestructibles
            # call player_has_died function with *args
            player, platforms, blocks, collision_blocks, collision_block_sprites,\
            entities, enemies, enemy_sprites, indestructibles = player_has_died(*args)
            pygame.time.delay(100)

        #healthPoints(WIN_WIDTH/2, WIN_HEIGHT/2, player.health, _background)

        # refresh screen at end of each frame
        healthBar(player.health, screen)
        #pygame.display.update()
        pygame.display.flip()


    # game has ended
    pygame.quit()
    raise SystemExit, "Game terminated..\nTotal Runtime: " + str(playtime) + "s."

if __name__ == "__main__":
    main()
