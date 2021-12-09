#!/usr/bin/env python3
import paho.mqtt.client as mqtt # This is the Subscriber
from influxdb import InfluxDBClient
import time, json
from flask import request, Flask
from datetime import datetime
import flask
app = flask.Flask(__name__)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client_mqtt.subscribe("topic/test")
    
def on_message(client_mqtt, userdata, msg):
    obj = json.loads(msg.payload.decode().replace("'","\""))
    #client.disconnect()
    json_body = [{
            'measurement':'env1',
            'tags':{'env':'true'},
            'time':datetime.now(),
            'fields':{
                'temperature' : round(float(obj['temperature']),2),
                'humidity': round(float(obj['humidity']),2) ,
                'brightness': round(float(obj['brightness']),2),
                'pressure': round(float(obj['pressure']),2),
                }}]
    #print(json_body) #wring this to db
    print(client_influx.write_points(json_body)) #True: if written succesfully
    #print(client_influx.write(json_body))
    #result = client_influx.query('select * from env1 order by time desc LIMIT 1') # retrieving last entered query
    #print(result)
                  
@app.route('/get-last')
def get_last():
    print("In get last request ")
    result = client_influx.query('select * from env1 order by time desc LIMIT 1') # retrieving last entered query
    #print (result)
    cpu_points = list(result.get_points())
    #print(cpu_points)
    #print(type(result))
    response = flask.jsonify(cpu_points[0])
    response.headers.add('Access-Control-Allow-Origin', '*')

    #delete this later
    #client_mqtt_post = mqtt.Client()
    #client_mqtt_post.connect('public.mqttq.com', 1883, 60)
    #client_mqtt_post.publish('topic/test',  'example')
    #client_mqtt_post.disconnect()    
 

    return response
    #return str(cpu_points[0])

@app.route('/update', methods=['GET'])
def update():
    #values = request.form['data']
    #temp = values['temperature']
    client_mqtt_post = mqtt.Client()
    client_mqtt_post.connect('public.mqttq.com', 1883, 60)
    client_mqtt_post.publish('topic/test',  'example')
    client_mqtt_post.disconnect()    
    return True #redirect(url_for('success',name = user))


if __name__ == '__main__':
    print('Trying connecting mqtt')
    client_mqtt = mqtt.Client()
    client_mqtt.connect('public.mqtthq.com',1883,60)
    client_mqtt.on_connect = on_connect
    client_mqtt.on_message = on_message
    #client_mqtt.loop_forever() # will be stuck here wit main loop
    client_mqtt.loop_start() #keeps one thred here and functions ahead with main thread
    #print('Error connecting to mqtt')
    print('Trying connecting influxDB')
    client_influx = InfluxDBClient(host='localhost', port=8086)
    print(client_influx.get_list_database())
    client_influx.switch_database('weather')
    #client_influx = InfluxDBClient(host='cc_weatherapp', port=8086, username='myuser', password='mypass', ssl=True, verify_ssl=True)
    #print('Error connecting influxDB')
 
    app.run(host="0.0.0.0", use_reloader=False, debug = True, port = 5000)
    #while(True):# to keep theread from ending can use daemon later
    #time.sleep(1)

