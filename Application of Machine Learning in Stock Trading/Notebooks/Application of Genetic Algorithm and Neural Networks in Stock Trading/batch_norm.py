from layer import Layer
from typing import Any, Callable
import numpy as np
import math

# inherit from base class Layer
class BatchNormLayer(Layer):
    def __init__(self):
        self.mean = 0
        self.std = 0

    # returns the activated input
    def forward_propagation(self, input_data):
        self.mean = np.mean(input_data)
        self.std = np.std(input_data)
        self.output = (input_data - self.mean)/math.sqrt(self.std**2)
        return self.output

    # # Returns input_error=dE/dX for a given output_error=dE/dY.
    # # learning_rate is not used because there is no "learnable" parameters.
    # def backward_propagation(self, output_error, learning_rate):
    #     return self._activation_prime(self.input) * output_error