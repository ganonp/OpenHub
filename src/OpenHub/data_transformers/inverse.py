import logging
from .data_transformer import DataTransformer


class Inverse(DataTransformer):

    def perform_op(self, inputs):
        product = 1
        for input in inputs:
            product = float(1/float(input))
        self.logger.info('inverted ' + str(product))
        return product