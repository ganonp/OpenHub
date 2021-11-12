import logging
from .data_transformer import DataTransformer


class Sum(DataTransformer):

    def perform_op(self, inputs):
        out = sum(inputs)
        self.logger.info('summed ' + str(out))

        return out