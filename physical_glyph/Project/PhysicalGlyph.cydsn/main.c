#include "project.h"
#include "glyphs.h"
#define NUM_GLYPHS 1
#define NUM_NODES 11
#define CORRECT_BIT_MASK 0b00000001

//Program states
enum State {INIT, GAME, FAILED, SOLVED};

//Global variables
enum State state;
volatile uint8 buttonPressed;
uint8 glyphCount;
uint8 currGlyphs[NUM_GLYPHS][NUM_NODES]; //Glyph node values are one-indexed

//Button interrupt
CY_ISR(ButtonISR) {
    buttonPressed = 1;
}

//IR Port 1 interrupt, falling edge
CY_ISR(IRPortISR) {
    //Port 0 interrupt, identify the pin triggered
    uint8 port_state = IR_detector_Read();
    uint8 IR1triggered = (port_state & 1) == 0;
    uint8 IR2triggered = (port_state & 1 << 1) == 0;
    uint8 IR3triggered = (port_state & 1 << 2) == 0;
}

uint8 checkGlyphs() {
    uint8 result = 0;
    uint8* expected = getBodyGlyph();
    
    //Compare Glyphs
    for(int i = 0; i < NUM_GLYPHS; i++) {
        uint8 expectedNodes = 0, currNodes = 0;
        uint8 expectedSet[NUM_NODES], currSet[NUM_NODES];
        uint8* currGlyph = currGlyphs[i];
        
        //Build boolean hash sets
        for(int j = 0; j < NUM_NODES; j++) {
            if(expected[j] && !expectedSet[expected[j]]) {
                expectedNodes++; //Count all nodes that have been set
                expectedSet[expected[j]] = 1;
            }
            
            if(currGlyph[j] && !currSet[currGlyph[j]]) {
                currNodes++;
                currSet[expected[j]] = 1;
            }
        }
        
        //check size, then compare contents which must be identical
        if(expectedNodes == currNodes) { 
            uint8 sameValues = 0, j = 0;
            while(j <= NUM_NODES && expected[j] == currSet[j])
                j++;
            
            if(sameValues == NUM_NODES + 1)
                result |= 1 << i;
        }
    }
    
    return result;
}

//Turn off LEDs in the idle state
void turnOffLEDs() {
    Port_0_Write(0);
    Pin_2_Write(0);
}

//Turn off the LEDs that for IR detectors that have detected IR
void turnOffLEDsInGame() {
    uint16 mask = ~0; //Get all 1s, then reset desired pins
    
    for(int i = 0; i < NUM_NODES; i++) 
        if(glyphCount && currGlyphs[glyphCount][i]) 
            mask &= ~(1 << currGlyphs[glyphCount][i]);
        
    Port_0_Write(mask & 0xff);
}

void updateFSM() {
    if(state == INIT && buttonPressed) {
        state = GAME;
        buttonPressed = 0;
        glyphCount = 0;
    } else if(state == GAME && glyphCount == NUM_GLYPHS) {
        if(checkGlyphs() == CORRECT_BIT_MASK) 
            state = SOLVED;
        else 
            state = FAILED;
    }
}

int main(void) {
    CyGlobalIntEnable; /* Enable global interrupts. */
    ButtonInt_StartEx(ButtonISR);
    RightISR_StartEx(IRPortISR);
    
    state = INIT;

    for(;;) {
        //Check for events that can change the state machine
        updateFSM();
        
        //Process FSM
        switch(state) {
            case GAME:
                turnOffLEDsInGame();
                break;
            
            case SOLVED:
                
                break;
            
            case FAILED:
                
                break;
            
            default:
                turnOffLEDs();
        }
    }
}

/* [] END OF FILE */
