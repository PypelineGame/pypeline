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

# X = Top of door (Exit Block) # TRIGGERS LEVEL CHANGE
# Y = Bottom of door (Exit Block) # TRIGGERS LEVEL CHANGE

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

import classes

""" lists to store levels and enemies """
get_levels = [0] #, get_enemies = [0], [0] # init first index to 0

MAX_PLAYTIME_PER_LEVEL = [0, 8000, 360, 360] # max time allowed before time runs out per level
SPAWN_POINT_LEVEL = [0, (64, 700), (64, 64), (64, 64)] # x,y coordinates for each level spawn
BACKGROUNDS = [0, 'background5.jpg', 'beauty.jpg', 'forest_day.png', 'montanha.png']
# Get list of backgrounds for the levels
for i in range(1, len(BACKGROUNDS)):
    BACKGROUNDS[i] = classes.SPRITES_DIRECTORY + 'backgrounds/' + BACKGROUNDS[i]

level_1 = [

"gg                                                                                  gg",
"gg                                                                                  gg",
"gg                                                                                  gg",
"gg             o                                                                    gg",
"gg            Xo                                                                    gg",
"gg            Yo                                                                    gg",
"gg           bbb                                                                    gg",
"gg    bbbbbbb                                                                       gg",
"gg                                                                                  gg",
"gg n                                                                                gg",
"gg  n  Q  4    Q                                                                    gg",
"gg   n  bbbbbbb  nQ  5  Q Q 5   Q  Q  5  Q  Q  5    Q Q    4  Qbbbbb                gg",
"gg                bbbbbb   bbbbb    bbbbb    bbbbbbb   bbbbbbbb                     gg",
"gg                                                                    oo            gg",
"gg     ooooooo                                                    oooo              gg",
"gg    o                                                          o   n              gg",
"gg   o                                                         oo    n              gg",
"gg     Q          1          Q                               Qo      n              gg",
"ggb     bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb       n              gg",
"gg b                                                                 w    bbbb      gg",
"gg  b                                                            O   w              gg",
"gg   bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb            gg",
"gg                                 7                     7              b           gg",
"gg                                                                       b          gg",
"gg                                                                        b         gg",
"gg                                 7                     7                 b        gg",
"gg                 bbbbbbbb                                                 b       gg",
"gg                                                                             o    gg",
"gg              o            o                           7                     n    gg",
"gg              oQ    2     QoQ           O  5       O        3  O            Qn   Qgg",
"ggDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDgg"]

# add enemies/levels to list
get_levels.append(level_1)

level_5 = [
"nn                                                                                                                                         B",
"nn                                                                                                                                         B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                    7                                                                                                     B",
"nn                                     7                                                                                                    B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn            7                                                                                                                             B",
"nn                                           DDDDDDDDDDDDDDDD          7                                                                    B",
"nn                                D          D              D                                                                               B",
"nn                                D          D            7 D                                                                               B",
"nn                   7           D                                                                 Q  5   Q                                 B",
"nn                           7   D          D              D     7   O        1  Q       7            nnnnnn                                B",
"nn          O    5   5 Q       D     7   7DO      5     QD          QDDDDDDDDDD              n                                              B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn     nnnnnnnnnnnnnnnnnnnn          nnnnnnnnnnnnnnnnnnnnnnnnnnnn B"
"nn                                                                        nn                                 n                              B",
"nn                                                  7                      n                                 n                              B",
"nn                                   7                      7              n                                 n                              B",
"nn                                                                         nQ                               Qn                              B",
"nn                                                                         nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn                              B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]

# add enemies/levels to list
get_levels.append(level_5)

level_3 = [
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
"nn             6                                                                                                          B",
"nn            7                                                                                                           B",
"nn         7                                                                                                              B",
"nn                                                                                      Xnn                               B",
"nn               nnnnnn                                                          Xnn                                      B",
"nn                                                                                      Xnn                               B",
"nn            n            n                                                                        Xnn                   B",
"nn            nQ    5     Qn            Q  5                5  Q                            Xnn                           B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]

# add enemies/levels to list
get_levels.append(level_3)
