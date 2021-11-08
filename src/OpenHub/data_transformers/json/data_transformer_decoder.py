import json
from data_transformers.divide import Divide
from data_transformers.max import Max
from data_transformers.min import Min
from data_transformers.product import Product
from data_transformers.difference import Difference
from data_transformers.sum import Sum

class DataTransformerDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        data_transformers = []
        if 'data_transformers' in dct and dct['data_transformers'] is not None:
            for data_transformer in dct['data_transformers']:
                transformer = json.loads(data_transformer, cls=self.__class__)
                data_transformers.append(transformer)

        type = dct['type']

        if type == 'Divide':
            return Divide(dct,data_transformers)
        if type == 'Max':
            return Max(dct,data_transformers)
        if type == 'Multiply':
            return Product(dct,data_transformers)
        if type == 'Subtract':
            return Difference(dct,data_transformers)
        if type == 'Min':
            return Min(dct,data_transformers)
        if type == 'Sum':
            return Sum(dct,data_transformers)
