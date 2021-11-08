from abc import ABC, abstractmethod

class StatInterface(ABC):
    def __init__(self, dct):
        if 'id' in dct:
            self.id = dct['id']
        if 'type' in dct:
            self.type = dct['type']
        if 'value' in dct:
            self.old_value = dct['value']
            self.value = dct['value']

        self.update_on_server = False

    @abstractmethod
    def update(self, value):
        pass

    def check_if_value_updated(self):
        if self.old_value != self.value:
            self.update_on_server = True

    def value_updated_on_server(self):
        self.old_value = self.value
        self.update_on_server = False;