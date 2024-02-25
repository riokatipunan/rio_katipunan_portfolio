from layer import Layer
from typing import Callable

# inherit from base class Layer
class ActivationLayer(Layer):

    def __init__(self, activation: Callable):
        self._activation = activation

    def set_activation(self, activation: Callable):
        self._activation = activation

    def set_activation_prime(self, activation_prime: Callable):
        self._activation_prime = activation_prime

    def get_activation(self):
        return self._activation

    def get_activation_prime(self):
        return self._activation_prime

    # returns the activated input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self._activation(self.input)
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    # def backward_propagation(self, output_error, learning_rate):
    #     return self._activation_prime(self.input) * output_error