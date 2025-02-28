import pygame, math, sys, os
from pygame.locals import *
import level

rootpath = ''#'/mnt/lvm/home/chris/docs/Documents/Personal/tanks'

TURNINGRATE = 1
SPEED = 1
TANKSIZE = 32*1.2
class Tank(pygame.sprite.Sprite):
    image = None

    def __init__(self, player = 1, position=(0,0), angle=90):
        pygame.sprite.Sprite.__init__(self)
        
        if player == 1:
            self.image = pygame.image.load(os.path.join(rootpath, "gfx","bluetank.png")).convert()
        else:
            self.image = pygame.image.load(os.path.join(rootpath, "gfx","redtank.png")).convert()
        self.position = position
        self.angle = angle
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.original = self.image
        
    def update(self):
       self.rect = self.image.get_rect()
       self.image = pygame.transform.rotate(self.original, self.angle)
       self.rect.center = self.position
           
    def move_forward(self, walls):
        x,y = self.position
        oldx, oldy = self.position
        x -= SPEED*math.cos(math.radians(self.angle))
        y += SPEED*math.sin(math.radians(self.angle))
        self.position = (x,y)
        self.update()
        if(pygame.sprite.spritecollide(self, walls, False)):
            self.position = (oldx,oldy)
            self.update()
    
    def move_backward(self, walls):
        x,y = self.position
        oldx, oldy = self.position
        x += SPEED*math.cos(math.radians(self.angle))
        y -= SPEED*math.sin(math.radians(self.angle))
        self.position = (x,y)
        if(pygame.sprite.spritecollide(self, walls, False)):
            self.position = (oldx,oldy)
            self.update()
    
    def rotate_right(self):
        oldangle = self.angle
        oldx, oldy = self.position
        self.angle -= TURNINGRATE
        if self.angle < 0: self.angle += 360
            
    def rotate_left(self):
        oldangle = self.angle
        self.angle += TURNINGRATE
        if self.angle > 360: self.angle -= 360
        
    def get_shot_location(self):
        x,y = self.position
        x -= TANKSIZE*math.cos(math.radians(self.angle))
        y += TANKSIZE*math.sin(math.radians(self.angle))
        return (x,y)
    
