#!/usr/bin/Python

""" BLOCKTYPES """
# E = Baige Block
# C = Brown Block
# A = Blue Block
# B = Bright Blue Block
# D = Gray Block

# L = Top left stone block
# R = Top right stone block
# M = left stone block
# N = right stone block

# X = Exit Block # TRIGGERS LEVEL CHANGE
# O = blank patrol platform # PLAYER REMOVES THESE BLOCKS WHEN COLLIDING WITH THEM
# Q = Corner patrol platform # THESE BLOCKS ARE PERMANENT FOR EACH LEVEL

""" ENEMIES """
# 1 = Garbage Collector
# 2 = Green Snake
# 3 = Red Snake
# 4 = Blue Snake
# 5 = Purple Snake
# 6 = Red Ghost
# 7 = White Ghost

# GarbageCollector(x,y)

from classes import *

""" lists to store levels and enemies """
get_levels, get_enemies = [0], [0] # init first index to 0

level_1 = [
"LR                                                                                                                                                                                                                                                                                                                                                                                          ",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                   1234567                                                              XLR                                                                                                                                                                                                                                                                                              B",
"LR                                                                                        XLR                                                                                                                                                                                                                                                                                              B",
"LR    	                                                                                   XLR                                                                                                                                                                                                                                                                                              B",
"LR                                                                                        XLR                                                                                                                                                                                                                                                                                              B",
"LRQ       O                           O                                           O       XLR                                                                                                                                                                                                                                                                                              B",
"LRBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]

# Generate level 1 enemies
#level_1_enemies = [
#GarbageCollector(100,0), PySnake(450, 268)
#]

# add enemies/levels to list
get_levels.append(level_1)
#get_enemies.append(level_1_enemies)

level_2 = [
"DD                                                                                                                                                                                                                                                                                                                                                                                          ",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                                                                                                                                                                                                                                                                                                                                                                         B",
"DD                                O                                                                                                                                                                                                                                                                                                                                                        B",
"DD          DABECDABDABDABDDABDABDAB                                                                                                                                                                                                                                                                                                                                                       B",
"DD        DABECDABDABDABDDABDABDAB                                                                                                                                                                                                                                                                                                                                                         B",
"DD          DABECDABDABDABDDABDABDAB                                                                                                                                                                                                                                                                                                                                                       B",
"DDO   DA    DABECDABDABDABDDABDABDAB                                                                                                                                                                                                                                                                                                                                                       B",
"DDOO DABECDABDABDABDDABDABDAB                                                                                                                                                                                                                                                                                                                                                              B",
"DDODDDDDDD                O                                                                                                                                                                                                                                                                                                                                                                B"
]

# Generate level 2 enemies
level_2_enemies = [PySnake(463, 305), GarbageCollector(351, 544)
]

# add enemies/levels to list
get_levels.append(level_2)
get_enemies.append(level_2_enemies)
