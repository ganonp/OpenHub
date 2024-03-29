# Updates!

For the light trickle of people I've seen cloning and visiting. I'm presently at the end of a big house move and still in the throes of starting a new job. However, in a few months updates to this and adjacent repos will resume (although at a slower pace). If you are interested in contributing, please feel free to let me know, open an issue, make a PR and I will do my best to get back to you.

# OpenHub

An open source iOT hub for the HomeKit framework. Works with [OpenHubAPI](https://github.com/ganonp/OpenHubAPI) and [OpenController](https://github.com/ganonp/OpenController). This project is built on [HAP-Python](https://github.com/ikalchev/HAP-python). 

Main features:

* Customizable
* Managed through a GUI via [OpenHubAPI](https://github.com/ganonp/OpenHubAPI)
* Works with the home automation framework [Home Assistant](https://github.com/home-assistant/home-assistant).
* Works with HomeKit and Siri
* Camera works with Raspberry Pi Zero (and more powerful pis) + PiCam

Accessories For:
* Air Temperature
* Soil Temperature
* AC Current
* Liquid Level
* Soil Moisture
* Air Humidity
* Water Pressure
* Air Quality
* Light
* Relays
* Pumps
* Valves
* Camera

Includes code for hardware:
* DHT22
* DS18B20
* VEML7700
* PMSA0013
* MCP3008
* PiCam
* PiPico (requires [OpenController](https://github.com/ganonp/OpenController))

## Installation 

On a Raspberry Pi with a clean version of Raspbian Buster run:
```
$ sudo apt-get update
$ sudo apt-get install python3-pip --fix-missing -y
$ sudo python3 -m pip install openhub
$ sudo python3 -m OpenHub.install
```
When prompted, enter a name for the hub (this will make it easier to find from the OpenHubAPI GUI) and press enter.
Please reboot when prompted.

## Home Assistant Integration 

<img width="1381" alt="garden_hub_home_assistant" src="https://user-images.githubusercontent.com/3904428/142282799-40c58ffb-13dd-4115-ba77-7052f0199957.png">

## Example Hub

![soil_moisture_temp_humidity](https://user-images.githubusercontent.com/3904428/142282859-fffbcc82-ac24-4a6b-afc1-daf44ad1abfe.jpg)
