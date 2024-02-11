from crossover import crossover
from mutation import mutate
import numpy as np
from typing import Tuple
from network import Network, flatten_NN, reconstruct_NN


def mate(nn1:Network, nn2:Network) -> Tuple[Network,Network]:
    # instantiate the offsprings
    offspring1 = np.array([])
    offspring2 = np.array([])
    
    # flatten the parent networks
    flat_nn1, num_layers_1, nn_layer_dims_1 = flatten_NN(nn1)
    flat_nn2, num_layers_2, nn_layer_dims_2 = flatten_NN(nn2)

    # perform crossover and mutation
    offspring1, offspring2 = crossover(flat_nn1 = flat_nn1, flat_nn2 = flat_nn2)
    
    # mutate the offspings
    offspring1 = mutate(offspring1)
    offspring2 = mutate(offspring2)

    offspring1_network = reconstruct_NN(offspring1, num_layers_1, nn_layer_dims_1)
    offspring2_network = reconstruct_NN(offspring2, num_layers_2, nn_layer_dims_2)
    
    # release some memory
    del offspring1
    del offspring2

    return offspring1_network, offspring2_network


