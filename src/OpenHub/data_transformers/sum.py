import logging
from .data_transformer import DataTransformer


class Sum(DataTransformer):

    def perform_op(self, inputs):
        return sum(inputs)