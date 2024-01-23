import copy
from multiprocessing import Pool, cpu_count
import pandas as pd
from Population import Population
from functools import reduce
import random

    
def roulette_wheel(population: Population, fitness_func: callable, series: pd.DataFrame, num_population:int = 100) -> Population:
    """
    This function selects the genomes in a population through the roullete
    wheel method
    
    Arguments:
        population:Populatoion
    Returns:
        new_population:Population
    """
    
    fitness_list = list()
    series_list = list()
    func_list = list()
    population_list = population.population
    
    # create a list containing the training data set with the same length as the population list 
    for _ in range(len(population_list)):
        series_list.append(copy.deepcopy(series))
        
    # join the series list and population list to produce one single iterable
    # this will be used in the starmap function in the multiprocessing module
    for i in range(len(population_list)):
        func_list.append((series_list[i], population_list[i]))
    
    # evaluate the genomes in the population
    with Pool(cpu_count()) as p:
        fitness_list = p.starmap(fitness_func, func_list) 

    # get the lowest fitness value in the population
    lowest_fitness = 0.
    for fitness in fitness_list:
        if (fitness < lowest_fitness) and (fitness != float('-inf')):
            lowest_fitness = fitness
    
    # adjust the fitness of all individuals in the population
    adjusted_fitness_list = list()
    for idx, fitness in enumerate(fitness_list):
        adjusted_fitness_list.append(fitness - lowest_fitness + 1)

    # compute for the total fitness of the population
    total_fitness = 0
    for adjusted_fitness in adjusted_fitness_list:
        if adjusted_fitness != float('-inf'):
            total_fitness +=  adjusted_fitness
    
    # compute for the selection probability of an individual 
    # based on the total fitness of the population
    selection_probability = list()
    for adjusted_fitness in adjusted_fitness_list:
        selection_probability.append(adjusted_fitness/total_fitness)
    
    # select the next population of the evolution
    new_population_genomes = list()
    for idx, _ in enumerate(selection_probability):
        if selection_probability[idx] > random.uniform(0,1):
            new_population_genomes.append(population_list[idx])

    new_population = Population(genome_list=new_population_genomes)
    
    if len(new_population) > num_population:
        new_population = new_population[0:100]
    
    return new_population
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