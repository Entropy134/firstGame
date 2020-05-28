import pygame
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40) 
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 24 * 64  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 24 * 32 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Combining Dungeon and Game"
BGCOLOR = DARKGREY


DEVLOG = False #True
TILESIZE = 24
GRIDWIDTH = int( WIDTH / TILESIZE)
GRIDHEIGHT = int(HEIGHT / TILESIZE)



CONTROLS = {
        'UP': pygame.K_w,
        'LEFT': pygame.K_a,
        'RIGHT':pygame.K_d,
        'DOWN': pygame.K_s,

        'QUIT': pygame.K_q,
        }


