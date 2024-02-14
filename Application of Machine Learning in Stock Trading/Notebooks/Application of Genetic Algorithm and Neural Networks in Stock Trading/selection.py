from typing import Iterable, Sequence, MutableSequence
import math
from network import Network
import random

# def keep_elites(percentage_elites:float, population: Iterable[Network]):    
#     sorted_population = sorted(population, key=lambda x: x.fitness, reverse=False)
#     elite_population = list()
#     num_elites = math.floor(percentage_elites * len(population))
#     sorted_population = sorted(population, key=lambda x: x.fitness, reverse=False)
#     elite_population = sorted_population[:num_elites:]

#     return elite_population

def keep_elites(percentage_elites: float, population: Sequence[Network]):
    """
    This function returns the top elites in a population
    
    Arguments:
        percentage_elites:float
            the percentage of the individuals to keep in a population
            for example, if percentage_elites = 0.1, the function will return
            only the top 10% of the population
            
        population:Sequence[Network]
            a sequence of neural networks to be treated as the population
            
    Returns:
        elite_population:Sequence[Network]
            a sequence of neural networks that are the elites in a population
    
    """
    
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=False)
    elite_population = sorted_population[:math.floor(percentage_elites * len(population))]
    
    return elite_population


# implement tournament selection
def selection(population: MutableSequence[Network]):
    random.shuffle(population)
    selected_population = list()
    left_bracket = population[:math.floor(len(population)/2):]
    right_bracket = population[math.floor(len(population)/2)::]

    for left_nn, right_nn in zip(left_bracket, right_bracket):
        if left_nn.fitness > right_nn.fitness:
            selected_population.append(left_nn)
        else:
            selected_population.append(right_nn)

    return selected_population