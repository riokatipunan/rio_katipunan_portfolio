from crossover import crossover
from mutation import mutate
import numpy as np
from typing import Tuple, MutableSequence
from network import Network, flatten_NN, reconstruct_NN
import math


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

def reproduce_population(population: MutableSequence[Network]) -> MutableSequence[Network]:
    new_population = list()
    offspring_population = list()
    left_bracket = population[:math.floor(len(population)/2):]
    right_bracket = population[math.floor(len(population)/2)::]

    for left_nn, right_nn in zip(left_bracket, right_bracket):
        offsprin1, offspring2 = mate(left_nn, right_nn)
        offspring_population.append(offsprin1)
        offspring_population.append(offspring2)

    new_population = population + offspring_population

    return new_population

def reduce_population(population: MutableSequence[Network], remove_percentage:float):
    """
    This function trims the population
    
    Arguments:
        population:MutableSequence[Network]
            the population to be trimmed
            
        remove_percentage:float
            the percentage of the population to be removed
            for example, a remove_percentage of 
    
    Returns:
    
    
    """
    
    
    
    new_population = population[:-math.floor(len(population)*remove_percentage):]

    return new_population