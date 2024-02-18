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