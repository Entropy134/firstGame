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
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY


DEVLOG = False
TILESIZE = 24
GRIDWIDTH = int( WIDTH / TILESIZE)
GRIDHEIGHT = int(HEIGHT / TILESIZE)
