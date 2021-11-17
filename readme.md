# OpenHub

An opensource homekit iOT hub. This project is built on [HAP-Python](https://github.com/ikalchev/HAP-python). 

Main features:

* Customizable
* Manage many iOT hubs from one location
* Integrated with the home automation framework [Home Assistant](https://github.com/home-assistant/home-assistant).
* Integrates with HomeKit and Siri

Sensors:
* Air Temperature
* Soil Temperature
* AC Current
* Liquid Level
* Soil Moisture
* Air Humidity
* Water Pressure
* Air Quality
* Light

Includes code for hardware:
* DHT22
* DS18B20
* VEML7700
* PMSA0013
* MCP3008
* PiPico (requires OpenHubController)

## Installation 


```
$ sudo apt-get install python3-pip
$ sudo python3 pip -m install openhub
$ sudo python3 pip -m OpenHub.install
```

## Home Assistant Integration 

<img width="1381" alt="garden_hub_home_assistant" src="https://user-images.githubusercontent.com/3904428/142282799-40c58ffb-13dd-4115-ba77-7052f0199957.png">

## Example Hub

![soil_moisture_temp_humidity](https://user-images.githubusercontent.com/3904428/142282859-fffbcc82-ac24-4a6b-afc1-daf44ad1abfe.jpg)
