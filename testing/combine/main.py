
import pygame
import os


# homebrew functions and variables
# - Classes -
# -- Player and Enemy Classes
from scripts.Character import * 
# -- Projectile Class and collide function
from scripts.Projectile import *
# -- DungeonWall and DungeonFloor Classes
from scripts.DungeonTiles import *


# Functions
from scripts.calculations import *
from scripts.charts import *
from scripts.dungeonGenerator import *

# Variables
from scripts.settings import *


# Define the game class

class Game:
    def __init__(self):
        pygame.init()
        # Set size of the screen
        self.screen = pygame.display.set_mode((int(WIDTH), int(HEIGHT)))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.showStartScreen()
        self.newGame()
        self.run()

    def loadFloor(self):
        game_folder = os.path.dirname(__file__)
        gen = mapGenerator(width = GRIDWIDTH, height = GRIDHEIGHT)
        gen.gen_level()
        self.map_data = gen.gen_tiles_level()
        

        MAP = {}
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles.strip()):
                MAP[(col, row)] = int(tile)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles.strip()):
                if MAP[(col, row)] == 1:
                    if DEVLOG: print(col, row)
                    DungeonWall(self, col, row,  MAP)
                else:
                    DungeonFloor(self, col, row)
        
        x, y, w, l = random.choice(gen.room_list)

        return (x+ 2) * TILESIZE, (y + 2) * TILESIZE
    
    def hitWall(self, testx, testy):
        for wall in self.walls:
            if wall.x == testx and wall.y == testy:
                return True
        return False

    def move(self, Object):
        if 'N' in Object.direction:
            if not self.hitWall(Object.x, Object.y - Object.vel):
                Object.y -= Object.vel
        elif 'S' in Object.direction:
            if not self.hitWall(Object.x, Object.y + Object.vel):
                Object.y += Object.vel

        if 'W' in Object.direction:
            if not self.hitWall(Object.x - Object.vel, Object.y):
                Object.x -= Object.vel
        elif 'E' in Object.direction:
            if not self.hitWall(Object.x + Object.vel, Object.y):
                Object.x += Object.vel




    def newGame(self):
        '''
        PURPOSE:
        Initialize variables and set up for a new game
        '''
        self.projectiles = []
        self.enemyProjectiles = []
        self.enemies = []

        
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.firstLayer = pygame.sprite.Group()
        self.variableLayer = TopDownGroup()


        # TEMPORARY: Load up a dungeon immediately
        playerx, playery = self.loadFloor()
        self.player = Player(playerx, playery, species = 'charmander')
        self.camera = Camera(WIDTH/4, HEIGHT/4)

    def processInput(self):
        keys = pygame.key.get_pressed()
        
        # Quit Game?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()

        if keys[CONTROLS['QUIT']]:
            self.playing = False
            pygame.quit()

        else:
            # Movement
            d = ''
            if keys[CONTROLS['UP']]:
                d = d + 'N'
            elif keys[CONTROLS['DOWN']]:
                d = d + 'S'

            if keys[CONTROLS['LEFT']]:
                d = d + 'W'
            elif keys[CONTROLS['RIGHT']]:
                d = d + 'E'
            
            if d != '':
                self.player.direction = d
                self.move(self.player)

    def update(self):
        self.camera.update(self.player)




    def run(self):
        # Main Game Loop
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.processInput()
            self.update()

            if self.playing:
                self.draw()


    def draw(self):

        self.screen.fill(BGCOLOR)

        for sprite in self.firstLayer:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        self.screen.blit(self.player.img, self.camera.apply(self.player))
        # self.firstLayer.draw(self.screen)

        self.player.draw(self.screen)
        
        for P in self.projectiles + self.enemyProjectiles:
            P.draw(self.screen)

        pygame.display.flip()

    def showStartScreen(self):
        pass
    



if __name__ == "__main__":
    # Create the Game Object
    Game()















