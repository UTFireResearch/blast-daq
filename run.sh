#!/bin/bash
vncserver :1 -geometry 1920x1080 > /tmp/vnc.log 2>&1 &
sleep 60
echo hello > /tmp/h.log
# Now we enter our normal code here. The above was just for online checking
echo 'Running'
cd /home/pi/blast-daq && git pull > /tmp/git.log 2>&1
cd /home/pi/blast-daq/USB_NDIR 
python3 /home/pi/blast-daq/USB_NDIR/USB_NDIR_runner.py > /tmp/ndir.log 2>&1 &
cd /home/pi/blast-daq/1wire_Temp 
python3 1wire_to_MQTT.py > /tmp/temp.log 2>&1 &

