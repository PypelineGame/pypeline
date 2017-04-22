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
"gg   b          c            c                                                 o    gg",
"gg  bX          o            o                           7                     n    gg",
"gg  bY c  c     oQ    2     QoQ           O  5       O        3  O            Qn ccQgg",
"ggDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDgg"]

# add enemies/levels to list
get_levels.append(level_1)

level_2 = [
"nn                                                                                                                                                               B",
"nn                                                                                                                                                               B",
"nn                                           DDDDDDDDDDDDDDDD          7                                                                                         B",
"nn                               D           D              D                                                                                                    B",
"nn                               D           D            7 D                                                                                   c    c    c      B",
"nn                               D           D              D                                       Q    5   Q                             wwwwwwwwwwwwwwwwwwwwwwB",
"nn                               D           D              D     7   Q      c 1  Q   c   7           nnnnnnnn                             wwwwwwwwwwwwwwwwwwwww B",
"nn                  c c          D   7    7  DO      5     QD          DDDDDDDDDDD             n                            c              wwwwwwwwwwwwwwwwwwwwwwB",
"nn          nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn     nnnnnnnnnnnnnnnnnnnn          nnnnnnnnnnnnnnnnnnnnnnnnnnnnwwwwwwwwwwwwwwwww   c  B",
"nn         wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                nn                                 n                                  wwwwwwwwwwwwwwwwwB",
"nn        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                 n                                 n                                                   B",
"nn       wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                 nn                                n                                                   B",
"nn      wwwwwccwwwwnnnnnnnnnnnnnnnnnnnnnnn                                 nnQ             p                Qn                                                   B",
"nn     wwwwwwwwwwwwwwwwww    wwwwwwwwwwwww                                 nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn                                                   B",
"nnn   wwwwwwwwwwwwwwwwwww    wwwwwwwwwwwww                                                                                                                       B",
"nnwwwwwwwwwwwwwwwwwwwwwww  5 wwwwwwwwwwwww                                                                                      7                                B",
"nnnnwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                c    Q   5    Q        c                                               7                               B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn    nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn                                                                        B",
"nnX                                              n                                       w                                                                       B",
"nnY                     7                        nn                                       w      c                                                               B",
"nn  n                                            nnn      O      5    Q          5    Q    w     w c                                                             B",
"nn   n  cc                             7         nnnwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww  w      wc                                                            B",
"nn    nnnnnnnn                                   nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww       w    wwwwww   w   w   w   wwwww   w   w   w   wwww          B",
"nn               n                                                                            w                                                                  B",
"nnnnnnnnnnnnnnnnn n                                   7                                        w                                                                 B",
"nn                 n                                                                            w   Q     5     5    5       5       5   5     5    Q            B",
"nn                  nc                                                                           w   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww             B",
"nn                   n                              Q  c  c   c  5  Q                             nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww          B",
"nn                    n     wwww    w                nnnnnnnnnnnnnnnn                              nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww        B",
"nn                        nwwwww     Q    5   Q     n                                 7                                                                 wwwwwwwwwB",
"nn                       nwwwwwwww    wwwwwwww     n                                                                                                    wwwwwwwwwB",
"nn                      nwwwwwwwwww    wwwwwwwww                                                                                                  wwwwwwwwwwwwwwwB",
"nn                    cnwwwwwwwwwwww    wwwwwww w                                                                                                                B",
"nn                    nwwwwwwwwwwwwww        w   w                                                                                                               B",
"nn                   nwww w         ww      w     w                                                                                                              B",
"nnQ      1      Q   nwwwwO     1    Oww    w       w                      Q     5      5    Q   Q      5        Q                    4           4               B",
"nnwwwwwwwwwnwnwnwnwnwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww  c  wwwwwwwwwwwwwwwwwww  c  wwwwwwwwwwwwwww   c  wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww          B",
"nn        nwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                wwwwwww                  wwww                wwwwww                                          B",
"nn       n     wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                                                                                           B",
"nn      n          wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                               7                                                       B",
"nn     n               wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                                                                                    B",
"nn    n                    wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                                                                        y     B",
"nn   n                       wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                                                 7                                   y      B",
"nn  n                             wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwnwww                7                                                             y yyyyyyB",
"nn n                                      wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwnwwwwwwwwww                                                                       y      B",
"nn Q            1                                  wwwwwwwwwwwwwwwwwwQwwwwnwwwwwwwwwwwwwwwww                                                               y     B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]


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