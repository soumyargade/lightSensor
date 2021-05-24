import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

#occurs when I connect to the broker
def on_connect(client, userdata, flags, rc):
    client.subscribe("lightSensor", qos=2)
    client.subscribe("threshold", qos=2)
    client.subscribe("LightStatus", qos=2)
    client.subscribe("Status/RaspberryPiA", qos=2)
    client.subscribe("Status/RaspberryPiC", qos=2)

#occurs whenever a message is posted to any subscribed topic
def on_message(client, userdata, msg):
    ct = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(ct + ": " + str(msg.topic) + " " + str(msg.payload))
    
#start of main code block            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# dynamic address could change
host = "98.121.22.98"
port = 1883 #does this port work the same within the LAN?
client.connect(host, port, 60)
client.loop_forever()
