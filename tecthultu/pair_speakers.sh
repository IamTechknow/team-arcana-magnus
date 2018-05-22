#!/bin/bash
sudo hciconfig hci0 up
bluetoothctl << EOF
connect ED:33:CF:45:3D:DE
EOF
