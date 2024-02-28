import numpy as np
from numpy.typing import NDArray
import copy

# perform mutation
def mutate(flat_nn:NDArray, mutation_rate:float = 0.1) -> NDArray:
    """
    This function mutates the weights and biases of a flat neural network
    
    Arguments:
        flat_nn:NDArray
            the neural network in its flat form

        mutation_rate:float
            the rate of mutation to used in this operation

    Returns:
        new_flat_nn:NDArray
            the new flat neural network with mutations in it.
    """
    new_flat_nn = copy.deepcopy(flat_nn)
    for idx, _ in enumerate(new_flat_nn):
        if np.random.uniform(0,1) > (1 - mutation_rate):
            new_flat_nn[idx] = np.random.uniform(-10,10)
            
    return new_flat_nn

def dropout(flat_nn:NDArray, dropout_rate:float = 0.1) -> NDArray:

    """
    This function performs dropouts to the weights and biases of a flat neural network
    
    Arguments:
        flat_nn:NDArray
            the neural network in its flat form

        dropout_rate:float
            the rate of dropout to used in this operation

    Returns:
        new_flat_nn:NDArray
            the new flat neural network with mutations in it.
    """

    new_flat_nn = copy.deepcopy(flat_nn)
    for idx, _ in enumerate(new_flat_nn):
        if np.random.uniform(0,1) > (1 - dropout_rate):
            new_flat_nn[idx] = 0.
            
    return new_flat_nn

def hypermutate(mutation_rate:float, average_fitness:float, mean_historical_average_fitness:float) -> float:
    """
    This function changes the mutation rate depending on the performance of the algorithm.
    It increases the mutation rate if the algorithm is perfoming poorly, hence prioritizing search over exploitation.
    If the algorithm performs well, it decreases the mutation rate.


    Argument:
        mutation_rate:float
            the current mutation rate of the algorithm
        
        average_fitness:float
            the average fitness of a population

        mean_historical_average_fitness:float
            the mean of the historical average fitness of the previous populations

    Returns:
        mutation_rate:float
            the new mutation rate of the algorithm
    """

    mutation_rate = 0.

    # check if the fitness of the population is underperforming the historical average fitness
    # if it is the case, then add 0.05 in the mutation rate
    if (average_fitness < mean_historical_average_fitness) and (mutation_rate <= 1):
        mutation_rate += 0.05
    
    # else if the average fitness of the population is performing better 
    # than the historical average fitness, then decrease the mutation rate
    # by 0.05; if the decrease is less than 0.1, maintain it at 0.1
    elif mutation_rate > 0.1:
        mutation_rate -= 0.05
        # print(f'Mutation rate: {mutation_rate:.2f}')
    else:
        mutation_rate = 0.1
        # print(f'Mutation rate: {mutation_rate:.2f}')

    return mutation_rate