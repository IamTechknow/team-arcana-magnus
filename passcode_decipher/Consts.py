import pygame

TITLE = 'Arkana'

CRYPTO_KEY_LETTERS = 'ARCANA'
CRYPTO_KEY_NUM = '12435'

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

# SEARCH from SEARCH DATA DISCOVER PATH
# ANSWER from DEFEND MESSAGE ANSWER IDEA 
GLYPHES = [['DATA', 'DISCOVER', 'PATH'], ['DEFEND', 'MESSAGE', 'IDEA']]

IMAGESDICT = {
    'board': pygame.image.load('assets/ingress.jpg'),
    'girl': pygame.image.load('assets/girl.png'),
}

pygame.font.init()
FONT = pygame.font.SysFont("monospace", 20, bold = True)

START_X_1 = 50
START_Y_1 = 100

START_X_2 = 450
START_Y_2 = 350

START_X_3 = 700
START_Y_3 = 100

SPACE_X  = 150
SPACE_Y  = 50

POS_LIST_1 = [(START_X_1,START_Y_1 + SPACE_Y), (START_X_1 + SPACE_X, START_Y_1), (START_X_1 + 2 * SPACE_X, START_Y_1), \
        (START_X_1 + 3 * SPACE_X, START_Y_1 + SPACE_Y), (START_X_1 + 2 * SPACE_X, START_Y_1 + 2 * SPACE_Y), (START_X_1 + SPACE_X, START_Y_1 + 2 * SPACE_Y), \
        (START_X_1 + 1.5 * SPACE_X, START_Y_1 + 3 * SPACE_Y + 15)]

POS_LIST_2 = [(START_X_2, START_Y_2 + SPACE_Y), (START_X_2 + SPACE_X, START_Y_2), (START_X_2 + 2 * SPACE_X, START_Y_2), \
        (START_X_2 + 3 * SPACE_X, START_Y_2 + SPACE_Y), (START_X_2 + 2 * SPACE_X, START_Y_2 + 2 * SPACE_Y), (START_X_2 + SPACE_X, START_Y_2 + 2 * SPACE_Y), \
        (START_X_2 + 1.5 * SPACE_X, START_Y_2 + 3 * SPACE_Y + 15)]

POS_LIST_3 = [(START_X_3,START_Y_3 + SPACE_Y), (START_X_3 + SPACE_X, START_Y_3), (START_X_3 + 2 * SPACE_X, START_Y_3), \
        (START_X_3 + 3 * SPACE_X, START_Y_3 + SPACE_Y), (START_X_3 + 2 * SPACE_X, START_Y_3 + 2 * SPACE_Y), (START_X_3 + SPACE_X, START_Y_3 + 2 * SPACE_Y), \
        (START_X_3 + 1.5 * SPACE_X, START_Y_3 + 3 * SPACE_Y + 15)]

STATE_STARTING = 0
STATE_DESCRIPTION = 1
STATE_PLAY = 2
STATE_FOUND = 3
STATE_WIN_DISPLAY = 4

MESSAGE_FONT = pygame.font.SysFont("monospace", 40, bold = True)
STARTUP_TEXTS = ["GLYPHS HUNTING TIME !", \
                 "As a Glyph hunter, you have to discover what glyphs ","are hidden in this game.", \
                 "You have to find how was encrypted","", "","", "", "", "some series of 3 glyphs.", \
                 "Then in a ultimate step, your glyphing capabilities", "will help you find the final 2 glyphs"]
STARTUP_TEXT_POSITION_Y = 50

MAX_TRIES = 5

HELP_TEXT = ["Choose the 3 algorithm with Rotary", " and validate with BUTTON.You have " + str(MAX_TRIES) + " 5 tries"]
HELP_TEXT_POSITION_Y = 600

FIRST_OK_TEXT = "You resolved first serie, let's do the second"

WON_TEXTS= ["You FOUND 6 GLYPHS BUT not the one you need", "____ DATA DISCOVER PATH","DEFEND MESSAGE ____ IDEA"]
WON_TEXT_POSITION_Y = 150

MQTT_SERVER = "192.168.1.121"
MQTT_PORT = 1883

