import pygame

TITLE = 'Arkana'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE  = (0, 0, 255)
GREEN = (69, 139, 0)

FPS = 30

screen_width = 1366
screen_height = 768

S1_PIN = 26
R1_PIN = [18, 17, 16]
R2_PIN = [23, 22, 24]
R3_PIN = [ 6, 13,  5]

GLYPHES = [['SEARCH', 'ANSWER', 'GAIN'], ['UNBOUNDED', 'KNWOLEDGE', 'IDEA']]

IMAGESDICT = {
    'board': pygame.image.load('assets/board.png'),
    'girl': pygame.image.load('assets/girl.png'),
}

pygame.font.init()
FONT = pygame.font.SysFont("monospace", 20, bold = True)

START_X_1 = 50
START_Y_1 = 50

START_X_2 = 450
START_Y_2 = 50

START_X_3 = 850
START_Y_3 = 50

SPACE_X  = 100
SPACE_Y  = 100

POS_LIST_1 = [(START_X_1,START_Y_1 + SPACE_Y), (START_X_1 + SPACE_X, START_Y_1), (START_X_1 + 2 * SPACE_X, START_Y_1), \
        (START_X_1 + 3 * SPACE_X, START_Y_1 + SPACE_Y), (START_X_1 + 2 * SPACE_X, START_Y_1 + 2 * SPACE_Y), (START_X_1 + SPACE_X, START_Y_1 + 2 * SPACE_Y), \
        (START_X_1 + 1.5 * SPACE_X, START_Y_1 + SPACE_Y)]

POS_LIST_2 = [(START_X_2, START_Y_2 + SPACE_Y), (START_X_2 + SPACE_X, START_Y_2), (START_X_2 + 2 * SPACE_X, START_Y_2), \
        (START_X_2 + 3 * SPACE_X, START_Y_2 + SPACE_Y), (START_X_2 + 2 * SPACE_X, START_Y_2 + 2 * SPACE_Y), (START_X_2 + SPACE_X, START_Y_2 + 2 * SPACE_Y), \
        (START_X_2 + 1.5 * SPACE_X, START_Y_2 + SPACE_Y)]

POS_LIST_3 = [(START_X_3,START_Y_3 + SPACE_Y), (START_X_3 + SPACE_X, START_Y_3), (START_X_3 + 2 * SPACE_X, START_Y_3), \
        (START_X_3 + 3 * SPACE_X, START_Y_3 + SPACE_Y), (START_X_3 + 2 * SPACE_X, START_Y_3 + 2 * SPACE_Y), (START_X_3 + SPACE_X, START_Y_3 + 2 * SPACE_Y), \
        (START_X_3 + 1.5 * SPACE_X, START_Y_3 + SPACE_Y)]