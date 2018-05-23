import json
import requests
import time

from paho.mqtt import publish, MQTTException

#This scripts queries the Tecthulhu API and sends MQTT messages within the LAN.
#Note that the multicast DNS endpoint is not the same as the API from the module itself.
ENDPOINT = "http://patron.local:8080/v1/info"
TEST_ENDPOINT = "http://operation-wigwam.ingress.com:8080/v1/test-info"
MQTT_BROKER = "localhost"
FACTION = "controllingFaction"

NEUTRAL = "Neutral"
ENL = "Enlightened"
RES = "Resistance"

NEUT_NUM = 0
ENL_NUM = 1
RES_NUM = 2

def getFactionNum(faction):
    if faction == NEUTRAL:
        return NEUT_NUM
    elif faction == ENL:
        return ENL_NUM
    else:
        return RES_NUM

#Publish events to the MQTT Broker
def publishEvents(events):
    num_events = len(events)
    print("Sending {} events".format(num_events))
    try:
        if num_events > 0:
            for e in events:
                print(str(e))

            publish.multiple(events, hostname=MQTT_BROKER, port=1883)
    except MQTTException as e:
        print("Could not publish events: " + str(e))

#Compute changes to the portal since the last state
#If no previous states, send events to init other subsystems
def computeEvents(prev_state, state):
    events = []

    #Check faction
    if not prev_state or prev_state[FACTION] != state[FACTION]:
        events.append( ('portal/factionChange', getFactionNum(state[FACTION])) )

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
        while True:
            #Query endpoint, parse JSON to dict
            r = requests.get(TEST_ENDPOINT)
            status = r.json()
            print("Response code: {}".format(status['code']))

            if 'result' in status:
                state = status['result']
                events = computeEvents(prev_state, state)
                publishEvents(events)
                prev_state = state

            time.sleep(1)

    except requests.RequestException as e:
        print("Could not fetch portal status: " + str(e))
