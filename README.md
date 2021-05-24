# Light Sensor
CSC 453 HW 1
### Device A Readme
Author: Soumya Gade, Raspberry Pi A
* Device A samples LDR and potentiometer values every 100 ms. It publishes these to the broker after normalizing the raw values to be between 0 and 1. Device A subscribes to lightSensor and threshold upon connecting to the broker. On keyboard interrupt, Device A will perform GPIO cleanup & exit.
* **Prerequisites & Dependencies**: Raspberry Pi set up as described in the Raspberry Pi A Schematics Diagram, Python 3, Python installation of MCP3xxx Library, Paho MQTT client (install: pip install paho-mqtt). To run:

      python3 device_a.py
### Device B Readme
Author: Mason Rowland, Raspberry Pi B
* Device B code controls the activation of LEDs 1-3, in each specific case:
  * LED 1 will activate when the mqtt topic "LightStatus" receives message "TurnOn"
  * LED 1 will deactivate when the mqtt topic "LightStatus" receives message "TurnOff"
  * LED 2 will activate when the mqtt topic "Status/RaspberryPiA" receives message "online"
  * LED 2 will deactivate when the mqtt topic "Status/RaspberryPiA" receives message "offline"
  * LED 3 will activate when the mqtt topic "Status/RaspberryPiC" receives message "online"
  * LED 3 will deactivate when the mqtt topic "Status/RaspberryPiC" receives message "offline"
* Device B subscribes to all three of these topics upon connecting to the broker. On Keyboard Interrupt, Device B will turn off all LEDs, perform GPIO cleanup, and exit.
* **Prerequisites & Dependencies**: Raspberry Pi set up as described in the Raspberry Pi B Schematics Diagram, Python 3, Paho MQTT client (install: pip install paho-mqtt). To run:

      python3 device_b.py
