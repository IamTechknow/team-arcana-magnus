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

//Not live until we get all 11 detectors working
/*
uint8* getSearchGlyph() {
    static uint8 p[11] = {};
    return p;
}

uint8* getAnswerGlyph() {
    static uint8 p[11] = {};
    return p;
}

uint8* getGainGlyph() {
    static uint8 p[11] = {};
    return p;
}

uint8* getUnboundedGlyph() {
    static uint8 p[11] = {};
    return p;
}

uint8* getKnowledgeGlyph() {
    static uint8 p[11] = {};
    return p;
}

uint8* getIdeaGlyph() {
    static uint8 p[11] = {};
    return p;
}
*/
