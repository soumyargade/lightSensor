import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

global lastStatus
#occurs when I connect to the broker
def on_connect(client, userdata, flags, rc):
    global lastStatus
    client.subscribe("LightStatus")
    client.subscribe("Status/RaspberryPiA")
    client.subscribe("Status/RaspberryPiC")
    lastStatus = ""
    
    #just in case lights are left on from previous
    GPIO.output(12,False)
    GPIO.output(16,False)
    GPIO.output(18,False)
    
    
#occurs whenever a message is posted to any subscribed topic
def on_message(client,userdata,msg):
    global lastStatus
    topic = msg.topic.encode("ascii")
    message = msg.payload.encode("ascii")
    
    if topic == "LightStatus":
        lastStatus = message
        if message =="TurnOff":
            GPIO.output(12,False) #LED1 OFF
        if message == "TurnOn":
            GPIO.output(12,True) #LED1 ON
    
    if topic == "Status/RaspberryPiA":
        if message == "online":
            GPIO.output(16,True) #LED2 ON
        if message == "offline":
            GPIO.output(16,False) #LED2 OFF
            
    if topic == "Status/RaspberryPiC":
        if message == "online":
            GPIO.output(18,True) #LED3 ON
            if lastStatus == "TurnOff":
                GPIO.output(12,False) #LED1 OFF
            if lastStatus == "TurnOn":
                GPIO.output(12,True) #LED1 ON
        if message == "offline":
            GPIO.output(18,False) #LED3 OFF
            GPIO.output(12,False) #LED1 OFF
            
#set up the client and GPIO systems then loop on connect
def main():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message=on_message

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) #or GPIO.BCM for pin function codes instead of pin #


    #setup(PinNo,Direction)
    GPIO.setup(12,GPIO.OUT) #LED1
    GPIO.setup(16,GPIO.OUT) #LED2
    GPIO.setup(18,GPIO.OUT) #LED3
    host = "98.121.22.98"
    port = 1883
    client.connect(host, port, 10)
    client.loop_forever()
    
#Handles keyboard interrupt to reset lights
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.output(12,False)
        GPIO.output(16,False)
        GPIO.output(18,False)
        GPIO.cleanup()
        
