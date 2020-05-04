import os
import pygame
import random
from scripts import charts

#-------------------------------------------------------------------------------
class Character:
    def __init__(self, x, y, species = 'charmander', level = 1,
        baseStats = None):

        self.x = x
        self.y = y
        self.species = species
        self.vel = 1 
        self.walkCount = 0 
        self.level = level

        if baseStats == None:
            self.baseStats = charts.getPokemonStats(self.species.capitalize())
        self.stats = self.baseStats
        self.type = self.baseStats['Type 1']

        self.health = self.stats['HP']
        self.max_health = self.stats['HP']
        self.standing = True
        self.direction = 'S' 
        self.img = None
        self.mask = None
    
        self.stateCounter = 5
        self.cdCounter = 0 
        self.coolDown = 45

    def healthBar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x,
            self.y + 32, 
            self.img.get_width(), 5)) 

        pygame.draw.rect(window, (0,255,0), (self.x,
            self.y + 32, 
            self.img.get_width() *\
            (1 - ((self.max_health - self.health)/self.max_health)), 5)) 

    def cooldown(self):
        if self.cdCounter >= self.coolDown:
            self.cdCounter = 0 
        elif self.cdCounter > 0:
            self.cdCounter += 1

    def draw(self, window):
        spriteDict = {
                'S' :{'STAND':['00'], 'WALK':['01','02']},
                'W' :{'STAND':['06'], 'WALK':['07','08']},
                'E' :{'STAND':['06'], 'WALK':['07','08']},
                'SW':{'STAND':['03'], 'WALK':['04','05']},
                'SE':{'STAND':['03'], 'WALK':['04','05']},
                'NW':{'STAND':['09'], 'WALK':['10','11']},
                'NE':{'STAND':['09'], 'WALK':['10','11']},
                'N' :{'STAND':['12'], 'WALK':['13','14']},
                }
        if not(self.standing):
            if 'E' in self.direction:
                pic = 'CHARACTERS/' + self.species + '_' + \
                    spriteDict[self.direction]['WALK'][self.walkCount] + '.png'
                self.img = pygame.image.load(os.path.join('assets', pic))
                self.img = pygame.transform.flip(self.img, True, False)

            else:
                pic = 'CHARACTERS/' + self.species + '_' + \
                    spriteDict[self.direction]['WALK'][self.walkCount] + '.png'
                self.img = pygame.image.load(os.path.join('assets', pic))

            window.blit( self.img, (self.x, self.y))
            if self.walkCount + 1 >= 2:
                self.walkCount = 0
            else:
                self.walkCount += 1

        else:
            if 'E' in self.direction:
                pic = 'CHARACTERS/'+self.species + '_' + \
                    spriteDict[self.direction]['STAND'][0] + '.png'
                self.img = pygame.image.load(os.path.join('assets', pic))
                self.img = pygame.transform.flip(self.img, True, False)

            else:
                pic = 'CHARACTERS/' + self.species + '_' + \
                    spriteDict[self.direction]['STAND'][0] + '.png'
                self.img = pygame.image.load(os.path.join('assets', pic))
            window.blit( self.img, (self.x, self.y))

        self.healthBar(window)
        self.mask = pygame.mask.from_surface(self.img)
        self.cooldown()

#-------------------------------------------------------------------------------
class Enemy(Character):
    def __init__(self, x, y, species, level = 1):
        super().__init__(x, y, species, level)
        self.moveCd = 45
        self.moveCounter = 0

    def draw(self, window):
        super().draw( window)
        if self.moveCounter + 1 >= self.moveCd:
            self.moveCounter = 0
        else:
            self.moveCounter += 1 * random.choice([0, 1, 2]) 

    
#-------------------------------------------------------------------------------
class Player(Character):
    def __init__(self, x, y, species, level = 1):
        super().__init__(x, y, species, level)

    def healthBar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x,
            self.y + 32, 32, 5)) 

        pygame.draw.rect(window, (0,0,225), (self.x,
            self.y + 32, 32 *\
            (1 - ((self.max_health - self.health)/self.max_health)), 5)) 
    
    # def experienceBar(self, window):

#-------------------------------------------------------------------------------

