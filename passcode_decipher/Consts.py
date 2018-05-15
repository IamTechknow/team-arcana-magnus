import pygame

TITLE = 'Arkana'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
FPS = 30

screen_width = 800
screen_height = 600


R1_PIN = [18, 17, 16]

GLYPHES = ['SEARCH', 'ANSWER', 'GAIN', 'UNBOUNDED', 'KNWOLEDGE', 'IDEA']

IMAGESDICT = {
    'board': pygame.image.load('assets/board.png'),
    'girl': pygame.image.load('assets/girl.png'),
}