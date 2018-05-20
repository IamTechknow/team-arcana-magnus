#ifndef _FLAPPYXM_H_
#define _FLAPPYXM_H_

#include "led-matrix.h"
#include "graphics.h"

#define ROWS 16
#define COLS 32
#define BTN1PIN 16 //BCM numbers
#define BTN2PIN 20
#define DEBOUNCE_TIME_US 100000

#define BROKER "192.168.1.124:1883"
#define CLIENTID "FlappyClient"
#define TOPIC "portal/levelChange"
#define QOS 0
#define TIMEOUT 10000L

#define XM1_X 8
#define XM2_X 56
#define XM1_HARD_X 16
#define XM2_HARD_X 48
#define XM_START_Y 8.0
#define FRAMES_TO_WIN 200 //20 seconds
#define FRAMES_TO_WIN_LVL8 400

using namespace rgb_matrix;
using namespace std;

//Function prototypes
void processState();

void drawGlyph(FrameCanvas *canvas, int r_orig, int c_orig, const vector<pair<int, int>> arr);

void drawXM(FrameCanvas *canvas);

bool checkCollision();

bool updateGame();

void jump1();

void jump2();

void gameOver();

void resetGame();

int updateScrollText(FrameCanvas *canvas, const Font &font, int x, const char *str);

#endif

