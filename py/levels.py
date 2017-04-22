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

# c = coin
# p - purple coin

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
"gg    c c c cbbb                                                                    gg",
"gg    bbbbbbb                                                                       gg",
"gg c                                                                                gg",
"gg nc                                                                               gg",
"gg  nc Q  4    Q c                                               c                  gg",
"gg   n  bbbbbbb  nQ  5  Q Q 5   Q  Q  5  Q  Q  5    Q Q    4  Qbbbbb                gg",
"gg                bbbbbb   bbbbb    bbbbb    bbbbbbb   bbbbbbbb                     gg",
"gg        c                                                        c  oo            gg",
"gg     ooooooo                                                    oooo              gg",
"gg    o                                                        cco   n              gg",
"gg   o                                                         oo    n              gg",
"gg     Qc c c     1          O                               Qo      n              gg",
"ggb     bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb       n     cc       gg",
"gg b                                                                 w    bbbb      gg",
"gg  bQ                                                              Qw              gg",
"gg   bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb            gg",
"gg                                 7                     7              n           gg",
"gg                                                                       n          gg",
"gg                                                                        n         gg",
"gg                 c      p        7                     7                 n        gg",
"gg                 bbbbbbbb                                                 n       gg",
"gg              c            c                                                 o    gg",
"gg              o            o                           7                     n    gg",
"gg     c  c     oQ    2     QoQ           O  5       O        3  O            Qn ccQgg",
"ggDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDgg"]

# add enemies/levels to list
get_levels.append(level_1)

level_2 = [
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                           DDDDDDDDDDDDDDDD          7                                                                    B",
"nn                               D           D              D                                                                               B",
"nn                               D           D            7 D                                                                               B",
"nn                              D           D                                                     Q  5   Q                                  B",
"nn                               D          D              D     7   O        1  Q       7            nnnnnn                                B",
"nn                               D   7   7DO      5     QD          QDDDDDDDDDD              n                                              B",
"nn          nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn     nnnnnnnnnnnnnnnnnnnn          nnnnnnnnnnnnnnnnnnnnnnnnnnnn  B",
"nn         wwwwwwwwwwwwwwwwwwwwwwwww                                      nn                                 n                              B",
"nn        wwwwwwwwwwwwwwwwwwwwwwwwww                                       n                                 n                              B",
"nn       wwwwwwwwwwwwwwwwwwwwwwwwwww                                       n                                 n                              B",
"nn      wwwwwwwwwwwnnnnnnnnnnnnnnnnn                                       nQ                               Qn                              B",
"nn     wwwwwwwwwwwwwwwwwwwwwwwwwwwww                                       nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn                              B",
"nn    wwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                                                                                        B",
"nnwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                                                                                        B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]


# add enemies/levels to list
get_levels.append(level_2)

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

level_4 = [
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                           DDDDDDDDDDDDDDDD          7                                                                    B",
"nn                               D           D              D                                                                               B",
"nn                               D           D            7 D                                                                               B",
"nn                               D           D                                                     Q  5   Q                                 B",
"nn                               D          D              D     7   O        1  Q       7            nnnnnn                                B",
"nn          O    5   5 Q         D   7   7DO      5     QD          QDDDDDDDDDD              n                                              B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn     nnnnnnnnnnnnnnnnnnnn          nnnnnnnnnnnnnnnnnnnnnnnnnnnn B"
"nn                                                                        nn                                 n                              B",
"nn                                                                         n                                 n                              B",
"nn                                                                         n                                 n                              B",
"nn                                                                         nQ                               Qn                              B",
"nn                                                                         nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn                              B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nn                                                                                                                                          B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]

# add enemies/levels to list
get_levels.append(level_4)