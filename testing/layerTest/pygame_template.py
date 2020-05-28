# Pygame template - skeleton for new pygame project
import pygame as pg
import random


WIDTH = 360
HEIGHT = 480

FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame and create window
pg.init()
pg.mixer.init() # handles music within Pygame
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Default Title")

clock = pg.time.Clock()

# Game Loop
running = True
while running:
    # keep loop running at correct speed
    clock.tick(FPS)

    # process input / events
    for event in pg.event.get():
        # check for closing the window
        if event.type == pg.QUIT:
            running = False

    # update

    # draw / render
    screen.fill(BLACK)
    pg.display.flip() # After drawing everything, flip display

pg.quit()
