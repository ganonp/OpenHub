import logging
from .data_transformer import DataTransformer


class Max(DataTransformer):

    def perform_op(self, inputs):
        return max(inputs)