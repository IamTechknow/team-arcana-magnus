#ifndef _FLAPPYXM_H_
#define _FLAPPYXM_H_

#define ROWS 16
#define COLS 32
#define BTN1PIN 3
#define BTN2PIN 5

//Function prototypes

void drawObstacle();

bool checkCollision();

void updateGame();

void jump1();

void jump2();

void gameOver();

#endif
