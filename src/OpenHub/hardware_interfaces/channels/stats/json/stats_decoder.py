import json
from OpenHub.hardware_interfaces.channels.stat.json.stat_decoder import StatDecoder
from OpenHub.hardware_interfaces.channels.stats.stats import Stats


class StatsDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        stats = []
        for stat in dct:
            stat = json.loads(stat, cls=StatDecoder)
            stats.append(stat)
        return Stats(stats)

