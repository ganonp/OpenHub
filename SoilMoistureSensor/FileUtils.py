import json


class FileUtils:
    def __init__(self, absolute_path):
        self.root = absolute_path
        self.bridge_path = self.root + "/config/bridge"
        self.accessory_path = self.root + "/config/acccessories"

    def add_bridge_config(self, dict):
        with open(self.bridge_path, 'w') as file:
            file.write(json.dumps(dict))
