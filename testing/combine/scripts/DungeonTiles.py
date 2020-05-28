import pygame
from scripts.settings import *
from scripts.dungeonSprite import *
import random
import os

class DungeonFloor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.firstLayer, game.floors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        pic = 'MAPTILES/' + 'MtSteel_'+ '013' + '.png'
        self.image = pygame.image.load(os.path.join('assets', pic))

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class DungeonWall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, MAP):
        self.groups = game.firstLayer, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.MAP = MAP
        # The total width is the number of columns, x
        # the total height is the number of rows, y
        if x - 1 < 0:
            xprev = x
        else:
            xprev = x - 1
        if y - 1 < 0:
            yprev = y
        else:
            yprev = y - 1
        if y + 1 >= GRIDHEIGHT:
            ynext = GRIDHEIGHT -1
        else:
            ynext = y + 1
        if x + 1 >= GRIDWIDTH:
            xnext = GRIDWIDTH - 1
        else:
            xnext = x + 1
        a, b, c = (xprev, yprev), (x, yprev), (xnext, yprev)
        d, e, f = (xprev, y), (x, y), (xnext, y)
        g, h, i = (xprev, ynext), (x, ynext), (xnext, ynext)
        MATRIX = [
                [int(self.MAP[a]), int(self.MAP[b]), int(self.MAP[c])],
                [int(self.MAP[d]), int(self.MAP[e]), int(self.MAP[f])],
                [int(self.MAP[g]), int(self.MAP[h]), int(self.MAP[i])]
                ]

        if DEVLOG: print(MATRIX)
        try:
            LIST = []
            for key, val in WALLPICS.items():
                if MATRIX == val:
                    if DEVLOG: print(key, val, '*')
                    LIST.append(key[:3])

                #else:
                #    if DEVLOG: print(key, val, '')

            picnum = random.choice(LIST)
        except IndexError:
            if int(self.MAP[b]) == 0:
                MATRIX = [[0, 0, 0], [1, 1, 1], [1, 1, 1]]
            elif int(self.MAP[d]) == 0:
                MATRIX = [[0, 1, 1], [0, 1, 1], [0, 1, 1]]
            elif int(self.MAP[f]) == 0:
                MATRIX = [[1, 1, 0], [1, 1, 0], [1, 1, 0]]
            elif int(self.MAP[h]) == 0:
                MATRIX = [[1, 1, 1], [1, 1, 1], [0, 0, 0]]

            if DEVLOG: print(MATRIX)

            LIST = []
            for key, val in WALLPICS.items():
                if MATRIX == val:
                    if DEVLOG: print(key, val, '*')
                    LIST.append(key[:3])
                else:
                    if DEVLOG: print(key, val, '')

            picnum = random.choice(LIST)

        # if picnum == '543': print(x, y, MATRIX, 'c = ', c, self.MAP[c]) # Issue Closed.
        pic = 'MAPTILES/' + 'MtSteel_'+ picnum + '.png'

        self.image = pygame.image.load(os.path.join('assets', pic))

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE





