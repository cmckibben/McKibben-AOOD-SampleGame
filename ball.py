import pygame, math, sys, os
from pygame.locals import *

rootpath = ''

bounce_sound = pygame.mixer.Sound(os.path.join(rootpath, "snd", "hitwall.mp3"))


class Ball(pygame.sprite.Sprite):
    """Bouncing ball used as a shot
        Terminitates itself after a specified number of frames"""
    image = None

    def __init__(self, speed, position=(0,0), angle=0, life = 300):
        """starts a ball going at a specified speed from a specified location (x,y) at a specified angle.
            lives for life frames"""
        pygame.sprite.Sprite.__init__(self)
        
        if Ball.image is None:
            self.image = pygame.image.load(os.path.join(rootpath, "gfx","ball.png")).convert()
        self.position = position
        while angle < 0: angle += 360
        while angle > 360: angle -= 360
        self.velocityx = -math.cos(math.radians(angle))*speed
        self.velocityy = math.sin(math.radians(angle))*speed
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.life = life
        
    def reflect(self,sprite):
        pygame.mixer.Sound.play(bounce_sound)
        if sprite.rect.collidepoint(self.rect.centerx,self.rect.top):
            self.velocityy = -self.velocityy
            self.update()
        if sprite.rect.collidepoint(self.rect.centerx,self.rect.bottom):
            self.velocityy = -self.velocityy
            self.update()
        if sprite.rect.collidepoint(self.rect.left,self.rect.centery):
            self.velocityx = -self.velocityx
            self.update()
        if sprite.rect.collidepoint(self.rect.right,self.rect.centery):
            self.velocityx = -self.velocityx
            self.update()

        
    def update(self):
        """Calculates new position"""
        self.life -= 1
        if self.life <= 0: self.kill() #terminate self
        x,y = self.position
        
        x += self.velocityx
        y += self.velocityy

        self.position = (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position