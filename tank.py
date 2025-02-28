import pygame, math, os

rootpath = ''

move_sound = pygame.mixer.Sound(os.path.join(rootpath, "snd", "move.mp3"))

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
        pygame.mixer.Sound.play(move_sound)
        x,y = self.position
        old_x, old_y = self.position
        x -= SPEED*math.cos(math.radians(self.angle))
        y += SPEED*math.sin(math.radians(self.angle))
        self.position = (x,y)
        self.update()
        if pygame.sprite.spritecollide(self, walls, False):
            self.position = old_x,old_y
            self.update()
    
    def move_backward(self, walls):
        pygame.mixer.Sound.play(move_sound)
        x,y = self.position
        old_x, old_y = self.position
        x += SPEED*math.cos(math.radians(self.angle))
        y -= SPEED*math.sin(math.radians(self.angle))
        self.position = (x,y)
        if pygame.sprite.spritecollide(self, walls, False):
            self.position = (old_x,old_y)
            self.update()
    
    def rotate_right(self):
        self.angle -= TURNINGRATE
        if self.angle < 0: self.angle += 360
            
    def rotate_left(self):
        self.angle += TURNINGRATE
        if self.angle > 360: self.angle -= 360
        
    def get_shot_location(self):
        x,y = self.position
        x -= TANKSIZE*math.cos(math.radians(self.angle))
        y += TANKSIZE*math.sin(math.radians(self.angle))
        return x,y
    
