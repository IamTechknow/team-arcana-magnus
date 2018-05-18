#ifndef _FLAPPYXM_H_
#define _FLAPPYXM_H_

#include "led-matrix.h"
#include "graphics.h"

#define ROWS 16
#define COLS 32
#define BTN1PIN 28 //BCM pins on Header P5
#define BTN2PIN 29

#define BROKER "192.168.1.124:1883"
#define CLIENTID "FlappyClient"
#define TOPIC "portal/levelChange"
#define QOS 0
#define TIMEOUT 10000L

#define XM1_X 8
#define XM2_X 56
#define FRAMES_TO_WIN 60 //20 seconds
#define FRAMES_TO_WIN_LVL8 120

using namespace rgb_matrix;

//Function prototypes
void processState();

void drawObstacles(FrameCanvas *canvas);

void drawXM(FrameCanvas *canvas);

bool checkCollision();

void updateGame();

void jump1();

void jump2();

void gameOver();

void resetGame();

int updateScrollText(FrameCanvas *canvas, Font font, int x, char *str);

#endif

