#! /usr/bin/python

from classes import *
import levels

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

def build_level(level, platforms, blocks, entities, Platform, ExitBlock):
    exit_block_provided = False
    x, y = 0, 0
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                blocks.add(p)
                entities.add(p)
            if col == "E":
                exit_block_provided = True
                e = ExitBlock(x, y)
                platforms.append(e)
                blocks.add(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    # generates a random exit block if one is not provided
    if exit_block_provided == False:
        coord_x = randrange(len(row))
        coord_y = randrange(350)
        e = ExitBlock(coord_x, coord_y)
        platforms.append(e)
        blocks.add(e)
        entities.add(e)

# Create a font
# When font name = None, Pygame returns a default font
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