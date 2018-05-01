import json
import requests
import time

from paho.mqtt import publish, MQTTException

#This scripts queries the Tecthulhu API and sends MQTT messages within the LAN.

ENDPOINT = "https://testthulu.firebaseio.com/.json"
MQTT_BROKER = "localhost"
FACTION = "controllingFaction"

NEUTRAL = 0
ENL = 1
RES = 2

#Publish events to the MQTT Broker
def publishEvents(events):
    try:
        publish.multiple(events, hostname=MQTT_BROKER, port=1883)
    except MQTTException as e:
        print("Could not publish events: " + e)

#Compute changes to the portal since the last state
#If no previous states, send events to init other subsystems
def computeEvents(prev_state, state):
    events = []

    #Check faction
    if not prev_state or prev_state[FACTION] != state[FACTION]:
        events.append( ('portal/factionChange', state[FACTION]) )

    #Check level
    if not prev_state or prev_state['level'] != state['level']:
        events.append( ('portal/levelChange', state['level']) )

    #Check health
    if prev_state and prev_state['health'] > state['health']:
        events.append( ('portal/portalDamaged', state['health']) )
    if not prev_state or prev_state['health'] < state['health']:
        events.append( ('portal/portalRecharged', state['health']) )

    return events

if __name__ == "__main__":
    prev_state = None

    try:
        #Query endpoint, parse JSON to dict
        r = requests.get(ENDPOINT)
        status = r.json()

        if 'status' in status:
            state = status['status']
            events = computeEvents(prev_state, state)
            publishEvents(events)
            prev_state = state

        time.sleep(1)

    except requests.RequestException as e:
        print("Could not fetch portal status: " + e)
