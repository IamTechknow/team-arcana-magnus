#include "project.h"
#include "glyphs.h"
#define CORRECT_BIT_MASK 0b00111111

//Program states
enum State {INIT, GAME, FAILED, SOLVED};

//Global variables
enum State state;

//Whether the button was Pressed
volatile uint8 buttonPressed;

//Indices for glyph, node, and value of last Node
volatile uint8 glyphCount, nodeCount, lastNode;
uint8 currGlyphs[NUM_GLYPHS][NUM_NODES]; //Glyph node values are one-indexed
uint8 currLEDStatus[NUM_NODES];
uint8 IRMap[] = {1, 2, 9, 0, 4, 5, 3, 6, 7, 8, 10}; //Map 0-index detectors to 0-index LED positions (e.g. detector 2+1 is at position 9)

//Button interrupt. Interrupts need to be cleared in the ISR
//It is possible for the variable to be more than one, but not by the interrupt
//so it gets reset when read
CY_ISR(ButtonISR) {
    if(state != SOLVED || state != FAILED) {
        buttonPressed = 1;
    }
    ButtonInt_ClearPending();
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
        currGlyphs[glyphCount][nodeCount] = IRMap[ir_idx] + 1; //IR index is 1-indexed
        currLEDStatus[ir_idx] = 1;
        nodeCount++;
        lastNode = ir_idx;
    }
    IR_detector_ClearInterrupt();
}

CY_ISR(IRPort5ISR) {
    //Port 5 interrupt, identify the pin triggered
    uint8 port5_state = IR_detector_2_Read();
    
    //Find the pin in which the IR detector is set low
    uint8 ir_idx = 0;
    while((port5_state & 1 << ir_idx) != 0)
        ir_idx++;
    
    //update the current glyph for the last 3 nodes
    ir_idx += 8; //Either detector 8, 9, or 10
    if(nodeCount < NUM_NODES && ir_idx < 11 && ir_idx != lastNode) {
        currGlyphs[glyphCount][nodeCount] = IRMap[ir_idx] + 1; //IR index is 1-indexed
        currLEDStatus[ir_idx] = 1;
        nodeCount++;
        lastNode = ir_idx;
    }
    IR_detector_2_ClearInterrupt();
}

uint8 checkGlyphs() { //Form bit vector based on result
    uint8 result = 0;
    
    result |= checkGlyph(currGlyphs[0], getBodyGlyph()) << 0;
//    result |= checkGlyph(currGlyphs[1], getAnswerGlyph()) << 1;
//    result |= checkGlyph(currGlyphs[2], getGainGlyph()) << 2;
//    result |= checkGlyph(currGlyphs[3], getUnboundedGlyph()) << 3;
//    result |= checkGlyph(currGlyphs[4], getKnowledgeGlyph()) << 4;
//    result |= checkGlyph(currGlyphs[5], getIdeaGlyph()) << 5;
    
    return result;
}

//Turn off LEDs in the idle state
void turnOffLEDs() {
    Port_3_Write(0);
    Port_12_Write(0);
}

//Process button presses in the game
void processButtonInGame() {
    if(buttonPressed >= 1) {
        buttonPressed = 0;
        nodeCount = 0;
        glyphCount++;
        memset(currLEDStatus, 0, NUM_NODES); //zero out LEDs
    }
}

//Turn on the LEDs that for IR detectors that have detected IR
void setLEDsInGame() {
    uint16 mask = 0, mask_2 = 0;
    
    for(int i = 0; i < 8; i++)
        if(currLEDStatus[i])
            mask |= (1 << (i) );
    Port_3_Write(mask & 0xff);
    
    for(int i = 8; i < NUM_NODES; i++)
        if(currLEDStatus[i])
            mask_2 |= (1 << (i - 8) );
    Port_12_Write(mask_2 & 0xff);
}

void showUseGlyph() { //For now, blink lights for 2 seconds
    for(int i = 0; i < 10; i++) {
        Port_3_Write(0);
        Port_12_Write(0);
        CyDelay(100);
        Port_3_Write(0b00100010);
        Port_12_Write(0b00000001);
        CyDelay(100);
    }
    state = INIT;
}

void showFailedGlyph() { //For now, blink lights for 2 seconds
    for(int i = 0; i < 2; i++) {
        Port_3_Write(0);
        Port_12_Write(0);
        CyDelay(500);
        Port_3_Write(0b11111111);
        Port_12_Write(0b00000111);
        CyDelay(500);
    }
    state = INIT;
}

void updateFSM() {
    if(state == INIT && buttonPressed == 1) { //New game, reset variables
        state = GAME;
        buttonPressed = 0;
        nodeCount = 0;
        glyphCount = 0;
        lastNode = 0xFF; //0 is used for first pin in port
        
        memset(currLEDStatus, 0, NUM_NODES);
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
    Port5ISR_StartEx(IRPort5ISR);
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
                showFailedGlyph();
                break;
            
            default:
                turnOffLEDs();
        }
    }
}
/* [] END OF FILE */
