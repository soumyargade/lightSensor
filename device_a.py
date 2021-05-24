import RPi.GPIO as GPIO
import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#from device_a_test import count
#print(count)

GPIO.setmode(GPIO.BCM)
pin_to_circuit = 4
 
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
 
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
 
# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

def rc_time(pin_to_circuit):
    count = 0
    
    # output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    # every 100 milliseconds
    time.sleep(0.1)
    
    # change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
    
    # count until the pin goes too high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    
    return count

def main():
    client = mqtt.Client()
    host = "98.121.22.98"
    port = 1883
    
    # lastwill message as retained message, topic: Status/RaspberryPiA, content: offline
    client.will_set("Status/RaspberryPiA", "offline", retain=True)
    
    client.connect(host, port, 5)
    
    client.publish("Status/RaspberryPiA", "online", retain=True)
    client.subscribe("lightStatus")
    client.subscribe("threshold")
    
    last_chan_val = 0
    new_value = 0
    min_ldr_val = 200000
    max_ldr_val = 2500000
    min_pot_val = 0
    max_pot_val = 65500
    
    while True:
        count = rc_time(pin_to_circuit)
        count = round((count-min_ldr_val)/(max_ldr_val-min_ldr_val), 3)
        #print(count)
        new_value = round((chan.value-min_pot_val)/(max_pot_val-min_pot_val), 3)
        #print('Raw ADC Value: ', new_value)
        #print('ADC Voltage: ' + str(chan.voltage) + 'V')
        time.sleep(0.1)
        client.publish("lightSensor", count, retain=True)
        if (last_chan_val != new_value):
            last_chan_val = new_value
            client.publish("threshold", new_value, retain=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()