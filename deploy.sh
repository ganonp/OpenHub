for VARIABLE in "192.168.3.130"
do
  ssh root@$VARIABLE "sudo rm -r /home/lesserdaemon/.hap-python/SoilMoistureSensor"
  scp -r /Users/ganonpierce/src/SoilMoistureSensor/SoilMoistureSensor root@$VARIABLE:/home/lesserdaemon/.hap-python/SoilMoistureSensor
  ssh root@$VARIABLE "chmod -R a+x+r+w /home/lesserdaemon/.hap-python/SoilMoistureSensor"
  ssh root@$VARIABLE "chmod a+x+r+w /home/lesserdaemon/.hap-python/SoilMoistureSensor/accessory.state"
  ssh root@$VARIABLE "chmod a+x+r+w /home/lesserdaemon/.hap-python/SoilMoistureSensor/soil_sensor.json"
done