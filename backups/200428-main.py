import pygame
import os
import random
from pprint import pprint

# Homebrew Functions
from assets import charts

#------------------------------------------------------------------------------
# Set up window
pygame.font.init()
WIDTH, HEIGHT = 1024, 768
TILESIZE = 32
LIGHTGREY = (120, 120, 120)

TYPECHART = charts.getTypeChart()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Walking Charmander")

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", 
    "BACKGROUNDS/background-black.png")), (WIDTH, HEIGHT))
FPS = 30

#------------------------------------------------------------------------------
def collide(obj1, obj2):

    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def damageCalc(target, projectile):
    base_damage = projectile.dmg
    weakness_multiplier = TYPECHART[projectile.type][target.type.upper()]

    return base_damage * weakness_multiplier


#------------------------------------------------------------------------------
def inBox(x, y, offset = -0.1):
    return 0 - offset * WIDTH < x < (1 + offset) * WIDTH and \
        0  - offset * HEIGHT < y < (1 + offset) * HEIGHT
#------------------------------------------------------------------------------

class Character:
    def __init__(self, x, y, species = 'charmander', level = 1, 
        baseStats = None):
        
        self.x = x
        self.y = y
        self.species = species
        self.walkCount = 0

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

        self.cdCounter = 0
        self.coolDown = FPS * 0.5 

    def healthBar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x,
            self.y + self.img.get_height() + 10,
            self.img.get_width(), 5))

        pygame.draw.rect(window, (0,255,0), (self.x,
            self.y + self.img.get_height() + 10,
            self.img.get_width() * \
            (1 - ((self.max_health - self.health)/self.max_health)), 5))

    def cooldown(self):
        if self.cdCounter >= self.coolDown:
            self.cdCounter = 0
        elif self.cdCounter > 0:
            self.cdCounter += 1

    def enemyMove(self, vel):
        self.y += vel

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

#------------------------------------------------------------------------------
class Projectile():
    def __init__(self, x, y, direction, _type = 'FIRE'):
        self.typeDict = {
                'FIRE' :{'VEL': 8, 'DMG':10, 'FRAMES':5},
                'GRASS':{'VEL':10, 'DMG': 8, 'FRAMES':4},
                'WATER':{'VEL': 9, 'DMG': 9},
                }

        self.x = x
        self.y = y
        self.direction = direction
        self.type = _type
        self.vel = self.typeDict[self.type]['VEL']
        self.dmg = self.typeDict[self.type]['DMG']
        self.animCount = 0
        self.img  = None
        self.mask = None
        

    def draw(self, window):
        pic = 'PROJECTILES/' + self.type.upper()+ '_' + str(self.animCount)+'.png'
        self.img = pygame.image.load(os.path.join("assets", pic))
        self.mask = pygame.mask.from_surface(self.img)
    
        if self.animCount + 2 >= self.typeDict[self.type]['FRAMES']:
            self.animCount = 0
        else:
            self.animCount += 1
        window.blit(self.img, (self.x, self.y))
    
    def collision(self, obj):
        return collide(self, obj)

    def move(self):
        if 'N' in self.direction:
            self.y -= self.vel
        elif 'S' in self.direction:
            self.y += self.vel
        if 'W' in self.direction:
            self.x -= self.vel
        elif 'E' in self.direction:
            self.x += self.vel



#------------------------------------------------------------------------------
def main():
    run = True
    playerVel = 32
    level = 0
    clock = pygame.time.Clock()
    
    PLAYER = Character(320, 320, species = 'charmander')
    stateCounter = 0

    projectiles = []
    enemies = []

    def stateUpdate(obj, stateCounter):
        obj.standing = False
        return 3
    
    def showGrid():
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (0, y), (WIDTH, y))

    def redraw():
        WIN.blit(BG, (0,0))
        showGrid()
        PLAYER.draw(WIN)
        
        for ENEMY in enemies:
            ENEMY.draw(WIN)

        for PROJECTILE in projectiles:
            PROJECTILE.draw(WIN)
        
        pygame.display.update() # This needs to be at the end
    
    while run:
        clock.tick(FPS)
       
        for CPU in enemies:
            if CPU.health <= 0:
                enemies.remove(CPU)
        
        if len(enemies) == 0:
            level += 1
            waveCount = 3
            
            for i in range(waveCount):
                enemy = Character(random.randrange(25, WIDTH-25),
                        random.randrange(25, HEIGHT - 25),
                        random.choice(['charmander', 'bulbasaur']))
                enemies.append(enemy)

        # Get user input
        keys = pygame.key.get_pressed()
        # Movement 
        if keys[pygame.K_a] and keys[pygame.K_w] and inBox(PLAYER.x - playerVel, 
            PLAYER.y - playerVel):
            
            PLAYER.x -= playerVel
            PLAYER.y -= playerVel
            PLAYER.direction = 'NW'
            stateCounter = stateUpdate(PLAYER, stateCounter)

        elif keys[pygame.K_a] and keys[pygame.K_s] and inBox(PLAYER.x - playerVel,
            PLAYER.y + playerVel):
    
            PLAYER.x -= playerVel
            PLAYER.y += playerVel
            PLAYER.direction = 'SW'
            stateCounter = stateUpdate(PLAYER, stateCounter)

        elif keys[pygame.K_d] and keys[pygame.K_w] and \
            inBox(PLAYER.x + playerVel, PLAYER.y - playerVel):

            PLAYER.x += playerVel
            PLAYER.y -= playerVel
            PLAYER.direction = 'NE'
            stateCounter = stateUpdate(PLAYER, stateCounter)

        elif keys[pygame.K_d] and keys[pygame.K_s] and \
            inBox(PLAYER.x + playerVel, PLAYER.y + playerVel):

            PLAYER.x += playerVel
            PLAYER.y += playerVel
            PLAYER.direction = 'SE'
            stateCounter = stateUpdate(PLAYER, stateCounter)
       
        elif keys[pygame.K_a] and inBox(PLAYER.x - playerVel, PLAYER.y):
            PLAYER.x -= playerVel
            PLAYER.direction = 'W'
            stateCounter = stateUpdate(PLAYER, stateCounter)

        elif keys[pygame.K_w] and inBox(PLAYER.x, PLAYER.y - playerVel):
            PLAYER.y -= playerVel
            PLAYER.direction = 'N'
            stateCounter = stateUpdate(PLAYER, stateCounter)

        elif keys[pygame.K_s] and inBox(PLAYER.x, PLAYER.y + playerVel):
            PLAYER.y += playerVel
            PLAYER.direction = 'S'
            stateCounter = stateUpdate(PLAYER, stateCounter)

        elif keys[pygame.K_d] and inBox(PLAYER.x + playerVel, PLAYER.y):
            PLAYER.x += playerVel
            PLAYER.direction = 'E'
            stateCounter = stateUpdate(PLAYER, stateCounter)


        if keys[pygame.K_SPACE]:
            if PLAYER.cdCounter == 0:
                shot = Projectile(PLAYER.x, PLAYER.y, PLAYER.direction,
                    PLAYER.type.upper())
                projectiles.append(shot)

                PLAYER.cdCounter = 1
        #
        for enemy in enemies[:]:
            enemy.enemyMove(1)

            #if not inBox(enemy.x, enemy.y):
            #    enemies.remove(enemy)


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
                        if PROJECTILE in projectiles[:]:
                            projectiles.remove(PROJECTILE)
                            
        # If not moving for so long, then change state to standing
        if stateCounter < 0:
            stateCounter = 0
            PLAYER.standing = True
        else:
            stateCounter -= 1
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()





