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
    load.blit(pygame.font.Font(None, 72).render('Loading...', 1, (255,255,255)),(90,10))
    pygame.display.update()
    time.sleep(0.5)

    print ("Game loaded.")
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    timer = pygame.time.Clock()

    # defining some useful objects
    up = down = left = right = running = False
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
    build_level(level, platforms, blocks, entities, Platform, ExitBlock)

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
            if e.type == pygame.MOUSEBUTTONDOWN or (e.type == KEYUP and e.key == K_SPACE):
                bullet = Bullet(pygame.mouse.get_pos(), [player.rect.x, player.rect.y, player.height], camera.state)
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

        # check bullet collision
        for bullet in bullets:
            # See if it hit a block
            block_hit_list = sprite.spritecollide(bullet, blocks, True)
 
            # For each block hit, remove the bullet or cause collision
            for block in block_hit_list:
                bullets.remove(bullet)
                entities.remove(bullet)
                if block in platforms:
                    platforms.remove(block)

            # Remove the bullet if it flies off the screen
            if bullet.rect.y > 1000:
                bullets.remove(bullet)
                entities.remove(bullet)

        # if player has fallen off screen, player has died
        if player.rect.y > 1000:

            # reset sprites and re-add player to game
            platforms = []
            blocks.empty()
            entities.empty()
            entities.add(player)

            # rebuild level
            build_level(level, platforms, blocks, entities, Platform, ExitBlock)

            # respawn player
            player.rect.x = 32
            player.rect.y = 32

            # render body text
            bodylines = [
                [(140, 100), "Try again n00b..."]]
            bodyfont = getFont(None, 22)
            for line in bodylines:
               position, text = line
               putText(screen, bodyfont, text, position,
                    forecolour = WHITE,
                    backcolour = BLACK )
            time.sleep(1)

        # refresh screen at end of frame
        pygame.display.update()

    pygame.quit()
    raise SystemExit, "Game terminated..\nTotal Runtime: " + str(playtime) + "s."

if __name__ == "__main__":
    main()