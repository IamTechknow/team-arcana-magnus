from ola.ClientWrapper import ClientWrapper
import array
import paho.mqtt.client as mqtt
import subprocess32

"""Python 2 script to test operation of PAR lights with the DMX interface."""
"""Also controls playing sounds to a Bluetooth Speaker. Use the script to connect to it first."""
MQTT_BROKER = "localhost"

#Globals
wrapper = ClientWrapper()
client = wrapper.Client()

def DmxHandler(status):
    if status.Succeeded():
        print('Success!')
    else:
        print('Error: ' + status.message)

#Send DMX data to the PAR lights based on the MQTT payload
#Levels 0 and 8 are fade colors
def ctrlLightsByLevel(level):
    data = [[140, 100, 80] + [0] * 5, [11, 70, 192] + [0] * 5,
	[0, 120, 192, 255, 255, 0xA6, 0x30, 0], [0, 120, 192, 255, 255, 0x73, 0x15, 0],
	[11, 40, 64] + [0] * 5, [0, 120, 192, 255, 0xFD, 0x29, 0x92, 0],
	[0, 120, 192, 255, 0xEB, 0x26, 0xCD, 0], [0, 120, 192, 255, 0xC1, 0x24, 0xE0, 0], [140, 90, 80] + [0] * 5]
    arr = array.array('B', data[level] + [0] * 504)

    client.SendDmx(0, arr, DmxHandler)

def turnOffLights():
    client.SendDmx(0, array.array('B', [0] * 512), DmxHandler)

def playSound(level):
    if level == 0:
        subprocess32.run(["aplay", "sfx_explode_resonator.wav"])
    elif level == 8:
        subprocess32.run(["aplay", "sfx_resonator_power_up.wav"])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("portal/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == 'portal/levelChange':
        ctrlLightsByLevel(int(msg.payload))
        playSound(int(msg.payload))
    elif msg.topic == 'portal/lightsOff':
        turnOffLights()

#By having the OLA client be a global, we can have the MQTT client loop
if __name__ == '__main__':
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.connect(MQTT_BROKER, 1883, 60)
    try:
        mqttClient.loop_forever()
    finally:
        turnOffLights()
