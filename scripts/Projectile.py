import os
import pygame

#------------------------------------------------------------------------------
def collide(obj1, obj2):

    _offset_x = obj2.x - obj1.x
    _offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (_offset_x, _offset_y)) != None


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
