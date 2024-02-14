from typing import Iterable, MutableSequence
from network import Network
from initialize_nn import initialize_nn

def initialize_population(num_individuals:int) -> MutableSequence[Network]:
    population = list()
    for _ in range(num_individuals):
        population.append(initialize_nn())

    return population