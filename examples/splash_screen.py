#! /usr/bin/env python
import pygame
import time
import os, sys
print 'Splash load...'
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500,80),pygame.NOFRAME)
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
screen.blit(background, (0,0))
screen.blit(pygame.font.Font(None, 72).render('Loading...', 1, (255,255,255)),(90,10))
pygame.display.update()
time.sleep(5)