import requests
import json
import time
from OpenHub.main import openhub_api_ip

class Stats:
    def __init__(self, stats_config):
        self.stats = stats_config
        self.last_updated = time.time() - 900

    def update(self,value):
        min_stat = None
        max_stat = None
        for stat in self.stats:
            if stat.type == 'MIN':
                min_stat = stat
            if stat.type == 'MAX':
                max_stat = stat
        min_stat.update(value)
        if min_stat.value != value:
            max_stat.update(value)
        if time.time() - self.last_updated > 900:
            self.last_updated = time.time()
            self.update_server_with_data_point(value)

    def update_server(self,stat):
        stat_dict = {}
        stat_dict['id'] = stat.id
        stat_dict['type'] = stat.type
        stat_dict['value'] = stat.value
        stat_dict['channel'] = stat.channel_serial
        response = requests.post('http://' + str(openhub_api_ip) + ':8000/channelstats/', data=stat_dict)

    def update_server_with_data_point(self,value):
        stat_dict = {}
        stat_dict['value'] = str(int(float(value)))
        stat_dict['channel'] = str(self.stats[0].channel_serial)
        response = requests.post('http://' + str(openhub_api_ip) + ':8000/channelstatdatapoint/', data=stat_dict)

    def update_on_server(self):
        for stat in self.stats:
            if stat.update_on_server:
                self.update_server(stat)
                stat.value_updated_on_server()
