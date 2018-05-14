from django.shortcuts import render
from django.contrib import messages

from paho.mqtt import publish, MQTTException

MQTT_BROKER = 'localhost'
FACTION_CHANGED = 'portal/factionChange'
LEVEL_CHANGED = 'portal/levelChange'
PORTAL_DAMAGED = 'portal/portalDamaged'
PORTAL_RECHARGED = 'portal/portalRecharged'
PORTAL_OFF = 'portal/lightsOff'

NEUTRAL = 0
ENL = 1
RES = 2

# Create your views here.
def index(request):
    #Parse GET request, publish events
    faction = request.GET.get('faction')
    level = request.GET.get('level')
    health = request.GET.get('health')
    turn_off = request.GET.get('off')

    switch_neutral = False

    #Send one or more MQTT events!
    events = []
    if faction != None:
        events.append( (FACTION_CHANGED, int(faction)) )
        messages.success(request, 'Faction changed to ' + getFaction(int(faction)))
        switch_neutral = int(faction) == NEUTRAL
        if not switch_neutral and level == None: #pressed a change faction button
            level = '1';

    if level != None:
        switch_neutral = int(level) == 0

    #Always send same result for neutralized portals
    if turn_off != None:
        events.append( (PORTAL_OFF, 0) )
    elif switch_neutral:
        events.append( (LEVEL_CHANGED, 0) )
        events.append( (PORTAL_DAMAGED, 0) )
        messages.success(request, 'Portal status changed to neutral')
    else:
        if level != None:
            events.append( (LEVEL_CHANGED, int(level)) )
            messages.success(request, 'Level changed to ' + level)

        if health != None:
            events.append( (PORTAL_RECHARGED if int(health) == 100 else PORTAL_DAMAGED, int(health)) )
            messages.success(request, 'Portal health changed to ' + health)

    try:
        if len(events) != 0:
            publish.multiple(events, hostname=MQTT_BROKER, port=1883)
    except MQTTException as e:
        print("Could not publish events: " + e)

    return render(request, 'tecthulhu_ctrl/index.html')

def getFaction(num):
    if num == 0:
        return 'Neutral'
    elif num == 1:
        return 'Enlightened'
    else:
        return 'Resistance'
