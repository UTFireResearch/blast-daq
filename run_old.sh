#!/bin/bash

function check_online
{
    netcat -z -w 5 8.8.8.8 53 && echo 1 || echo 0
}

# Initial check to see if we are online
IS_ONLINE=check_online
# How many times we should check if we're online - this prevents infinite looping
MAX_CHECKS=5
# Initial starting value for checks
CHECKS=0

# Loop while we're not online.
while [ $IS_ONLINE = 0 ]; do
    # We're offline. Sleep for a bit, then check again
    echo 'Offline, sleeping'
    sleep 10;
    IS_ONLINE=check_online

    CHECKS=$[ $CHECKS + 1 ]
    if [ $CHECKS -gt $MAX_CHECKS ]; then
        break
    fi
done

if [ $IS_ONLINE = 0 ]; then
    # We never were able to get online. Kill script.
	echo 'Not online'
	cd /home/pi/blast-daq/USB-NDIR && python3 /home/pi/blast-daq/USB-NDIR/USB_NDIR_runner.p$
	cd /home/pi/blast-daq/1wire_to_MQTT &&  python3 /home/pi/blast-daq/1wire_to_MQTT.py  > $
	vncserver :1 -geometry 1920x1080 > /tmp/vnc.log 2>&1 &
    exit 1
fi

# Now we enter our normal code here. The above was just for online checking
echo 'We are online'
cd /home/pi/blast-daq && git pull > /tmp/git.log 2>&1
cd /home/pi/blast-daq/USB_NDIR 
python3 /home/pi/blast-daq/USB_NDIR/USB_NDIR_runner.py > /tmp/ndir.log 2>&1 &
cd /home/pi/blast-daq/1wire_Temp 
python3 1wire_to_MQTT.py > /tmp/temp.log 2>&1 &
vncserver :1 -geometry 1920x1080 > /tmp/vnc.log 2>&1 &
