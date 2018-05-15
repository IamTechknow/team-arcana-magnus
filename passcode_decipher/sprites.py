import Consts
import pygame

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    #rot_image = rot_image.subsurface(rot_rect).copy()
    rot_image = rot_image.copy()
    return rot_image

class Wheel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.rect = pygame.Rect(width, height)
        #self.image = pygame.Surface([width, height])
        self.image = Consts.IMAGESDICT['girl'].convert_alpha()
        self.rect = self.image.get_rect()
    
    def rotate(self, direction):
        if (direction == -1):
            self.image = rot_center(self.image, 10)
        else:
            self.image = rot_center(self.image, -10)