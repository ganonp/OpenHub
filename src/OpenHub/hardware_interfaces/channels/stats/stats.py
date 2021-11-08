import requests


class Stats:
    def __init__(self, stats_config):
        self.stats = stats_config

    def update(self,value):
        for stat in self.stats:
            stat.update(value)

    def update_server(self,stat):
        stat_dict = {}
        stat_dict['id'] = stat.id
        stat_dict['value'] = stat.value
        response = requests.post('http://' + '192.168.3.132' + ':8000/channelstats/', json=stat_dict)

    def update_on_server(self):
        for stat in self.stats:
            if stat.update_on_server:
                self.update_server(stat)
                stat.value_updated_on_server()