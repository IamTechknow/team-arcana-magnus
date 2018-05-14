import Consts
import pygame

class Wheel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.rect = pygame.Rect(width, height)
        #self.image = pygame.Surface([width, height])
        self.image = Consts.IMAGESDICT['girl'].convert_alpha()
        self.rect = self.image.get_rect()
    
    def rotate(self, direction):
        rotate = pygame.transform.rotate
        if (direction == -1):
            self.image = rotate(self.image, 10)
        else:
            self.image = rotate(self.image, -10)