import logging
from .data_transformer import DataTransformer


class Divide(DataTransformer):

    def perform_op(self, inputs):
        if len(inputs) == 2:
            return inputs[0]/inputs[1]
        else:
            return 0