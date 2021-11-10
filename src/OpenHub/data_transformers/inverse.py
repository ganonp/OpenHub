import logging
from .data_transformer import DataTransformer


class Inverse(DataTransformer):

    def perform_op(self, inputs):
        for input in inputs:
            product = float(1/float(input))
        return product