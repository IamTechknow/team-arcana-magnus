# Flappy XM Game (Two-Player puzzle)

## Introduction
The Flappy XM Game is a cooperative game between two players to reach the center of the mind palace without colliding with any obstacles in order to find out any vital information, very much an Ingress themed Flappy Bird. This is represented by two 16x32 RGB LED Matrices which will display the game environment and two buttons used to control the movement of the XM. The game begins when both players have pressed the corresponding button. When this game is successfully completed, a glyph will show up on both matrices.

## Minimum Specification
* One embedded computing device is used to control both LED Matrices and manage the game state, currently a RPi is used
* Must have network capabilities and subscribe to the “level” topic
* Button input must be debounced and support repeated presses
* One side scrolls to the right while the other scrolls to the left
* During the game, various Ingress glyphs will be shown that serve as obstacles
* The game will end early if either player’s XM collides
* When both players reach the center, then the contents of each LED matrices will become the same and an animation will play before the glyph is shown
* The game is connected to the Techultu integration as follows:
   * Color of the LEDs is determined by the portal level
   * If the portal level is 8 then more obstacles will be present, and the game lasts longer. Movement speed is the same.
* If possible, LED color changes over time instead of instantaneously 

## Materials
* Network connected device, using Raspberry Pi
* [Two 16x32 RGB LED Matrix panel](https://www.adafruit.com/product/420)
* [Two Arcade style buttons](https://www.adafruit.com/product/476)
* [Crimped cables for the buttons](https://www.adafruit.com/product/1152)
* Perfboard, 20-26 gauge wire to securely connect the panels with the Pi

## Setup Information
The microcontroller system must support 20 GPIO pins, 6 data pins for both panels each, 6 control pins to be shared amongst both panels, which means they are updated at the same time. Two pins for buttons. [Wiring information here](https://learn.adafruit.com/32x16-32x32-rgb-led-matrix/connecting-with-jumper-wires)

Uses a Raspberry Pi 1 Model B with Stretch Lite, overclocked from 700 MHz to 900 MHz, turbo mode on, 8 GB SDHC card
Packages installed for Mosquitto and Python: git libwrap0-dev libssl-dev libc-ares-dev uuid-dev xsltproc mosquitto-clients libmosquitto1 libmosquittopp1 python-pip python3-pip python3-gi python-dev python3-dev 
Python modules: paho-mqtt

Manually installed packages: pigpio, Eclipse Paho for C
