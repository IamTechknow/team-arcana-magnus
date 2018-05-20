#include <utility>

using namespace std;

//Array of coordinates to draw the Knowledge and Idea glyph.
//They start at 0 and can be offset to be draw in both matrices.
static const pair<int, int> arr[38] = {
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
    make_pair(8, 4),
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
    make_pair(7, 14),
};
