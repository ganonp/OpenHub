import logging
from .data_transformer import DataTransformer


class Min(DataTransformer):

    def perform_op(self, inputs):
        return min(inputs)