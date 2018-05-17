import pygame

TITLE = 'Arkana'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
FPS = 30

screen_width = 800
screen_height = 600


S1_PIN = 26
R1_PIN = [18, 17, 16]

GLYPHES = ['SEARCH', 'ANSWER', 'GAIN', 'UNBOUNDED', 'KNWOLEDGE', 'IDEA']

IMAGESDICT = {
    'board': pygame.image.load('assets/board.png'),
    'girl': pygame.image.load('assets/girl.png'),
}

pygame.font.init()
FONT = pygame.font.SysFont("monospace", 15)

POS_LIST =[(100,300), (200,200), (300,200), (400,300), (300,400), (200,400)]
