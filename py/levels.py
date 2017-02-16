#!/usr/bin/Python

""" BLOCKTYPES """
# M = Mossy block
# B = Baige Block
# B = Baige Round Block

""" ENEMIES """
# GARBAGE_COLLECTOR

from classes import *

level_1 = [
"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
"B                                                                                                                                                                                                                                                                                                                                                                                          B",
"B                                                                                                                                                                                                                                                                                                                                                                                          B",
"B                                                                                                                                                                                                                                                                                                                                                                                          B",
"B                                                                                                                                                                                                                                                                                                                                                                                          B",
"B                                                                                                                                                                                                                                                                                                                                                                                          B",
"B                                      B                                                                                                                                                                                                                                                                                                                                                   B",
"B           B             R     B  BBB  BB B               BBBB                                                                                                                                                                                                                                                                                                                            B",
"B           BB        R                     B      BBBBBB        BB                               E                                                                                                                                                                                                                                                                                        B",
"B           B       R                        BBB                   BBBB                   BBBBB                                                                                                                                                                                                                                                                                            B",
"B                                                                        BBBB        BBBB                                                                                                                                                                                                                                                                                                  B",
"B           B    R         B                                                                                                                                                                                                                                                                                                                                                               B",
"B           B   R          B                                                                                                                                                                                                                                                                                                                                                               B",
"B           B  R           B                                                                                                                                                                                                                                                                                                                                                               B",
"B   BBBBBBBBBBBBBBBBBBBBBBBBBBBB                                                                                                                                                                                                                                                                                                                                                           B",
"B           RR                                                                                                                                                                                                                                                                                                                                                                             B",
"B          R                                                                                                                                                                                                                                                                                                                                                                               B",
"B         R                                                                                                                                                                                                                                                                                                                                                                                B",
"B        R                                                                                                                                                                                                                                                                                                                                                                                 B",
"BBBBBBBBB    B BBBBBBBBBBBB                                          BBBBB          RRRBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]

# Generate level 1 enemies
level_1_enemies = [
GarbageCollector(273,380),
]
