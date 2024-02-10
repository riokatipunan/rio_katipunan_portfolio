import numpy as np
import copy

# perform mutation
def mutate(flat_nn, mutation_rate: float = 0.1) -> np.ndarray:

    new_flat_nn = copy.deepcopy(flat_nn)
    for idx, _ in enumerate(new_flat_nn):
        if np.random.uniform(0,1) > (1 - mutation_rate):
            new_flat_nn[idx] = np.random.rand()
            
    return new_flat_nn