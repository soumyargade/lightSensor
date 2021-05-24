import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import signal

lightSensor = 0.0
lightSensor_changed = False
threshold = 0.0
# False == light is off
# True == light is on
status = False

client = mqtt.Client()

def signal_handler(signal, frame):
    print("Disconnecting!")
    client.publish("Status/RaspberryPiC", "offline", qos=2, retain=True)
    client.disconnect()
    sys.exit(0)

def on_connect(client, userdata, flags, rc):
    print("Connected with code " + str(rc))
    client.publish("Status/RaspberryPiC", "online", qos=2, retain=True)
    client.subscribe("dev/test")
    client.subscribe("lightsensor")
    client.subscribe("threshold")

def on_message(client, userdata, msg):
    global status, lightSensor, threshold
    print("RECEIVED: " + msg.topic + " " + str(msg.payload))
    # Hold the status before the computation to see if it changed
    last_status = status

    if (msg.topic == "lightsensor"):
        lightSensor = float(msg.payload)
        print(f"Changed light sensor value to: {lightSensor}")
    elif (msg.topic == "threshold"):
        threshold = float(msg.payload)
        print(f"Changed threshold value to: {threshold}")
    elif (msg.topic == "dev/test"):
        print(f"debug: {msg.payload}")

    # Compute new light status
    status = lightSensor >= threshold
    if (status != last_status):
        payload = ""
        if (status):
            payload = "TurnOn"
        else:
            payload = "TurnOff"
        print(f"Changing light status to {payload}")
        client.publish("LightStatus", payload, retain=False)

client.on_connect = on_connect
client.on_message = on_message

host = "98.121.22.98"
port = 1883
client.will_set("Status/RaspberryPiC", "offline", qos=2, retain=True)
client.connect(host, port, 5)
signal.signal(signal.SIGINT, signal_handler)

client.loop_forever()
