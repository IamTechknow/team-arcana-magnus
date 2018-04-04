# Flappy XM Game (Two-Player puzzle)

## Introduction
The Passcode Decipher station will present a visitor with encrypted phrases and a variety of methods which could be used to convert a phrase into something different and ultimately decrypt the phrases to English. This station will involve a monitor and three turnable knobs which will allow the user to switch through available deciphering methods. Up to three phrases may be solved at a time, but there may be more than one set of phrases to go through, depending on the portal level. Deciphering all of the phrases will complete the puzzle and the user is rewarding with a glyph for the final puzzle, as well as any information obtained throughout this puzzle.

## Minimum Specification
* Puzzle consists of a Raspberry Pi full-screen program
* Connects to the Tecthcultu API to obtain portal level information
* The puzzle presents 2 or 3 encrypted ciphers at a time at the top half of the screen, and the bottom half shows the current encryption method and the modified cipher based on the selected method
* Three wooden knobs are connected to three rotary encoders that are connected to the RPi GPIO to allow one to turn the knobs
* The program should be able to detect the turning in real time and adjust the current deciphering method for the corresponding phrase
* If the portal level is 8, then the puzzle cipher will not directly result in an English phrase, instead the correct cipher will be used as the next set of ciphers to be solved.
* When the program starts, it will represent an instruction screen, turning a knob will start the puzzle.
* When part of or all of the puzzle is solved, an animation must show before proceeding with the next part of the puzzle, for a limited amount of time. The finishing animation will go back to the instruction screen.

## Materials
* Raspberry Pi with WiFi capability or dongle
* Rotary Encoders (see inventory for what we have and product links)
* 3D printed or fabricated knobs
* Display monitor
