from typing import Iterable, MutableSequence
from network import Network
from initialize_nn import initialize_nn, init_nn

def initialize_population(num_individuals:int) -> MutableSequence[Network]:
    population = list()
    for _ in range(num_individuals):
        population.append(initialize_nn())

    return population

def init_population(nn_topology, num_individuals:int) -> MutableSequence[Network]:
    population = list()
    for _ in range(num_individuals):
        population.append(init_nn(nn_topology = nn_topology))

    return population    