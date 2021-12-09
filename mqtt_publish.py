#!/usr/bin/env python3
#source7il.
#https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/

import paho.mqtt.client as mqtt
import time
from random import randrange, uniform

# This is the Publisher

client = mqtt.Client()
client.connect('public.mqtthq.com',1883,60)

while True:
    randNumberTemp = uniform(15.0, 24.0)
    randNumberHumidity = uniform(60.0, 100.0)
    randNumberPressure = uniform(20.0, 21.0)
    randNumberBrightness = uniform(0.0, 15.0)
    data = {
        "temperature" : randNumberTemp,
                "humidity": randNumberHumidity,
                "brightness": randNumberBrightness,
                "pressure": randNumberPressure
    }
    # client.publish("TEMPERATURE112", randNumberTemp)
    # print("Sending msg: ")
    client.publish("topic/test", str(data))
    print("Just published " + str(data) )
    time.sleep(1)

client.disconnect()
