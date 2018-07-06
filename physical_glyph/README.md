# Physical Glyph (Final) Station

## Introduction
The Physical Glyph station allows the visitor to make use of all the information collected from the other puzzle stations. Glyphs must be entered in the correct order to solve this puzzle, upon doing so a prize is awarded. To input the glyphs, one must use a special wand shaped device and press a button to start the puzzle. From there on, the wand must be pointed to the glyph nodes which will light up LEDs indicating what the current glyph being entered looks like. Once all LEDs are lit up or the button is pressed the user may move on to the next glyph. 

In other words, hand gestures are used to draw glyphs, not finger swipes!

## Minimum Specification
* A disc will be laser cut with square holes to resemble glyph nodes
* The disc must be secured by the walls of the structure and there must be adequate space for all electronics
* Each hole will have its own infrared detector circuit
* Each IR detector circuit must support a range of 1-2 feet and only turn on when IR in a certain frequency is detected. It must not turn on by ambient lighting.
* Each circuit must provide a digital output for the microcontroller indicating IR is detected
* The microcontroller to use must support at least 24 GPIO pins, 22 for each set of IR circuit and a LED to indicate it has detected IR during a glyph, 1 for the wand button, and 1 for an actuator that releases the swag prize. Networking is not required.
* A wand device shall emit the IR at a certain frequency that is to be detected by any IR circuit. It is controlled by a button to allow the user to finish a glyph or start the puzzle. The button output must be debounced.
* When enough glyphs have been entered, the LEDs will light up to indicate whether the sequence of glyphs were correct or not. If they were, a check will be shown, and the actuator will turn to release a prize. Otherwise a cross is shown. The wand button when pressed will now start go to the initial screen.
* The microcontroller program must keep track of the glyphs recorded, and game states including initial idle, puzzle in session, and when the puzzle has ended.
* In the initial idle state the LEDs could show a hint for the Low Tech puzzle.

## Glyph order
| Glyph     |
| --------- |
| Search    |
| Answer    |
| Gain      |
| Unbounded |
| Knowledge |
| Idea      |

## Materials
* Wooden or card board to cut holes that resemble a glyph interface pattern.
* Microcontroller with lots of ports, either a PSoC 5LP or Arduino Mega 2560
* Fabricated PCBs, solder, solder paste, and an iron
* 22 and 24 gauge solid core wiring
* An actuator (servo or motor) and H-Bridge if motor is needed
* Push Button
* IR detection circuit materials:
   * Phototransistors
   * IR Emitter
   * LM339 Comparator
   * Op-Amps
   * Resistors
   * Capacitors
   * Voltage regulators
   * Diodes
   * LEDs

## Program Description
The program will be run by a PSoC 5LP development board, which contains enough interrupt perpherials for all of our IR detector inputs and a button. Digital outputs will be connected to LEDs. The IR detectors have an active low output, due to the use of an inverting Schmitt Trigger to snap the output to digital low or high.

The microcontroller program can transition through three states, the idle or default state, the game state, and an ending state. In the idle state the game is waiting to begin with a push of a button so the LEDs are off, and can also display a hint for the low tech puzzle hint. When the button is pressed, the game begins and will allow the user to input the first glyph by waving the wand to the LEDs, which are all lit up. When a IR detector input goes low, the LED will turn off so the user can tell what shape they are trying to draw. When the user is finished with that glyph, he or she will press the button again to start the next glyph. When the last glyph is drawn, the game will transition to the ending state where it will let the user know whether it has succeeded or failed, with a check or X glyph. 

To check if the drawn glyph is correct, we can define our own glyph definitions and check whether or not a drawn glyph is the same by putting all drawn nodes into a simple boolean array that can act as a set. This also means order will not matter here unlike in Ingress. All correct glyphs will have no more than 11 nodes to connect, so if a user draws a glyph with more than 11 glyphs it cannot be valid.

If possible we can try to record how long the button is pressed by using both rising and falling interrupts to be able to implement an undo function.

## AAR
An [AAR](https://docs.google.com/document/d/1Uy8Y4W4OLF-Iq5YLK9eRnNFhhYjXUx_bJ7s4a8xR_as/edit#) has been written detailing the bring up of this project component.