#ifndef _GLYPH_H_
#define _GLYPH_H_

#include "project.h"

//Functions that return glyphs
uint8* getBodyGlyph();

uint8* getUseGlyph(); //Check

uint8* getWrongGlyph(); //Not an actual glyph, just an X

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
