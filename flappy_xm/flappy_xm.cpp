#include <string>
#include <unordered_set>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pigpio.h>
#include <MQTTClient.h>
#include "flappy_xm.h"
#include "glyph_drawing.cpp"

using namespace rgb_matrix;

//Game states
enum State {IDLE, GAME, WIN_ANIM, LOSE_ANIM, LOSE_TEXT, SHOW_GLYPHS};

//Game colors
Color cyan(0, 255, 255), purple(255, 0, 255);

//Game vars
State gameState = IDLE;
float xmLeftY, xmRightY, xmLeftX, xmRightX;
float obstacleLeftX = 32.0F, obstacleRightX = 0;
float gapLeftY = 8.0, gapRightY = 8.0;
int portalLevel = 0;
int currFrames;

//Allow coordinates to be hashable
//See Method 1 in http://marknelson.us/2011/09/03/hash-functions-for-c-unordered-containers/
typedef pair<int,int> Coord;
size_t coord_hash(const Coord &c) {
    return hash<int>()(c.first) ^ hash<int>()(c.second);
}

//Obstacles info
static unordered_set<pair<int, int>, decltype(&coord_hash)> coordsSet(1000, coord_hash);
vector<Glyph> currObstacles;
vector<int> toDelete;
vector<vector<pair<int, int>>> allGlyphs = { breathe, easy, soul, gain, create, mystery, civil, war };

//Game settings
float fps = 10.0, text_fps = 7.0;
int delay_usec = 1000000 / fps, text_delay = 1000000 / text_fps;
float jump_rate, fall_rate;
bool hardMode = false; //only set when game starts, so portal changes don't affect current game
Color color = cyan;

//Text variables
std::string idleLine = "Press buttons to play Flappy XM", gameOverStr = "Game over!", youWin = "You win!";
Color bg_color(0, 0, 0);
int x, x_orig;

//Handle ctrl-C
volatile bool interrupt_received = false;
static void InterruptHandler(int signo) {
  interrupt_received = true;
}

//Button interrupt, triggers variables that get checked when FSM updates
//Also handle the button debouncing here.
static volatile uint32_t prev_tick, prev2_tick;
volatile bool buttonPressed = false, button2Pressed = false;
void btnInt(int gpio, int level, uint32_t tick) {
	uint32_t diff;
    if(gpio == BTN1PIN) {
		diff = tick - prev_tick;
		if(diff > DEBOUNCE_TIME_US) { //next button press cannot come before 1/2 second after last valid one
			prev_tick = tick;
			printf("Button 1: Interrupt level %d at %u\n", level, tick);
			buttonPressed = true;
		}
	} else {
		diff = tick - prev2_tick;
		if(diff > DEBOUNCE_TIME_US) {
			prev2_tick = tick;
			printf("Button 2: Interrupt level %d at %u\n", level, tick);
			button2Pressed = true;
		}
	}
}

//Callback for message arrival
int msg_arrived(void *context, char *topicName, int topicLen, MQTTClient_message *message) {
	//Changes to portal level changes game settings. Only change during idle state for now
	if(gameState == IDLE) {
		char *payload = (char*) message->payload;
		portalLevel = std::strtol(payload, NULL, 10); //Parse value, don't use end pointer

		//Set color based on level
		color = portalLevel == 8 ? purple : cyan;
	}

	MQTTClient_freeMessage(&message);
	MQTTClient_free(topicName);
	return 1;
}

void conn_lost(void *context, char* cause) {
	printf("Connection lost, cause: %s\n", cause);
}

//Draw a glyph onto the canvas, given the origin coordinates and the coordinate vector.
//SetPixel takes X and Y coordinates
void drawGlyph(FrameCanvas* canvas, int r_orig, int c_orig, const vector<pair<int, int>> arr) {
	for(auto coord : arr)
		canvas->SetPixel(coord.second + c_orig, coord.first + r_orig, color.r, color.g, color.b);
}

void drawObstacles(FrameCanvas *canvas) {
	for(Glyph g : currObstacles)
		for(auto coord : g.getData())
			canvas->SetPixel(coord.second + (int) g.getOrigin().second, coord.first + (int) g.getOrigin().first, color.r, color.g, color.b);
}

//Set the pixels for the two XM particles
void drawXM(FrameCanvas* canvas) {
	canvas->SetPixel(xmLeftX, (int) xmLeftY, color.r, color.g, color.b);
	canvas->SetPixel(xmRightX, (int) xmRightY, color.r, color.g, color.b);
}

//Returns whether or not there is a collision and the game should end
//We can do this in constant time by checking if the XM particle coordinates overlap
bool checkCollision() {
	auto pair1 = make_pair(xmLeftX, (int) xmLeftY);
	auto pair2 = make_pair(xmRightX, (int) xmRightY);

	return coordsSet.find(pair1) != coordsSet.end() || coordsSet.find(pair2) != coordsSet.end();
}

//Update game values that will be used to update the matrices, and return whether the game should be over
bool updateGame() {
	xmLeftY += fall_rate; //Move down players every 1/3 a second
	xmRightY += fall_rate;
	currFrames++;

	//Determine if a new glyph should spawn, then spawn one for each matrix
	if(currFrames % SPAWN_THRESHOLD == 1) {
		printf("Creating glyphs...\n");
		int rand_x = rand() % 12, rand_idx = rand() % 8;
		currObstacles.push_back(Glyph(make_pair(rand_x, COLS), allGlyphs[rand_idx], GLYPH_LENGTHS[rand_idx], true));
		currObstacles.push_back(Glyph(make_pair(rand_x, COLS), allGlyphs[rand_idx], GLYPH_LENGTHS[rand_idx], false));
	}

	//Update all existing glyphs. If a glyph should disappear, queue its index
	for(size_t i = 0; i < currObstacles.size(); i++) {
		Glyph temp = currObstacles[i];
		if(temp.getOrigin().second + temp.getLength() < 0) {
			toDelete.push_back(i);
			printf("Destroying glyph...\n");
		} else
			currObstacles[i].updateOrigin();
	}

	for(int i : toDelete)
		currObstacles.erase(currObstacles.begin() + i);
	toDelete.clear();

	//Update the coordinate set
	coordsSet.clear();
	for(Glyph g : currObstacles)
		for(auto pair : g.getData())
			coordsSet.insert(make_pair(pair.second + g.getOrigin().second, pair.first + g.getOrigin().first));

	return checkCollision() || xmLeftY >= ROWS || xmRightY >= ROWS || xmLeftY < 0.0 || xmRightY < 0.0;
}

//Start scrolling the Game over text
void gameOver() {
	printf("Game over\n");
}

//Reset values and start a new game
void resetGame() {
	hardMode = portalLevel == 8;
	fall_rate = hardMode ? 0.4 : 0.2;
	jump_rate = hardMode ? 1.2 : 1.0;
	currFrames = 0;
	xmLeftY = xmRightY = XM_START_Y;
	xmLeftX = hardMode ? XM1_HARD_X : XM1_X;
	xmRightX = hardMode ? XM2_HARD_X : XM2_X;
	obstacleLeftX = 32.0;
	obstacleRightX = 0;
	coordsSet.clear();
	currObstacles.clear();
	toDelete.clear();
	printf("Starting new game...\n");
}

//Raise the position of the left and right players (accounts for gravity too)
void jump1() {
	if(xmLeftY > 0)
		xmLeftY -= jump_rate;
}

void jump2() {
	if(xmRightY > 0)
		xmRightY -= jump_rate;
}

//Draw text on the screen and update the given x variable.
int updateScrollText(FrameCanvas *canvas, const Font &font, int x, const char *str) {
	int length = DrawText(canvas, font, x, 0 + font.baseline(), color, &bg_color, str, 0);

	if (--x + length < 0)
		x = x_orig;

	return x;
}

std::string printState(State state) {
	std::string str;
	switch(state) {
		case WIN_ANIM:
			str = "WIN_ANIM";
			break;
		case LOSE_ANIM:
			str = "LOSE_ANIM";
			break;
		case LOSE_TEXT:
			str = "LOSE_TEXT";
			break;
		case GAME:
			str = "Game";
			break;
		case SHOW_GLYPHS:
			str = "Show Glyphs";
			break;
		default:
			str = "Idle";
	}
	return str;
}

void processState() {
	State newState = gameState;
	//Transition from the animation states to the idle state
	if(gameState == LOSE_ANIM && x == 80)
		newState = LOSE_TEXT;

	if(gameState == LOSE_TEXT && x == -80) { //Text is going through left matrix
		newState = IDLE;
		x = x_orig;
	}

	if(gameState == WIN_ANIM && x == -60)
		newState = SHOW_GLYPHS;

	if(gameState == SHOW_GLYPHS) {
		usleep(3000000);
		newState = IDLE;
		x = x_orig;
	}

	//Manage button presses
	if(buttonPressed) {
		if(gameState == IDLE) {
			resetGame();
			newState = GAME;
		} else if(gameState == GAME)
			jump1();

		buttonPressed = false;
	}

	if(button2Pressed) {
		if(gameState == GAME)
			jump2();

		button2Pressed = false;
	}

	//Update game variables
	if(gameState == GAME) {
		bool hasCollision = updateGame();

		if(hasCollision) {
			gameOver();
			newState = LOSE_ANIM;
			x = 0;
		} else if((!hardMode && currFrames >= FRAMES_TO_WIN) || (hardMode && currFrames >= FRAMES_TO_WIN_LVL8)) {
			newState = WIN_ANIM;
			x = x_orig;
		}
	}

	if(gameState != newState) {
		printf("Transitioning from %s to %s\n", printState(gameState).c_str(), printState(newState).c_str());
		gameState = newState;
	}
}

int main(int argc, char **argv) {
	//Init Buttons and rising edge interrupts
	gpioInitialise();
	prev_tick = gpioTick();
	prev2_tick = prev_tick;
	gpioSetMode(BTN1PIN, PI_INPUT);
	gpioSetMode(BTN2PIN, PI_INPUT);
	gpioSetPullUpDown(BTN1PIN, PI_PUD_DOWN);
	gpioSetPullUpDown(BTN2PIN, PI_PUD_DOWN);
	gpioSetISRFunc(BTN1PIN, RISING_EDGE, 0, btnInt);
	gpioSetISRFunc(BTN2PIN, RISING_EDGE, 0, btnInt);

	//Init MQTT
/*	MQTTClient client;
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
*/
	//Init Matrix
	RGBMatrix::Options opts;

	//Using 2 32x16 matrices, drop sudo
	opts.hardware_mapping = "regular";
	opts.chain_length = 2;
	opts.rows = ROWS;
	opts.cols = COLS;
	opts.brightness = 50;
	opts.pwm_bits = 3; //less PWM bits = less CPU time
	x_orig = (opts.chain_length * opts.cols) + 5;
	x = x_orig;

	//Load Font
	Font the_font;
	if(!the_font.LoadFont("led_matrix/fonts/8x13.bdf")) {
		printf("Couldn't load the specified font. Exiting...\n");
		return 1;
	}

	RuntimeOptions runtime_defaults;
	runtime_defaults.drop_privileges = 1;

	RGBMatrix *matrix = rgb_matrix::CreateMatrixFromOptions(opts, runtime_defaults);
	if (matrix == NULL) {
		printf("Matrix creation failed! Exiting...\n");
		return 1;
	}

	signal(SIGTERM, InterruptHandler);
	signal(SIGINT, InterruptHandler);
	printf("Program initialized. Running...\n");

	// Create a new canvas to be used with led_matrix_swap_on_vsync
	FrameCanvas *offscreen_canvas = matrix->CreateFrameCanvas();

	while (!interrupt_received) {
		offscreen_canvas->Clear();

		//Process the state machine, update the matrices
		processState();
		switch(gameState) {
			case SHOW_GLYPHS:
				drawGlyph(offscreen_canvas, 3, 4, knowledge);
				drawGlyph(offscreen_canvas, 3, 4 + COLS, knowledge);
				drawGlyph(offscreen_canvas, 3, 15, idea);
				drawGlyph(offscreen_canvas, 3, 15 + COLS, idea);
				break;

			case WIN_ANIM:
				x = updateScrollText(offscreen_canvas, the_font, x, youWin.c_str());
				break;

			case LOSE_ANIM:
				drawObstacles(offscreen_canvas);
				if((x % 20) < 10)
					drawXM(offscreen_canvas);
				else {
					offscreen_canvas->SetPixel(xmLeftX, (int) xmLeftY, 0, 0, 0);
					offscreen_canvas->SetPixel(xmRightX, (int) xmRightY, 0, 0, 0);
				}
				x++;
				break;

			case LOSE_TEXT:
				x = updateScrollText(offscreen_canvas, the_font, x, gameOverStr.c_str());
				break;

			case GAME:
				drawXM(offscreen_canvas);
				drawObstacles(offscreen_canvas);
				break;
			default:
				x = updateScrollText(offscreen_canvas, the_font, x, idleLine.c_str());
		}

		// Swap the offscreen_canvas with canvas on vsync, avoids flickering
		offscreen_canvas = matrix->SwapOnVSync(offscreen_canvas);

		usleep(gameState == GAME ? delay_usec : text_delay / the_font.CharacterWidth('W'));
	}

	printf("Exiting on Ctrl-C...\n");
	gpioTerminate();
//	MQTTClient_disconnect(client, TIMEOUT);
//	MQTTClient_destroy(&client);
	matrix->Clear();
	delete matrix;

	return 0;
}
