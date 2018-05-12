#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>

#define BTN1PIN 28
#define BTN2PIN 29

//Interrupt handler function
void btnInt(int gpio, int level, uint32_t tick) {
	if(gpio == BTN1PIN)
		printf("Button 1: Interrupt level %d at %u\n", level, tick);
	else if(gpio == BTN2PIN)
		printf("Button 2: Interrupt level %d at %u\n", level, tick);
}

int main(int argc, char **argv) {
	//Set input pins, pull down configuration, and interrupt (no timeout)
	gpioInitialise();
	gpioSetMode(BTN1PIN, PI_INPUT);
	gpioSetMode(BTN2PIN, PI_INPUT);
	gpioSetPullUpDown(BTN1PIN, PI_PUD_DOWN);
	gpioSetPullUpDown(BTN2PIN, PI_PUD_DOWN);
	gpioSetISRFunc(BTN1PIN, RISING_EDGE, 0, btnInt);
	gpioSetISRFunc(BTN2PIN, RISING_EDGE, 0, btnInt);

	unsigned int ch = 0;
	while(ch != 'Q' && ch != 'q')
		ch = getchar();

	gpioTerminate();
	return 0;
}
