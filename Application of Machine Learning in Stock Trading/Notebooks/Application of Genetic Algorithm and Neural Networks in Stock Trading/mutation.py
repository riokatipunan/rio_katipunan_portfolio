import numpy as np
import copy

# perform mutation
def mutate(flat_nn, mutation_rate: float = 0.1) -> np.ndarray:

    new_flat_nn = copy.deepcopy(flat_nn)
    for idx, _ in enumerate(new_flat_nn):
        if np.random.uniform(0,1) > (1 - mutation_rate):
            if np.random.uniform(0,1) > 0.1:
                new_flat_nn[idx] = np.random.uniform(-10,10)
            else:
                new_flat_nn[idx] = 0.
            # new_flat_nn[idx] = np.random.uniform(-10,10)
            
    return new_flat_nn

def hypermutate(mutation_rate, average_fitness, mean_historical_average_fitness):
    mutation_rate = 0.

    # check if the fitness of the population is underperforming the historical average fitness
    # if it is the case, then add 0.05 in the mutation rate
    if average_fitness < mean_historical_average_fitness:
        if mutation_rate <= 1:
            mutation_rate += 0.05
    
    # else if the average fitness of the population is performing better 
    # than the historical average fitness, then decrease the mutation rate
    # by 0.05; if the decrease is less than 0.1, maintain it at 0.1
    else:
        if mutation_rate > 0.1:
            mutation_rate -= 0.05
            # print(f'Mutation rate: {mutation_rate:.2f}')
        else:
            mutation_rate = 0.1
            # print(f'Mutation rate: {mutation_rate:.2f}')

    return mutation_rate