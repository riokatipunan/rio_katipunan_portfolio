from network import Network
from fc_layer import FCLayer
from activation_layer import ActivationLayer
from activation_function import tanh, soft_max

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
    net.add(ActivationLayer(tanh))
    net.add(FCLayer(100, 50))
    net.add(ActivationLayer(tanh))
    net.add(FCLayer(50, 3))
    net.add(ActivationLayer(soft_max))

    return net