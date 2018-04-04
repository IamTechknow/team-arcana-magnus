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

## Materials
* Plate of laser cuttable material. Could be foamcore, MDF, acrylic
* Microcontroller with lots of ports, either a PSoC 5LP or Arduino Mega 2560
* Perfboards, soldering material
* 20-26 gauge solid core wiring… and lots of it
* An actuator (servo or motor) and H-Bridge if motor is needed
* IR detection circuit materials:
   * Phototransistors
   * LM339 Comparator
   * Op-Amps
   * Resistors
   * Capacitors
   * Voltage regulators
   * Diodes
   * LEDs
