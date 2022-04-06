import serial
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import numpy as np
import socket

#Setup serial port.  For more info lookup pyserial help
ser = serial.Serial('/dev/ttyUSB0', 9600)    #TODO Add serial port settings here depending on the device that you're communicating with
ser.readline() #Reads a line from the serial port
ser.readline() #Reads a line from the serial port

#Setup connection to thingsboard IOT server, if this doesn't work just continue on.
connected = False
try:
  THINGSBOARD_HOST = '192.168.0.200'
  ACCESS_TOKEN = socket.gethostname()
  client = mqtt.Client()
  client.username_pw_set(ACCESS_TOKEN)
  client.connect(THINGSBOARD_HOST, 1883, 60)
  client.loop_start()
  connected = True
except:
  print('Connection failed, data will be saved locally')
 

def ReadSerialData():
    LINE = str(ser.readline())                                            #Read data from serial port
    data_arr = LINE.split(' ')                                            #Separate the data into an array assuming there are blank spaces between data points  
    dv = {}                                                               #This is a dictionary that stores the data that we're interested in.
    dv['TimeNow'] = datetime.now().isoformat()                            #Capture current time
    dv['PkPkRef'] = float.fromhex(data_arr[2])              #Save float value into dictionary for data value in position 2 of the rec'd data string

    return dv

def do_loop():
    y=0
    while True:
        y+=1
        dv = ReadSerialData()
        dv['y']=y
        if connected:                                                       #If IOT connection worked
          client.publish('v1/devices/me/telemetry', json.dumps(dv), 1)      #Send data to thingsboard
        outt = '%s, %5.4f, %5.4f, %5.4f, %5.4f, ' % (dv['TimeNow'], dv['PkPkRef'], dv['PkPk1'], dv['PkPk2'], -1)
        outt = outt + '%5.2f, %5.3f, %5.3f, %5.3f, %5.3f, %5.5f\n' % (dv['Temperature'], -1, dv['CO2'], dv['CH4'], dv['O2'], dv['O2Voltage'])
        myfile = open('data/MySerialDevice1_' + datetime.now().isoformat()[0:13] +'.csv','a')
        myfile.write(outt)
        myfile.close()
        print(y, " Time: CO2: %5.1f  CH4: %5.1f O2: %5.1f PkPkRef: %5.3f PkPkCO2: %5.3f PkPkCH4: %5.3f " % (dv['CO2'], dv['CH4'], dv['O2'], dv['PkPkRef'], dv['PkPk1'], dv['PkPk2'])) 

do_loop()
