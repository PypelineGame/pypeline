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
BACKGROUNDS = [0, 'background5.jpg', 'beauty.jpg', 'montanha.png', 'forest_day.png']
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
#"gg                                                                             o    gg",
#"gg                                                       7                     n    gg",
#"gg Q           3                                              3  O            Qn ccQgg",
"gg   b          c            c                                                 o    gg",
"gg  bX          o            o                           7                     n    gg",
"gg  bY c  c     oQ    2     QoQ           O  5       O        3  O            Qn ccQgg",
"ggDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDgg"]

# add enemies/levels to list
get_levels.append(level_1)

level_2 = [
"nn                          D           DDDDDDDDDDDDDDDD                                                                B",
"nn                          D           D            7 D     p                                Q    5   Q                B",
"nn                          D           D              D     n   Q      c 1  Q   c   7         nnnnnnnn                 B",
"nn             c c          D   7    7  DO      5     QD          DDDDDDDDDDD             n                     pc     cB",
"nn          nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn     nnnnnnnnnnnnnnnnnnnn          nnnnnnnnnnnnnnnB",
"nn         wwwwwwwwwwwwwwwwwwwwww                                    nn                                 n               B",
"nn        wwwwwwwwwwwwwwwwwwwwwww                                     n                                 n               B",
"nn       wwwwwwwwwwwwwwwwwwwwwwww                                     nn                                n               B",
"nn      wcwwwwnnnnnnnnnnnnnnnnnnn                                     nnQ        c      c        c     Qn               B",
"nn     wwwwwwwwwwwww    wwwwwwwww                                     nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn               B",
"nnn   wwwwwwwwwwwwww    wwwwwwwww                                                                                       B",
"nnwwwwwwwwwwwwwwwwww  5 wwwwwwwww                                                                                       B",
"nnnnwwwwwwwwwwwwwwwwwwwwwwwwwwwww                    c    Q   5    Q        c                                           B",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn    nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn                                    B",
"nnX                                         n                                       w                                   B",
"nnY                7                        nnc                                      w      c                           B",
"nn                       wwwwwwwwwwww       nnn      O      5    Q    c     5    Q   cw     w c                         B",
"nn   n cc                n        7 n       nnnwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww  p w      w c                       B",
"nn    nnn                n          n        WWWWWWWWWWWWnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn       w    wwwwww   w   w   w B",
"nn          n            nQ   1    Qn                wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                              B",
"nnnnnnnnnnnn n           wwwwwwwwwwwwwwwwww      7   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww                             B",
"nn            n          wwwwwwwwwwwwwwwwwwww                                              w   Q     5     5    5    Q  B",
"nn             nc   wwwwwwwwwww       wwwwwww                                               w   wwwwwwwwwwwwwwwwwwwwww  B",
"nn              nwwwwwwwww              wwwwwwwQ 5c  c  Qc  5                                nwwww   wwwcpcwwwwwwwwwwwwwB",
"nn               nQwwwww                   wwwwwwwwwwwwQ                                 Q    nwwwwwwwwwwwwwwwwwwwwwcpcwB",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]


# add enemies/levels to list
get_levels.append(level_2)

level_3 = [

"nn                                                                                                             B",
"nn                                                                                                             B",
"nn                               Q    P     3            Q                                                     B",
"nn         n     wwwwwwwwwwwww    wwwwwwwwwwwwwwwwwwwwwww    wwwwwwwwwwwwwwwwwwwwwww    wwwwwwwwwwww           B",
"nn          n    n   n   n   n   n   n   n   n   n   n   n   n  7 n   n   n   n   n   n   n   n    n           B",
"nn           n                                                                                    n    y       B",
"nn            n                                                                                 cn     y       B",
"nn             n      Q  5  Q Q   5 Q Q     4    3     2    Q   Q  5   5   Q                    n    yyyyy     B",
"nn              nnnn   nnnnn   nnnnn   nnnnnnnnnnnnnnnnnnnnn     nnnnnnnnnn   nnnnnnnn         n      yyy      B",
"nn                                                          w                         n       n        y       B",
"nn                                                           w   c                     n     n                 B",
"nn                                                            wwwwwwwwwwwwwww               n                  B",
"nn                                      n       n     6                                    n  6                B",
"nn                                      n   1  Qn                                        cn                    B",
"nn                                       wwwwwww                                         n                     B",
"nn                                                                                      n                      B",
"nn      wwcwwwwcwwwcwwwcwwwwwcwwwww               w     w     w    w                   n                       B",
"nn      wcwwccwwwcwwwwwcwcwcwwcwwww                w     w     w    w                 n                        B",
"nn      wwcwcwwwcwwwcwwcwwwcwwwwcww                cw    cw    cw   cw               n                         B",
"nn      wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwn       cn      6                   B",
"nn                                                                          n      n                           B",
"nn                                               7                                n                            B",
"nn                                                                               n                             B",
"nn                                                                             cn                              B",
"nn                                                                             n  6                            B",
"nn                          c   c   c       c    c    c                       n                                B",
"nn       wwwwwwwwn    wwww  w   w   w   w   w    w    w   w  n               n                                 B",
"nn      w       wn                                           n              w                                  B",
"nn     w        wn               7                           n             w                                   B",
"nn    w         ww                                7          w            w                                    B",
"nn   wp Q c  5 QwwQ    1                1               1   QwQ p   5   Qw    Q                 8             QB",
"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnB"]

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
