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
"                                                                                                                                                                                                                                                                                                                                                                                            ",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                 DDDDDDDLR                                                                                                                                                                                                                                                                                                                                                               B",
"LR                 DDDDDDDLR                                                                                                                                                                                                                                                                                                                                                               B",
"LR                 DDDDDDDLR                                                                                                                                                                                                                                                                                                                                                               B",
"LR                 DDDDDDDLR                                                                                                                                                                                                                                                                                                                                                               B",
"LR                 DDDDDDDLR                                                                                                                                                                                                                                                                                                                                                               B",
"LRAAAAAAAAAAAAAAAAAAAAAAAA                                                                                                                                                                                                                                                                                                                                                                 B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LRLRLRLRLRLRLRLRLRLRLRLRLR                                                                                                                                                                                                                                                                                                                                                                 B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LR                                                                                                                                                                                                                                                                                                                                                                                         B",
"LRO                      O                                                                                                                                                                                                                                                                                                                                                                 B",
"LRBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]

# Generate level 1 enemies
level_1_enemies = [
GarbageCollector(400,555),
]
