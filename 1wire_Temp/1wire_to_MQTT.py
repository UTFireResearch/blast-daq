from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt
import json
import socket

THINGSBOARD_HOST = '192.168.0.199'
ACCESS_TOKEN = socket.gethostname() + '-TC'
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()


sensors = []
for sensor in W1ThermSensor.get_available_sensors():
    if sensor.get_temperature() < 2000:
        sensors.append(sensor)
    

while True:
    dv = {}
    for sensor in sensors:
        dv['TC-' + sensor.id[-2::]] = sensor.get_temperature()
    print(dv)
    client.publish('v1/devices/me/telemetry', json.dumps(dv), 1)
