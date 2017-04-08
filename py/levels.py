#!/usr/bin/Python

""" BLOCKTYPES """
# E = Baige Block
# C = Brown Block
# A = Blue Block
# B = Bright Blue Block
# D = Gray Block

# neon blocks
# r = red neon block
# w = white neon block
# b = blue neon block
# y = yellow neon block
# o = orange neon block
# g = green neon block

# unbreakables
# n = unbreakable 1
# m = unbreakable 2

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

#from classes import *

""" lists to store levels and enemies """
get_levels = [0] #, get_enemies = [0], [0] # init first index to 0

level_1 = [
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                                                        B",
"nn                                                                                        Xnn                             B",
"nn                 nnnnnn                                                          Xnn                                    B",
"nn    	                                                                                   Xnn                             B",
"nn             n            n                                                                        Xnn                  B",
"nn             nQ    2     Qn            Q  2                2  Q                            Xnn                          B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]

# add enemies/levels to list
get_levels.append(level_1)

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

# add enemies/levels to list
get_levels.append(level_2)
