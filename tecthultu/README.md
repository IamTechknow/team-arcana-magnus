# Tecthultu Integration

## Introduction
A central device serves as the subscriber for the Techultu API and the publisher of MQTT events for all other microcontrollers that support the MQTT protocol. This device will also control the lighting system. In case of broken WiFi, a secondary interface may be used to control the PLP itself.

## Minimum Specification
* A router is used to establish a local WLAN of which all puzzle and art devices shall be connected to
* This device should be fast, the best candidate for this is the Raspberry Pi 3
* This device shall query the Techultu API, parse the data, and publish events that indicate changes to the portal in real-time.
* Hosts the MQTT broker, and publishes to the “level” topic with the level as the payload, or to the “faction” topic with 0 or 1 as the payload to indicate RES/ENL control
* Is connected to a USB DMX interface that can control PAR lights when the portal level changes
* Hosts a website that may be used to control the PLP. They may be done with django and endpoints may be used to publish MQTT events

## Materials
* Raspberry Pi 3 Model B (not the new B+)
* [USB DMX Interface](https://www.amazon.com/gp/product/B00T8OKM98/)
* [PAR Lights](https://www.amazon.com/gp/product/B012IDO3VS/) and XLR cables
* Portable Router, we are using the TP-Link MR3040

## MQTT Events
| Action           | Topic                  |
| ---------------- |------------------------|
| Faction Change   | portal/factionChange   |
| Level Change     | portal/levelChange     |
| Portal Damaged   | portal/portalDamaged   |
| Portal Recharged | portal/portalRecharged |

## Setup Information
Uses a Raspberry Pi 3 Model B with Stretch Lite, 16 GB microSD card
Packages installed for Mosquitto and Python: git libwrap0-dev libssl-dev libc-ares-dev uuid-dev xsltproc mosquitto-clients libmosquitto1 libmosquittopp1 python-pip python3-pip python3-gi python-dev python3-dev autoconf libtool ola ola-python (Only for 2.7)
Python modules: django paho-mqtt protobuf
