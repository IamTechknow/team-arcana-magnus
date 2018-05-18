CXXFLAGS=-Wall -O1 -g -std=c++11
OBJS=flappy_xm.o
BIN=flappy_xm

LED_LIB_NAME=rgbmatrix
LED_INCLUDE=led_matrix/include
LED_LIBRARY=led_matrix/lib$(LED_LIB_NAME).a
LED_LIB_DIR=led_matrix/lib

LDFLAGS+=-L$(LED_LIB_DIR) -lrt -lm -lpthread -lpigpio -lpaho-mqtt3c -l$(LED_LIB_NAME)

all : flappy_xm

flappy_xm : $(OBJS) $(LED_LIBRARY)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $@ $(LDFLAGS)

$(LED_LIBRARY):
	$(MAKE) -C $(LED_LIB_DIR)

flappy_xm.o : flappy_xm.cpp

%.o : %.cpp
	$(CXX) -I$(LED_INCLUDE) $(CXXFLAGS) -c -o $@ $<

clean :
	rm -f $(OBJS) $(BIN)
	$(MAKE) -C $(LED_LIB_DIR) clean
