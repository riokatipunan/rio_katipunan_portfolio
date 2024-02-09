from crossover import crossover
from mutation import mutate
import numpy as np
from typing import Tuple

def mate(flat_nn1:np.ndarray, flat_nn2:np.ndarray) -> Tuple[np.ndarray,np.ndarray]:
    # instantiate the offsprings
    offspring1 = np.array([])
    offspring2 = np.array([])
    
    # perform crossover and mutation
    offspring1, offspring2 = crossover(flat_nn1 = flat_nn1, flat_nn2 = flat_nn2)
    offspring1 = mutate(offspring1)
    offspring2 = mutate(offspring2)
    
    return offspring1, offspring2


