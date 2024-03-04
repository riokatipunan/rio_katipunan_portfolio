from network import Network
from fc_layer import FCLayer
from activation_layer import ActivationLayer
from activation_function import tanh, soft_max, sigmoid, swish, ActivationFunction
from layer_norm import LayerNormLayer
from typing import List, Tuple


def initialize_nn() -> Network:
    """
    This function initializes an neural network

    Arguments:
        None

    Returns:
        net:Network
            the initialized neural network

    """

    # initialize NN
    net = Network()
    net.add(FCLayer(150, 100))
    net.add(ActivationLayer(swish))
    net.add(LayerNormLayer())
    net.add(FCLayer(100, 50))
    net.add(ActivationLayer(swish))
    net.add(LayerNormLayer())    
    net.add(FCLayer(50, 25))
    net.add(ActivationLayer(swish))
    net.add(LayerNormLayer())
    net.add(FCLayer(25, 3))
    net.add(ActivationLayer(soft_max))

    return net

# def test_init_nn():
#     # initialize NN
#     net = Network()
#     net.add(FCLayer(2, 3))
#     net.add(ActivationLayer(sigmoid))
#     net.add(FCLayer(3, 3))
#     net.add(ActivationLayer(soft_max))

#     return net

def init_nn(nn_topology:List[Tuple[int, int, ActivationFunction, bool]]):
    net = Network()
    for layer in nn_topology:
        (input_dim, output_dim, activation_function, enable_layernorm) = layer
        net.add(FCLayer(input_dim, output_dim))
        net.add(ActivationLayer(activation_function))
        if enable_layernorm:
            net.add(LayerNormLayer())

    return net
    
        


