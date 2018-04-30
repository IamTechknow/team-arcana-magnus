#include "led-matrix.h"

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pigpio.h>
#include "flappy_xm.h"

using rgb_matrix::RGBMatrix;

//Game states
enum State {IDLE, GAME, WIN_ANIM};

//Game settings
State gameState = IDLE;
float fps = 3.0f;
Color cyan(0, 255, 255);
float xmLeftY = 7.0f, xmRightY = 7.0f;
float obstacleLeftX = 32.0f, obstacleRightX = 0f;
float gapLeftY = 8.0f, gapRightY = 8.0f;
int delay_speed_usec = 1000000 / speed;

//Handle ctrl-C
volatile bool interrupt_received = false;
static void InterruptHandler(int signo) {
  interrupt_received = true;
}

//Button interrupt
void btnInt(int gpio, int level, uint32_t tick)
{
    static int c=1;
    printf("Interrupt #%d level %d at %u\n", c, level, tick);
    c++;
   
    if(gameState == IDLE && level == 1)
		resetGame();
    else if(level == 1) { //rising edge, did not timeout
        if(gpio == BTN1PIN)
			jump1();
		else
			jump2();
	}
}

void drawObstacles() {
	
}

//Returns whether or not there is a collision and the game should end
bool checkCollision() {
	return xmLeftY < gapLeftY || xmLeftY > gapLeftY + 7 || xmRightY < gapRightY || xmRightY > gapRightY + 7
}

void updateGame() {
	xmLeftY += 1.0f;
	xmRightY += 1.0f;
	
	if(xmLeftY >= ROWS || xmRightY >= ROWS)
		gameOver();
}

void gameOver() {
	gameState = IDLE;
}

void resetGame() {
	xmLeftY = 7.0f;
	xmRightY = 7.0f;
	obstacleLeftX = 32.0f;
	obstacleRightX = 0f;
	gapLeftY = 8.0f; 
	gapRightY = 8.0f;
	gameState = GAME;
}

void jump1() {
	if(xmLeftY > 0)
		xmLeftY -= 0.5;
}

void jump2() {
	if(xmRightY > 0)
		xmRightY -= 0.5;
}

int main(int argc, char **argv) {
	int BTN1PIN = 3, BTN2PIN = 5;
	
	//Init Buttons and rising edge interrupts
	gpioInitialise();
	gpioSetMode(BTN1PIN, PI_INPUT);
	gpioSetMode(BTN2PIN, PI_INPUT);
	gpioSetPullUpDown(BTN1PIN, PI_PUD_UP);
	gpioSetPullUpDown(BTN2PIN, PI_PUD_UP);
	gpioSetISRFunc(BTN1PIN, RISING_EDGE, 1000, btnInt);
	gpioSetISRFunc(BTN2PIN, RISING_EDGE, 1000, btnInt);
	
	//Init Matrix
	RGBMatrix::Options opts;
	rgb_matrix::RuntimeOptions runtime_defaults;
	
	//Using 2 32x16 matrices, drop sudo 
	opts.hardware_mapping = "regular";
	opts.chain_length = 2;
	opts.rows = ROWS;
	opts.cols = COLS;
	opts.pwm_bits = 5; //less PWM bits = less CPU time
	runtime_defaults.drop_privileges = 1;
	
	RGBMatrix *matrix = rgb_matrix::CreateMatrixFromOptions(&opts, &runtime_defaults);
	if (matrix == NULL) {
		return 1;
	}
	
	signal(SIGTERM, InterruptHandler);
	signal(SIGINT, InterruptHandler);
	
	// Create a new canvas to be used with led_matrix_swap_on_vsync
	FrameCanvas *offscreen_canvas = matrix->CreateFrameCanvas();
	
	while (!interrupt_received) {
		offscreen_canvas->Clear();
		
		//Draw current game data here!
		//updateGame();
		
		usleep(delay_speed_usec);
		
		// Swap the offscreen_canvas with canvas on vsync, avoids flickering
		offscreen_canvas = canvas->SwapOnVSync(offscreen_canvas);
	}
	
	matrix->Clear();
	delete matrix;
	gpioTerminate();
	
	return 0;
}
