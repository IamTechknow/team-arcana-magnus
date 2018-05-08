#ifndef _GLYPH_H_
#define _GLYPH_H_

#include "project.h"
#define NUM_GLYPHS 1
#define NUM_NODES 11

//Functions that return glyphs
uint8* getBodyGlyph();

uint8* getUseGlyph(); //Check

uint8* getWrongGlyph(); //Not an actual glyph, just an X

uint8 checkGlyph(uint8* left, uint8* right);

//Not live until we get all 11 detectors working
/*
uint8* getSearchGlyph();

uint8* getAnswerGlyph();

uint8* getGainGlyph();

uint8* getUnboundedGlyph();

uint8* getKnowledgeGlyph();

uint8* getIdeaGlyph();
*/

#endif
