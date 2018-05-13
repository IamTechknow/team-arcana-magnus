#ifndef _FLAPPYXM_H_
#define _FLAPPYXM_H_

#define ROWS 16
#define COLS 32
#define BTN1PIN 28
#define BTN2PIN 29
#define BROKER "192.168.1.124:1883"
#define CLIENTID "FlappyClient"
#define TOPIC "portal/levelChange"
#define QOS 0
#define TIMEOUT 10000L

//Function prototypes

void drawObstacle();

bool checkCollision();

void updateGame();

void jump1();

void jump2();

void gameOver();

void resetGame();

#endif
