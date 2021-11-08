import logging
from data_transformer import DataTransformer


class Product(DataTransformer):

    def perform_op(self, inputs):
        product = 1
        for input in inputs:
            product = product * input
        return product