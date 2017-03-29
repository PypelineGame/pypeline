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
# O = blank collision platform
# X = Exit Block

""" ENEMIES """
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
"LR                                                                                        XLR                                                                                                                                                                                                                                                                                              B",
"LR                                                                                        XLR                                                                                                                                                                                                                                                                                              B",
"LR    	                                                                                   XLR                                                                                                                                                                                                                                                                                              B",
"LR                                                                                        XLR                                                                                                                                                                                                                                                                                              B",
"LRO                                   O                                           O       XLR                                                                                                                                                                                                                                                                                              B",
"LRBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]

# Generate level 1 enemies
level_1_enemies = [
GarbageCollector(821,264), PySnake(450, 268)
]

# add enemies/levels to list
get_levels.append(level_1)
get_enemies.append(level_1_enemies)

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
"DD        DABEC                                                                                                                                                                                                                                                                                                                                                                            B",
"DD          LR                                                                                                                                                                                                                                                                                                                                                                             B",
"DDO   DA    LR                                                                                                                                                                                                                                                                                                                                                                              B",
"DDOO DABECDDLR                                                                                                                                                                                                                                                                                                                                                                             B",
"DDODDDDDDD                O                                                                                                                                                                                                                                                                                                                                                                B"
]

# Generate level 2 enemies
level_2_enemies = [PySnake(463, 305), GarbageCollector(351, 544)
]

# add enemies/levels to list
get_levels.append(level_2)
get_enemies.append(level_2_enemies)