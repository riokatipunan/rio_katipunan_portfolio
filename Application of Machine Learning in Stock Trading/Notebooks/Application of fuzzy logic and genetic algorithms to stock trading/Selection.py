import copy
from multiprocessing import Pool, cpu_count
import pandas as pd
from Population import Population
from functools import reduce
import random

    
def roulette_wheel(population: Population, fitness_func: callable, series: pd.DataFrame) -> Population:
    """
    This function selects the genomes in a population through the roullete
    wheel method
    
    Arguments:
        population:Populatoion
    Returns:
        None
    """
    
    fitness_list = list()
    series_list = list()
    func_list = list()
    population_list = population.population
    for _ in range(len(population_list)):
        series_list.append(copy.deepcopy(series))
        
    for i in range(len(population_list)):
        func_list.append((series_list[i], population_list[i]))
        
    with Pool(cpu_count()) as p:
        fitness_list = p.starmap(fitness_func, func_list) 
    
    print(fitness_list)

    lowest_fitness = 0.
    for fitness in fitness_list:
        if (fitness < lowest_fitness) and (fitness != float('-inf')):
            lowest_fitness = fitness
        
    adjusted_fitness_list = list()
    for idx, fitness in enumerate(fitness_list):
        adjusted_fitness_list.append(fitness - lowest_fitness + 1)

    total_fitness = 0
    for adjusted_fitness in adjusted_fitness_list:
        if adjusted_fitness != float('-inf'):
            total_fitness +=  adjusted_fitness
    
    selection_probability = list()
    for adjusted_fitness in adjusted_fitness_list:
        selection_probability.append(adjusted_fitness/total_fitness)
        
    new_population = list()
    for idx, _ in enumerate(selection_probability):
        if selection_probability[idx] > random.randint(0,1):
            new_population.append(population_list[idx])
    print(adjusted_fitness_list)
    print(new_population)
    return selection_probability
    
def rank(self):
    """
    Some text
    """
    pass
    
def steady_state(self):
    """
    Some text
    """
    pass
    
def tournament(self):
    """
    Some text
    """
    pass
    
def elitist(self):
    """
    Some text
    """
    pass
    
def boltzman(self):
    """
    Some text
    """
    pass
    
def reward_based(self):
    """
    Some text
    
    Reference:
    https://en.wikipedia.org/wiki/Reward-based_selection
    """
    pass
    
def SUS(self):
    """
    Stochastic universal sampling
    
    Reference:
    https://en.wikipedia.org/wiki/Stochastic_universal_sampling
    """
    pass