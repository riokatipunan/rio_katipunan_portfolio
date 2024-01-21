import copy
from multiprocessing import Pool, cpu_count
import pandas as pd
from Population import Population

    
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
    
    return fitness_list
    
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