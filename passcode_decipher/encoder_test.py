import RPi.GPIO as gp
import time

OUTPUT1 = 33
OUTPUT2 = 35
LIMIT = 48

#Need to resolve floating outputs by debouncing. Remember that all encoders differ!
#Helpful guides:
#http://howtomechatronics.com/tutorials/arduino/rotary-encoder-works-use-arduino/
#hifiduino.wordpress.com/2010/10/20/rotaryencoder-hw-sw-no-debounce/

#This test harness allows you to test positioning of the rotary encoder (Bounes PEC12R)
#There are 24 detents, and a change in state can occur halfway through a detent.
#The encoder has no "memory" so the location needs to be calibrated and relate to a real world object.
#This code is similar to the Arduino code in how to mechatronics, and works fine for our application.

def setup():
    gp.setmode(gp.BOARD)
    gp.setup(OUTPUT1, gp.IN, pull_up_down=gp.PUD_DOWN)
    gp.setup(OUTPUT2, gp.IN, pull_up_down=gp.PUD_DOWN)

if __name__ == '__main__':
    setup()
    aState = 0
    aLastState = 0
    counter = 0
    
    try:
        while True:
            aState = gp.input(OUTPUT1)

            #If output A has changed, then we can check if rotated CW or CCW
            if aState != aLastState:
                counter += 1 if gp.input(OUTPUT2) != aState else -1
                print(counter)

            if abs(counter) >= LIMIT:
                print("Full rotation complete")
                counter = 0

            aLastState = aState
    finally:
        gp.cleanup()
