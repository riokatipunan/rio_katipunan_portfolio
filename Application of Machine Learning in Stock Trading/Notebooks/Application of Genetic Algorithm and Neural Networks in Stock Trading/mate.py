from crossover import crossover
from mutation import dropout, mutate
import numpy as np
from typing import Tuple, MutableSequence
from network import Network, flatten_NN, reconstruct_NN
import math


def mate(nn1:Network, nn2:Network, mutation_rate = 0.1, dropout_rate = 0.1) -> Tuple[Network,Network]:
    """
    This function mates two parent neural networks and produces two offsprings 
    
    Arguments:
        nn1:Network
            the first parent neural network

        nn2:Network
            the second parent neural network
        
        mutation_rate:float
            the mutation rate to be applied during the mutation of the offsprings

        dropout_rate:float
            the dropout rate to be applied to the offsprings

    Returns:
        offspring1_network, offspring2_network: Tuple[Network, Network]
            the offsprings of the parents
    
    """

    # instantiate the offsprings
    offspring1 = np.array([])
    offspring2 = np.array([])
    
    # flatten the parent networks
    flat_nn1, num_layers_1, nn_layer_dims_1, nn_activation_funcs_1 = flatten_NN(nn1)
    flat_nn2, num_layers_2, nn_layer_dims_2, nn_activation_funcs_2 = flatten_NN(nn2)

    # perform crossover and mutation
    offspring1, offspring2 = crossover(flat_nn1 = flat_nn1, flat_nn2 = flat_nn2)
    
    # mutate the offspings
    offspring1 = mutate(flat_nn = offspring1, mutation_rate = mutation_rate)
    offspring2 = mutate(flat_nn = offspring2, mutation_rate = mutation_rate)

    # apply dropout to the weights of the neural network
    offspring1 = dropout(flat_nn = offspring1, dropout_rate = dropout_rate)
    offspring2 = dropout(flat_nn = offspring2, dropout_rate = dropout_rate)

    # reconstruct the neural network
    offspring1_network = reconstruct_NN(offspring1, num_layers_1, nn_layer_dims_1, nn_activation_funcs_1)
    offspring2_network = reconstruct_NN(offspring2, num_layers_2, nn_layer_dims_2, nn_activation_funcs_2)
    
    # release some memory
    del offspring1
    del offspring2

    return offspring1_network, offspring2_network

def reproduce_population(population: MutableSequence[Network], mutation_rate:float = 0.1, dropout_rate:float = 0.1) -> MutableSequence[Network]:
    """
    This function performs mating to all individuals in the population

    Arguments:
        population:MutableSequence[Network]
            the population to be reproduced
        
        mutation_rate:float
            the rate of mutation to used in the reproduction

        dropout_rate:float
            the dropout rate to be used in the neural networks

    Returns:
        new_population:MutableSequence[Network]
            the new population with the offsprings of the prior population
    """

    new_population = list()
    offspring_population = list()
    left_bracket = population[:math.floor(len(population)/2):]
    right_bracket = population[math.floor(len(population)/2)::]

    for left_nn, right_nn in zip(left_bracket, right_bracket):
        offsprin1, offspring2 = mate(nn1 = left_nn, nn2 = right_nn, mutation_rate = mutation_rate, dropout_rate = dropout_rate)
        offspring_population.append(offsprin1)
        offspring_population.append(offspring2)

    new_population = population + offspring_population

    return new_population

def reduce_population(population: MutableSequence[Network], remove_percentage:float) -> MutableSequence[Network]:
    """
    This function trims the population
    
    Arguments:
        population:MutableSequence[Network]
            the population to be trimmed
            
        remove_percentage:float
            the percentage of the population to be removed
            for example, a remove_percentage of 
    
    Returns:
        new_population:MutableSequence[Network]
            the new reduced population 
    """
    
    new_population = population[:-math.floor(len(population)*remove_percentage):]

    return new_population

def restrict_population_size(population: MutableSequence[Network], max_number_of_population:int):
    """
    This function restricts the size of a population to a certain size

    Arguments:
        population:MutableSequence[Network]
            the population to be restricted

        max_number_of_population:int
            the maximum number of individuals in a population
    """

    assert len(population) > max_number_of_population, 'the population size should be more'

    new_population = population[:max_number_of_population:]
    
    return new_population