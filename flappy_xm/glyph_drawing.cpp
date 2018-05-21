#include <utility>

using namespace std;

//One-to-one correspondence with glyphs and their lengths on the matrix
static const int GLYPH_LENGTHS[8] = {9, 5, 5, 5, 7, 7, 8, 9};

//Array of coordinates to draw glyphs in Row-Major form.
//They start at 0 and can be offset to be draw in both matrices.
static const vector<pair<int, int>> knowledge = {
    //Knowledge, 12 pixels, uses 8x8 space
    make_pair(0, 0),
    make_pair(0, 8),
    make_pair(1, 2),
    make_pair(1, 6),
    make_pair(2, 1),
    make_pair(2, 4),
    make_pair(2, 7),
    make_pair(4, 2),
    make_pair(4, 6),
    make_pair(6, 3),
    make_pair(6, 5),
    make_pair(8, 4)
};

static const vector<pair<int, int>> idea = {
    //Idea, 26 pixels, uses 8x15 space
    make_pair(0, 0),
    make_pair(0, 14),
    make_pair(1, 0),
    make_pair(1, 2),
    make_pair(1, 12),
    make_pair(1, 14),
    make_pair(2, 0),
    make_pair(2, 4),
    make_pair(2, 10),
    make_pair(2, 14),
    make_pair(3, 0),
    make_pair(3, 6),
    make_pair(3, 14),
    make_pair(4, 0),
    make_pair(4, 8),
    make_pair(4, 14),
    make_pair(5, 0),
    make_pair(5, 4),
    make_pair(5, 10),
    make_pair(5, 14),
    make_pair(6, 0),
    make_pair(6, 2),
    make_pair(6, 12),
    make_pair(6, 14),
    make_pair(7, 0),
    make_pair(7, 14)
};

//Glyphs used as obstacles
static const vector<pair<int, int>> breathe = {
    make_pair(0, 0),
	make_pair(1, 2),
	make_pair(2, 4),
	make_pair(1, 6),
	make_pair(0, 8)
};

static const vector<pair<int, int>> easy = {
	make_pair(0, 4),
	make_pair(1, 2),
	make_pair(2, 0),
	make_pair(4, 1),
	make_pair(6, 2)
};

static const vector<pair<int, int>> soul = {
	make_pair(1, 0),
	make_pair(2, 0),
	make_pair(3, 0),
	make_pair(4, 0),
	make_pair(0, 2),
	make_pair(2, 2),
	make_pair(3, 1)
};

static const vector<pair<int, int>> gain = {
	make_pair(0, 0),
	make_pair(1, 1),
	make_pair(2, 2),
	make_pair(3, 3)
};

static const vector<pair<int, int>> create = {
	make_pair(6, 0),
	make_pair(5, 1),
	make_pair(4, 2),
	make_pair(3, 3),
	make_pair(2, 4),
	make_pair(1, 5),
	make_pair(0, 6)
};

static const vector<pair<int, int>> mystery = {
	make_pair(1, 0),
	make_pair(2, 2),
	make_pair(2, 3),
	make_pair(2, 4),
	make_pair(2, 5),
	make_pair(2, 6),
	make_pair(1, 5),
	make_pair(0, 4),
	make_pair(1, 3),
	make_pair(3, 2),
	make_pair(4, 2)
};

static const vector<pair<int, int>> civil = {
	make_pair(0, 0),
	make_pair(1, 2),
	make_pair(2, 2),
	make_pair(3, 2),
	make_pair(3, 3),
	make_pair(3, 4),
	make_pair(3, 5),
	make_pair(2, 5),
	make_pair(1, 5),
	make_pair(0, 7)
};

static const vector<pair<int, int>> war = {
	make_pair(4, 0),
	make_pair(3, 1),
	make_pair(2, 2),
	make_pair(1, 3),
	make_pair(0, 4),
	make_pair(1, 5),
	make_pair(2, 6),
	make_pair(3, 7),
	make_pair(4, 8)
};
