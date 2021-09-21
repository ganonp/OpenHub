import json
from calibrators import RawValueConverter


class RawValueEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, RawValueConverter):
            dict = o.__dict__
            dict['type'] = o.__name__

        return json.JSONEncoder.default(self, o)
