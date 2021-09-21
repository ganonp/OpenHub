Pi Zero W Setup

Download Raspberry Pi Imager
Use to download and flash Raspberry Pi OS Lite to the micro sd card

Add file named ```.ssh``` to base directory of card.

Connect wifi by adding a file named ```wpa_supplicant.conf``` to the same location.

wpa_supplicant.conf:

```country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid=<WIFI_NETWORK_NAME_
scan_ssid=1
psk=<WIFI_PASSWORD>
key_mgmt=WPA-PSK
} ```

Run at boot:

1. Add openhub user with correct permissions:

sudo adduser openhubdaemon
sudo adduser openhubdaemon spi
sudo adduser openhubdaemon gpio

2. Set option to wait for wifi before running hub
raspi-config wait for wifi

place in: /etc/systemd/system/OpenHub.service

[Unit]
Description = OpenHub daemon
Wants = network-online.target systemd-networkd-wait-online.service OpenHubAPI.service
After = network-online.target systemd-networkd-wait-online.service local-fs.target OpenHubAPI.service

[Service]
User = openhubdaemon
Environment="PATH=/home/openhubdaemon/"
# Script starting HAP-python, e.g. main.py
# Be careful to set any paths you use, e.g. for persisting the state.
ExecStart = /usr/bin/python3 /home/openhubdaemon/OpenHub/OpenHub/run_bridge.py

[Install]
WantedBy = multi-user.target


sudo apt-get install python3-pip

pip install openhub