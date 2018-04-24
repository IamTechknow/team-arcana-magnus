# Low Tech Puzzle Station

## Introduction
The visitor is presented with a lock to a safe or door that contains two glyphs needed for the final puzzle. The lock may be unlocked by reproducing the correct combination set by moving the knob in certain directions. The visitor must conduct a scavenger hunt to find all relevant intel to solve the puzzle.

## Minimum Specification
A variety of locations should be searched to find the intel needed to open the lock. These may include:
* Messages written throughout the structure or on non removable dead drops. This can be a sentence, flavor text, a portal name or intel link to a portal, or gibberish.
* Messages represented by LED art
* Messages under objects or on the floor
* False messages that are misleading (this is the Trickster archetype after all)

These need some tech expertise:
* When some puzzles aren't being used, turn on some LEDs to create shapes
* LED lighting can display hints
* Create a WiFi network others can connect to and display a photo, like a pirate box (I have a Wi-Fi microcontroller, can use RPi 3 too)

An order is needed to figure out the right combination of left, right, up, and down movements. For example, associate a direction to a letter, then require visitors to form a long word from clues, then the letters can be converted to directions to open the lock.

This puzzle does not interact with data from the Tecthultu and does not require changes when the portal level is 8.

## Puzzle Flow
* Visitor locates 4-6 clues for the passcode, and 4-6 clues that map a letter to an arrow, for a total of 10 clues
* Visitor uses this information to determine the passcode and the combination
* Visitor opens the combination lock

## Design Notes
* Fake information could be references, such as the Konami Code or rumors like when Ingress Prime will come out
* We will need to place hints regarding the correct order of the combination. One way is to use a phrase which may be translated to direction arrows, require visitors to form a long word from clues, then the letters can be converted to directions to open the lock
* For instance, one can find 4 places that say something like "P" = "E" left, "A" = up, "S" = "O" = down, "C" = "D" = up. A 5th dead drop says passcode. It can be implied that the combination is Left Up Down Down Up Down Up Left
* We can use a sentence and highlight certain letters for both hints and fake information. For example, highlight letters that say “Made you look”

## Materials
* [Speed Combination Lock](https://www.lowes.com/pd/Master-Lock-2-125-in-Multi-Color-Steel-Shackle-Combination-Padlock/3120695?cm_mmc=SCE_PLA-_-RoughPlumbingElectrical-_-Padlocks-_-3120695:Master_Lock)
