#include <signal.h>
#include <unistd.h>
#include "MQTTClient.h"

#define BROKER "192.168.1.124:1883"
#define CLIENTID "FlappyClient"
#define TOPIC "portal/levelChange"
#define TIMEOUT 10000L
#define QOS 0

//Handle Ctrl-C to exit gracefully
volatile int int_received = 0;
static void InterruptHandler(int signo) {
	int_received = 1;
}

//Callback for message arrival
int msg_arrived(void *context, char *topicName, int topicLen, MQTTClient_message *message) {
	char *payload_ptr = message->payload;

	printf("Messaged arrived : %s\n", payload_ptr);
	MQTTClient_freeMessage(&message);
	MQTTClient_free(topicName);
	return 1;
}

void conn_lost(void *context, char *cause) {
	printf("Connection lost, cause: %s\n", cause);
}

int main(int argc, char* argv[]) {
	//Init MQTT
	MQTTClient client;
	MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;

	MQTTClient_create(&client, BROKER, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL);
	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;
	MQTTClient_setCallbacks(client, NULL, conn_lost, msg_arrived, NULL);

	//Attempt connection to the specified broker.
	int rc;
	if((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS) {
		printf("Failed to connect, code %d\n", rc);
		return 1;
	}
	MQTTClient_subscribe(client, TOPIC, QOS);

	signal(SIGTERM, InterruptHandler);
	signal(SIGINT, InterruptHandler);

	//Wait here, and also respond to new messages from the subscribed topic.
	while(!int_received);

	//De-init MQTT Client
	MQTTClient_disconnect(client, TIMEOUT);
	MQTTClient_destroy(&client);

	return 0;
}
