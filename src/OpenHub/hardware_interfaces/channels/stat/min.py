from .stat_interface import StatInterface

class Min(StatInterface):
    def __init__(self,dct=None,id=None,value=None,channel_serial=None):
        super().__init__(dct=dct, id=id, value=value, type='MIN',channel_serial=channel_serial)

    def update(self, value):
        if float(value) < self.value:
            self.value = float(value)
            self.check_if_value_updated()
