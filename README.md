# Light Sensor
CSC 453 HW 1
### Device A Readme
Author: Soumya Gade, Raspberry Pi A
* Device A samples LDR and potentiometer values every 100 ms. It publishes these to the broker after normalizing the raw values to be between 0 and 1. Device A subscribes to lightSensor and threshold upon connecting to the broker. On keyboard interrupt, Device A will perform GPIO cleanup & exit.
* **Prerequisites & Dependencies**: Raspberry Pi set up as described in the Raspberry Pi A Schematics Diagram, Python 3, Python installation of MCP3xxx Library, Paho MQTT client (install: pip install paho-mqtt). In order to run:

      python3 device_a.py
### Device B Readme
