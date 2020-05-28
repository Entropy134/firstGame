import pygame
import os
import random
import pickle

# Developer Functions
from pprint import pprint

# Homebrew Functions
from scripts import charts
from scripts.Character import *
from scripts.calculations import *
from scripts.Projectile import *
#------------------------------------------------------------------------------
# Set up window
pygame.font.init()
WIDTH, HEIGHT = 1024, 768
TILESIZE = 32
LIGHTGREY = (120, 120, 120)

# TYPECHART = charts.getTypeChart()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", 
    "BACKGROUNDS/background-black.png")), (WIDTH, HEIGHT))
DEVLOG = False
FPS = 60

#------------------------------------------------------------------------------
def inBox(x, y, offset = -0.01):
    return 0 - offset * WIDTH < x < (1 + offset) * WIDTH and \
        0  + offset * HEIGHT < y < (1 - offset) * HEIGHT

def move(Object):
    if 'N' in Object.direction:
        if inBox(Object.x, Object.y - Object.vel):
            Object.y -= Object.vel
    elif 'S' in Object.direction:
        if inBox(Object.x, Object.y + Object.vel):
            Object.y += Object.vel
    if 'W' in Object.direction:
        if inBox(Object.x - Object.vel, Object.y):
            Object.x -= Object.vel
    elif 'E' in Object.direction:
        if inBox(Object.x + Object.vel, Object.y):
            Object.x += Object.vel

#------------------------------------------------------------------------------
def game():
    run = True
    playerVel = 1
    LEVEL = 0
    clock = pygame.time.Clock()
    
    PLAYER = Player(320, 320, species = 'charmander')
    stateCounter = 0

    projectiles = []
    enemyProjectiles = []
    enemies = []
    #--------------------------------------------------------------------------- 
    def stateUpdate(obj):
        '''
        PURPOSE:
        The purpose of this is to update the state of a player or cpu
        character.

        RETURNS:
        None
        '''
        obj.standing = False
        obj.stateCounter = 3
    
    #--------------------------------------------------------------------------- 
    def showGrid():
        '''
        PURPOSE:
        Show the grid on the plot
        '''
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (0, y), (WIDTH, y))

    #--------------------------------------------------------------------------- 
    def redraw():
        '''
        PURPOSE:
        Redraw components onto the screen
        '''
        # Background
        WIN.blit(BG, (0,0))
        # Grid
        showGrid()
        # Player
        PLAYER.draw(WIN)
        # Enemies
        for ENEMY in enemies:
            ENEMY.draw(WIN)
        # Projectiles
        for PROJECTILE in projectiles + enemyProjectiles:
            PROJECTILE.draw(WIN)
        
        pygame.display.update() # This needs to be at the end of the redraw 
        # function
    #--------------------------------------------------------------------------- 
    
    while run:
        clock.tick(FPS)
       
        for CPU in enemies:
            if CPU.health <= 0:
                enemies.remove(CPU)
        
        if len(enemies) == 0:
            LEVEL += 1
            waveCount = 1
            
            for i in range(waveCount):
                enemy = Enemy(random.randrange(25, WIDTH-25),
                        random.randrange(25, HEIGHT - 25),
                        random.choice(['charmander']), #, 'bulbasaur']),
                        level = LEVEL)
                enemies.append(enemy)

        # Get user input
        keys = pygame.key.get_pressed()
       
        # Movement 
        if keys[pygame.K_a] and keys[pygame.K_w]:
            PLAYER.direction = 'NW'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)

        elif keys[pygame.K_a] and keys[pygame.K_s]:
            PLAYER.direction = 'SW'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)

        elif keys[pygame.K_d] and keys[pygame.K_w]:
            PLAYER.direction = 'NE'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            PLAYER.direction = 'SE'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)
       
        elif keys[pygame.K_a]:
            PLAYER.direction = 'W'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)

        elif keys[pygame.K_w]:
            PLAYER.direction = 'N'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)

        elif keys[pygame.K_s]:
            PLAYER.direction = 'S'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)

        elif keys[pygame.K_d]:
            PLAYER.direction = 'E'
            move(PLAYER)
            stateCounter = stateUpdate(PLAYER)

        if keys[pygame.K_SPACE]:
            if PLAYER.cdCounter == 0:
                shot = Projectile(PLAYER.x, PLAYER.y, PLAYER.direction,
                    PLAYER.type.upper())
                projectiles.append(shot)

                PLAYER.cdCounter += 1
        elif keys[pygame.K_q]:
            run = False
        
        # Advance and remove enemies 
        for enemy in enemies[:]:
            if enemy.moveCounter == 0:
                enemy.direction = random.choice(['N','S','W','E', 
                    'NW','SW','SE','NE'])
            if enemy.moveCounter < enemy.moveCd/4:
                move(enemy)

            # Make enemies shoot
            if enemy.cdCounter == 0 and random.uniform(0, 100) <= enemy.level:
                shot = Projectile(enemy.x, enemy.y, enemy.direction,
                    enemy.type.upper())
                enemyProjectiles.append(shot)
                enemy.cdCounter += 1

            stateUpdate(enemy)

            # If not moving for so long, then change state to standing
            if enemy.stateCounter < 0:
                enemy.stateCounter = 0
                enemy.standing = True
            else:
                enemy.stateCounter -= 1
            # If not in box, remove
            if not inBox(enemy.x, enemy.y):
                enemies.remove(enemy)

        redraw()

        # Advance and remove lost projectiles
        for PROJECTILE in projectiles[:]:
            PROJECTILE.move()             
            
            if not inBox(PROJECTILE.x, PROJECTILE.y, offset = -0.01):
                projectiles.remove(PROJECTILE)

            else:
                for enemy in enemies:
                    # WARNING: a collision requires a mask, which is created
                    # when the projectiles are drawn, so run redraw before this
                    if PROJECTILE.collision(enemy):
                        enemy.health -= damageCalc(enemy, PROJECTILE)
                        if DEVLOG: print('Enemy HP: ', enemy.health)
                        projectiles.remove(PROJECTILE)

        # Advance and check collisions in enemy projectiles
        for projectile in enemyProjectiles[:]:
            projectile.move()
            
            if not inBox(projectile.x, projectile.y, offset = -0.01):
                enemyProjectiles.remove(projectile)
            else:
                if projectile.collision(PLAYER):
                    PLAYER.health -= damageCalc(PLAYER, projectile)
                    if DEVLOG: print('Player HP: ', PLAYER.health)
                    enemyProjectiles.remove(projectile)

        # If not moving for so long, then change state to standing
        if PLAYER.stateCounter < 0:
            PLAYER.stateCounter = 0
            PLAYER.standing = True
        else:
            PLAYER.stateCounter -= 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

class Menu:
    def __init__(self, label):
        self.label = label

    def draw(self, window):
        pass    

#------------------------------------------------------------------------------
if __name__ == "__main__":
    game()





