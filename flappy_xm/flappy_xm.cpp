#include "led-matrix.h"
#include "graphics.h"

#include <string>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pigpio.h>
#include <MQTTClient.h>
#include "flappy_xm.h"

using namespace rgb_matrix;

//Game states
enum State {IDLE, GAME, WIN_ANIM};

//Game settings
State gameState = IDLE;
float fps = 3.0;
Color cyan(0, 255, 255);
float xmLeftY = 7.0, xmRightY = 7.0;
float obstacleLeftX = 32.0F, obstacleRightX = 0;
float gapLeftY = 8.0, gapRightY = 8.0;
int delay_speed_usec = 1000000 / fps;
int portalLevel = 0;

//Handle ctrl-C
volatile bool interrupt_received = false;
static void InterruptHandler(int signo) {
  interrupt_received = true;
}

//Button interrupt
void btnInt(int gpio, int level, uint32_t tick) {
    printf("Interrupt level %d at %u\n", level, tick);

    if(gameState == IDLE && level == 1)
		resetGame();
    else if(level == 1) { //rising edge, did not timeout
        if(gpio == BTN1PIN)
			jump1();
		else
			jump2();
	}
}

//Callback for message arrival
int msg_arrived(void *context, char *topicName, int topicLen, MQTTClient_message *message) {
	char *payload = (char*) message->payload;
	char *end;
	portalLevel = std::strtol(payload, &end, 10);

	MQTTClient_freeMessage(&message);
	MQTTClient_free(topicName);
	return 1;
}

void conn_lost(void *context, char* cause) {
	printf("Connection lost, cause: %s\n", cause);
}

void drawObstacles() {
	
}

//Returns whether or not there is a collision and the game should end
bool checkCollision() {
	return xmLeftY < gapLeftY || xmLeftY > gapLeftY + 7 || xmRightY < gapRightY || xmRightY > gapRightY + 7;
}

void updateGame() {
	xmLeftY += 1.0;
	xmRightY += 1.0;
	
	if(xmLeftY >= ROWS || xmRightY >= ROWS)
		gameOver();
}

void gameOver() {
	gameState = IDLE;
}

void resetGame() {
	xmLeftY = 7.0;
	xmRightY = 7.0;
	obstacleLeftX = 32.0;
	obstacleRightX = 0;
	gapLeftY = 8.0;
	gapRightY = 8.0;
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
	//Init Buttons and rising edge interrupts
	gpioInitialise();
	gpioSetMode(BTN1PIN, PI_INPUT);
	gpioSetMode(BTN2PIN, PI_INPUT);
	gpioSetPullUpDown(BTN1PIN, PI_PUD_DOWN);
	gpioSetPullUpDown(BTN2PIN, PI_PUD_DOWN);
	gpioSetISRFunc(BTN1PIN, RISING_EDGE, 0, btnInt);
	gpioSetISRFunc(BTN2PIN, RISING_EDGE, 0, btnInt);
	
	//Init MQTT
	MQTTClient client;
	MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;

	MQTTClient_create(&client, BROKER, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL);
	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;
	MQTTClient_setCallbacks(client, NULL, conn_lost, msg_arrived, NULL);

	int rc = MQTTClient_connect(client, &conn_opts);
	if(rc != MQTTCLIENT_SUCCESS) {
		printf("Failed to connect, code %d\n", rc);
		return 1;
	}
	MQTTClient_subscribe(client, TOPIC, QOS);

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
	
	RGBMatrix *matrix = rgb_matrix::CreateMatrixFromOptions(opts, runtime_defaults);
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
		offscreen_canvas = matrix->SwapOnVSync(offscreen_canvas);
	}
	
	MQTTClient_disconnect(client, TIMEOUT);
	MQTTClient_destroy(&client);
	matrix->Clear();
	delete matrix;
	gpioTerminate();
	
	return 0;
}
