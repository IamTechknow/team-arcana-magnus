#include "project.h"
#include "glyphs.h"

uint8* getBodyGlyph() {
    static uint8 p[11] = {4, 5, 6, 4, 0, 0, 0, 0, 0, 0, 0};
    return p;
}

uint8* getUseGlyph() {
    static uint8 p[11] = {6, 8, 3, 0, 0, 0, 0, 0, 0, 0, 0};
    return p;
}

uint8* getWrongGlyph() {
    static uint8 p[11] = {2, 4, 6, 8, 10, 3, 5, 6, 7, 9, 0};
    return p;
}

uint8 checkGlyph(uint8* left, uint8* right) {
    uint8 expectedNodes = 0, currNodes = 0, result = 0;
    uint8 expectedSet[NUM_NODES], currSet[NUM_NODES];
    memset(expectedSet, 0, NUM_NODES);
    memset(currSet, 0, NUM_NODES);

    //Build boolean hash sets
    for(int j = 0; j < NUM_NODES; j++) {
        if(right[j] && !expectedSet[right[j]]) {
            expectedNodes++; //Count all nodes that have been set
            expectedSet[right[j]] = 1;
        }

        if(left[j] && !currSet[left[j]]) {
            currNodes++;
            currSet[left[j]] = 1;
        }
    }

    //check size, then compare contents which must be identical
    if(expectedNodes == currNodes) { 
        uint8 j = 0;
        while(j < NUM_NODES && expectedSet[j] == currSet[j])
            j++;

        result = j == NUM_NODES;
    }
    return result;
}

uint8* getSearchGlyph() {
    static uint8 p[11] = {8, 7, 4, 5, 6, 0, 0, 0, 0, 0, 0};
    return p;
}

uint8* getAnswerGlyph() {
    static uint8 p[11] = {4, 5, 8, 6, 0, 0, 0, 0, 0, 0, 0};
    return p;
}

uint8* getGainGlyph() {
    static uint8 p[11] = {3, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    return p;
}

uint8* getUnboundedGlyph() {
    static uint8 p[11] = {10, 11, 9, 2, 1, 3, 8, 7, 4, 5, 6};
    return p;
}

uint8* getKnowledgeGlyph() {
    static uint8 p[11] = {4, 11, 5, 6, 4, 0, 0, 0, 0, 0, 0};
    return p;
}

uint8* getIdeaGlyph() {
    static uint8 p[11] = {5, 3, 10, 8, 6, 4, 2, 9, 7, 0, 0};
    return p;
}
