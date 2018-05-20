import pygame

TITLE = 'Arkana'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
FPS = 30

screen_width = 1366
screen_height = 768


S1_PIN = 26
R1_PIN = [18, 17, 16]
R2_PIN = [23, 22, 24]
R3_PIN = [ 6, 13,  5]


GLYPHES = ['SEARCH', 'ANSWER', 'GAIN', 'UNBOUNDED', 'KNWOLEDGE', 'IDEA']

IMAGESDICT = {
    'board': pygame.image.load('assets/board.png'),
    'girl': pygame.image.load('assets/girl.png'),
}

pygame.font.init()
FONT = pygame.font.SysFont("monospace", 15)

POS_LIST_1 =[(50,150), (150,50), (250,50), (350,150), (250,250), (150,250)]
POS_LIST_2 =[(450,150), (550,50), (650,50), (750,150), (650,250), (550,250)]
POS_LIST_3 =[(850,150), (950,50), (1050,50), (1150,150), (1050,250), (950,250)]
