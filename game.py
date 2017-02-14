#! /usr/bin/python

# import our modules
from classes import *
from functions import *

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
    _background.fill((0,0,0))
    load.blit(_background, (0,0))
    load.blit(pygame.font.Font(None, 72)\
    .render('Loading...', 1, (255,255,255)),(90,10))
    pygame.display.update()

    player_is_dead = False

    print ("Game loaded.")
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    timer = pygame.time.Clock()

    # defining some useful objects
    up = down = left = right = running = False
    #a_bullet_has_been_fired = False
    bullet = None
    bg = Surface((32,32))
    bg.convert()
    bg.fill(BLACK)
    entities = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    player = Player(32, 32)
    entities.add(player) # adds player to the list of entities
    platforms = []
    x, y = 0, 0

    level = get_level(1)
    args = level, platforms, blocks, entities, Platform, ExitBlock
    platforms, blocks, entities = build_level(*args)

    # generate size of level and set camera
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    playtime = 0 # keeps track of play time in seconds

    # main game loop
    main_loop = True
    while main_loop:
        __FPS = 100
        fps = timer.tick(__FPS) # max fps
        playtime += fps / 1000.0 # add second to playtime
        text_display = "{0:.2f}fps    {1:.2f}s".format(timer.get_fps(), playtime)
        pygame.display.set_caption(text_display)

        #if player_is_dead:
        #    player_is_dead = False
        #    time.sleep(0.5)

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

            # fire if mouse click or space bar is hit
            if e.type == pygame.MOUSEBUTTONDOWN or\
            (e.type == KEYUP and e.key == K_SPACE):
                #a_bullet_has_been_fired = True
                bullet = Bullet(pygame.mouse.get_pos(),\
                [player.rect.x, player.rect.y, player.height], camera.state)
                bullet.rect.x = player.rect.x + player.height / 2
                bullet.rect.y = player.rect.y + player.height / 2
                entities.add(bullet)
                bullets.add(bullet)

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        # update bullets and camera
        bullets.update()
        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # handle bullet collision
        #if a_bullet_has_been_fired:
        if len(bullets) > 0:
            args = bullets, blocks, platforms, entities
            bullets, entities, platforms, blocks = bullet_collision(*args)

        # if player has fallen off screen, player has died
        if player.rect.y > 1000:
            respawn_text = "Try again n00b..."
            args = screen, player, level, platforms, bullets,\
            blocks, entities, respawn_text, Platform, ExitBlock
            platforms, blocks, entities,\
            player.rect.x, player.rect.y = player_has_died(*args)
            player_is_dead = True

        # refresh screen at end of frame
        pygame.display.update()

    pygame.quit()
    raise SystemExit, "Game terminated..\nTotal Runtime: " + str(playtime) + "s."

if __name__ == "__main__":
    main()