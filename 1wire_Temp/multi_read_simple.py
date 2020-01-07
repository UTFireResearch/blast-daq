from w1thermsensor import W1ThermSensor
ss = []
for sensor in W1ThermSensor.get_available_sensors():
    ss.append(sensor)
    print("Sensor %s has temperature %.2f " % (sensor.id, sensor.get_temperature()))   
