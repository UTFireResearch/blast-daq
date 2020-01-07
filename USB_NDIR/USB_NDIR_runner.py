import serial
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from o2_helper import GetO2Voltage
import numpy as np
import socket

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.readline()
ser.readline()

THINGSBOARD_HOST = '192.168.0.199'
ACCESS_TOKEN = socket.gethostname()
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

def XaXfXp(XO2,XCO2, XCH4):
    T = np.array([[0.209, 0, 0],
                  [0,0.319,0.214],
                  [0,1.897,0]])
    X = np.array([XO2,XCO2,XCH4])
    return np.linalg.solve(T,X)


def ReadUSBData():
    LINE = str(ser.readline())
    data_arr = LINE.split(' ')
    dv = {}
    dv['TimeNow'] = datetime.now().isoformat()
    dv['PkPkRef'] = float.fromhex(data_arr[2])/(65536.0/3.0)
    dv['PkPk1'] = float.fromhex(data_arr[3])/(65536.0/3.0)
    dv['PkPk2'] = float.fromhex(data_arr[4])/(65536.0/3.0)
    dv['CH4'] = float(data_arr[5])*100/1000000
    dv['CO2'] = float(data_arr[6])*100/1000000
    dv['Temperature'] = float(data_arr[7])
    dv['O2'], dv['O2Voltage'] = GetO2Voltage()
    dv['Xa'], dv['Xf'], dv['Xp'] = XaXfXp(dv['O2'],dv['CO2'], dv['CH4'])
    return dv

def do_loop():
    y=0
    while True:
        y+=1
        dv = ReadUSBData()
        dv['y']=y
        client.publish('v1/devices/me/telemetry', json.dumps(dv), 1)
        outt = '%s, %5.4f, %5.4f, %5.4f, %5.4f, ' % (dv['TimeNow'], dv['PkPkRef'], dv['PkPk1'], dv['PkPk2'], -1)
        outt = outt + '%5.2f, %5.3f, %5.3f, %5.3f, %5.3f, %5.5f\n' % (dv['Temperature'], -1, dv['CO2'], dv['CH4'], dv['O2'], dv['O2Voltage'])
        myfile = open('data/NDIRJupiterEV_' + datetime.now().isoformat()[0:13] +'.csv','a')
        myfile.write(outt)
        myfile.close()
        print(y, " Time: CO2: %5.1f  CH4: %5.1f O2: %5.1f PkPkRef: %5.3f PkPkCO2: %5.3f PkPkCH4: %5.3f " % (dv['CO2'], dv['CH4'], dv['O2'], dv['PkPkRef'], dv['PkPk1'], dv['PkPk2'])) 

do_loop()
