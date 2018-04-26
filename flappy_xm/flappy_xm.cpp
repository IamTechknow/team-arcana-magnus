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
float fps = 3.0f;
Color cyan(0, 255, 255);
float xmLeftY = 7.0f, xmRightY = COLS - 7.0f;
float obstacleLeftX = 32.0f, obstacleRightX = 0f;
float gapLeftY = 8.0f, gapRightY = 8.0f;
int delay_speed_usec = 1000000 / speed;

//Handle ctrl-C
volatile bool interrupt_received = false;
static void InterruptHandler(int signo) {
  interrupt_received = true;
}

void btnInt(int gpio, int level, uint32_t tick)
{
   static int c=1;
   printf("Interrupt #%d level %d at %u\n", c, level, tick);
   c++;
}

void drawObstacle() {
	
}

bool checkCollision() {
	
}

void updateGame() {
	
}

void jump() {
	
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
		
		
		usleep(delay_speed_usec);
		
		// Swap the offscreen_canvas with canvas on vsync, avoids flickering
		offscreen_canvas = canvas->SwapOnVSync(offscreen_canvas);
	}
	
	matrix->Clear();
	delete matrix;
	gpioTerminate();
	
	return 0;
}
