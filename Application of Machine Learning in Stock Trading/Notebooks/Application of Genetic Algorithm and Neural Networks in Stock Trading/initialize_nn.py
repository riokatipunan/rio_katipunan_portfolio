from network import Network
from fc_layer import FCLayer
from activation_layer import ActivationLayer
<<<<<<< HEAD
from activation_function import tanh, soft_max
=======
from activation_function import tanh, soft_max, sigmoid, swish
from batch_norm import BatchNormLayer
>>>>>>> dac67c56 (updated file)

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
<<<<<<< HEAD
    net.add(ActivationLayer(tanh))
    net.add(FCLayer(100, 50))
    net.add(ActivationLayer(tanh))
    net.add(FCLayer(50, 3))
    net.add(ActivationLayer(soft_max))

    return net
=======
    net.add(ActivationLayer(swish))
    net.add(BatchNormLayer())
    net.add(FCLayer(100, 50))
    net.add(ActivationLayer(swish))
    net.add(BatchNormLayer())
    net.add(FCLayer(50, 3))
    net.add(ActivationLayer(soft_max))

    return net

def test_init_nn():
    # initialize NN
    net = Network()
    net.add(FCLayer(2, 3))
    net.add(ActivationLayer(sigmoid))
    net.add(FCLayer(3, 3))
    net.add(ActivationLayer(soft_max))

    return net
>>>>>>> dac67c56 (updated file)
