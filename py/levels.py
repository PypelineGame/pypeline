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

""" ENEMIES """
# GarbageCollector(x,y)

from classes import *

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
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR    DABEC                                                                                                                                                                                                                                                                                                                                                                                B",
"LR   DABEC                                                                                                                                                                                                                                                                                                                                                                                 B",
"LRO                      O                                                                                                                                                                                                                                                                                                                                                                 B",
"LRBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]

# Generate level 1 enemies
level_1_enemies = [
GarbageCollector(121,264),
]


level_2 = [
"",
"",
""
]

# Generate level 2 enemies
level_2_enemies = [
]