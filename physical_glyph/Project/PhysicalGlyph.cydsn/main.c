#include "project.h"
#include "glyphs.h"
#define NUM_GLYPHS 1
#define NUM_NODES 11
#define CORRECT_BIT_MASK 0b00000001

//Program states
enum State {INIT, GAME, FAILED, SOLVED};

//Global variables
enum State state;

//Whether the button was Pressed
volatile uint8 buttonPressed;

//Indices for glyph, node, and value of last Node
volatile uint8 glyphCount, nodeCount, lastNode;
uint8 currGlyphs[NUM_GLYPHS][NUM_NODES]; //Glyph node values are one-indexed

//Button interrupt. Interrupts need to be cleared in the ISR
//It is possible for the variable to be more than one, so it gets reset when read
CY_ISR(ButtonISR) {
    if(state != SOLVED || state != FAILED) {
        buttonPressed++;
    }
    ButtonPin_ClearInterrupt();
}

//IR Port 1 interrupt, falling edge
CY_ISR(IRPortISR) {
    //Port 0 interrupt, identify the pin triggered
    uint8 port_state = IR_detector_Read();
    
    //Find the pin in which the IR detector is set low
    uint8 ir_idx = 0;
    while((port_state & 1 << ir_idx) != 0)
        ir_idx++;
    
    //update the current glyph
    if(nodeCount < NUM_NODES && ir_idx < 8 && ir_idx != lastNode) {
        currGlyphs[glyphCount][nodeCount] = ir_idx + 1; //IR index is 1-indexed
        nodeCount++;
        lastNode = ir_idx;
    }
    
    IR_detector_ClearInterrupt();
}

uint8 checkGlyphs() { //Form bit vector based on result
    uint8 result = 0;
    for(int i = 0; i < NUM_GLYPHS; i++)
        result |= checkGlyph(currGlyphs[i], getBodyGlyph()) << i;
    
    return result;
}

//Turn off LEDs in the idle state
void turnOffLEDs() {
    Port_3_Write(0);
}

//Process button presses in the game
void processButtonInGame() {
    if(buttonPressed >= 1) {
        buttonPressed = 0;
        nodeCount = 0;
        glyphCount++;
    }
}

//Turn off the LEDs that for IR detectors that have detected IR
void setLEDsInGame() {
    uint16 mask = 0; //Get all 1s, then reset desired pins
    
    for(int i = 0; i < NUM_NODES; i++) 
        if(currGlyphs[glyphCount][i]) 
            mask |= (1 << (currGlyphs[glyphCount][i] - 1) ); //IR index is 1-indexed 
    Port_3_Write(mask & 0xff);
    //Write the last 3 bits here
}

void showUseGlyph() {
    //For now, blink lights for 2 seconds
    for(int i = 0; i < 2; i++) {
        Port_3_Write(0);
        CyDelay(500);
        Port_3_Write(0xFF);
        CyDelay(500);
    }
    state = INIT;
}

void updateFSM() {
    if(state == INIT && buttonPressed >= 1) { //New game, reset variables
        state = GAME;
        buttonPressed = 0;
        nodeCount = 0;
        glyphCount = 0;
        lastNode = 0xFF; //0 is used for first pin in port
        
        for(int i = 0; i < NUM_GLYPHS; i++) //reset glyph data
            memset(currGlyphs[i], 0, NUM_NODES);
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
    Port0ISR_StartEx(IRPortISR);
    state = INIT;

    for(;;) {
        updateFSM();
        
        switch(state) { //Process FSM
            case GAME:
                processButtonInGame();
                setLEDsInGame();
                break;
            
            case SOLVED:
                showUseGlyph();
                break;
            
            case FAILED:
                showUseGlyph();
                break;
            
            default:
                turnOffLEDs();
        }
    }
}
/* [] END OF FILE */
