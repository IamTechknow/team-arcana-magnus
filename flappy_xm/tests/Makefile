CFLAGS= -Wall -O1 -g -Wextra -Wno-unused-parameter -pthread
BINS=mqtt_c_test btn_test

all : $(BINS)

btn_test : btn_test.c
	$(CC) $(CFLAGS) $< -o $@ -lpigpio -lrt

mqtt_c_test : mqtt_c_test.c
	$(CC) $(CFLAGS) $< -o $@ -lpaho-mqtt3c

clean:
	rm -f $(BINS)
