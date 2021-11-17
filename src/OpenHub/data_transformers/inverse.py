import logging
from .data_transformer import DataTransformer


class Inverse(DataTransformer):

    def perform_op(self, inputs):
        product = 1
        for input in inputs:
            if input == 0:
                self.logger.info('input is 0 returning -1 ')

                return -1
            product = float(1/float(input))
        self.logger.info('inverted ' + str(product))
        return product