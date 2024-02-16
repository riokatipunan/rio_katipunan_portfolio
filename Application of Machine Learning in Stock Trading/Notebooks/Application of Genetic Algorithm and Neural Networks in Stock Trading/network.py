import numpy as np
from batch_norm import BatchNormLayer
from fc_layer import FCLayer
from activation_layer import ActivationLayer
from activation_function import tanh, soft_max
from typing import List, Tuple, Union, Callable


class Network:
    def __init__(self):
        self.layers = []
        self.fitness = 0
        # self.loss = None
        # self.loss_prime = None

    # add layer to network
    def add(self, layer: Union[FCLayer, ActivationLayer,BatchNormLayer]) -> None:
        self.layers.append(layer)

    # set loss to use
    def use(self, loss: Callable, loss_prime:Callable) -> None:
        self.loss = loss
        self.loss_prime = loss_prime

    # predict output for given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    # predict output for given input
    def propagate_forward(self, input_data):
        # run network over all samples
        # forward propagation
        output = input_data
        for layer in self.layers:
            output = layer.forward_propagation(output)
        
        return output

    # train the network
    def fit(self, x_train, y_train, epochs:int, learning_rate:float):
        # sample dimension first
        samples = len(x_train)

        # training loop
        for i in range(epochs):
            err = 0.
            for j in range(samples):
                # forward propagation
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # compute loss (for display purpose only)
                err += self.loss(y_train[j], output)

                # backward propagation
                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            # calculate average error on all samples
            err /= samples
            print('epoch %d/%d   error=%f' % (i+1, epochs, err))

def flatten_NN(NN: Network):

    # initialize some variables
    flat_NN = np.array([])
    num_layers: int = 0
    NN_layer_dims: List[Tuple[int, int]] = list(tuple())
    
    # loop through all the layers in the network
    for layer in NN.layers:
        if isinstance(layer, FCLayer):
            NN_layer_dims.append(np.shape(layer.weights))
            flat_NN = np.append(flat_NN, layer.weights.flatten())
            flat_NN = np.append(flat_NN, layer.bias.flatten())
            num_layers += 1
    
    return flat_NN, num_layers, NN_layer_dims

def reconstruct_NN(flat_NN, num_layers, NN_layer_dims) -> Network:
    elems_taken = 0
    NN = Network()
    for layer_id, NN_layer_dim in zip(range(num_layers), NN_layer_dims):
        
        # instatiate variables
        rows, columns = NN_layer_dim
        fc_layer = FCLayer(rows, columns)
        layer_num_elems = rows*columns
        
        # get the weigths for the FC layer
        layer_weights_elems = flat_NN[elems_taken:elems_taken+layer_num_elems]
        elems_taken += layer_num_elems
        fc_layer.weights = np.reshape(layer_weights_elems, (rows, columns))
        
        # get the biases for the FC layer
        layer_bias_elems = flat_NN[elems_taken:elems_taken+columns]
        elems_taken += columns
        fc_layer.bias = np.reshape(layer_bias_elems, (1, columns))
        
        NN.add(fc_layer)
        
        if layer_id == num_layers-1:
            NN.add(ActivationLayer(soft_max)) 
        else:
            NN.add(ActivationLayer(tanh))   
        
    return NN