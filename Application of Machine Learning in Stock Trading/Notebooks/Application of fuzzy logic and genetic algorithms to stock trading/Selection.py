import copy
from multiprocessing import Pool, cpu_count
import pandas as pd
from Population import Population
import random

def RWS(population: Population, fitness_func: callable, series: pd.DataFrame, num_population:int = 100, num_new_population = 50) -> Population:
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
    func_args_list = list()
    genome_list = population.population
    valid_fitness_list = list()
    valid_genome_list = list()
    new_population_list = list()
    
    # create a list containing the training data set with the same length as the population list 
    for _ in range(len(genome_list)):
        series_list.append(copy.deepcopy(series))
        
    # join the series list and population list to produce one single iterable
    # this will be used in the starmap function in the multiprocessing module
    for i in range(len(genome_list)):
        func_args_list.append((series_list[i], genome_list[i]))
    
    # evaluate the genomes in the population
    with Pool(cpu_count()) as p:
        fitness_list = p.starmap(fitness_func, func_args_list) 

    # sequential processing
    # for genome in genome_list:
    #     fitness_list.append(fitness_func(series = series, genome = genome))

    for idx, fitness in enumerate(fitness_list):
        if fitness != float('-inf'):
            valid_fitness_list.append(fitness)
            valid_genome_list.append(genome_list[idx])

    # get the lowest fitness value in the population
    lowest_fitness = 0.
    for fitness in valid_fitness_list:
        if (fitness < lowest_fitness):
            lowest_fitness = fitness
    
    # adjust the fitness of all individuals in the population
    adjusted_fitness_list = list()
    for idx, fitness in enumerate(valid_fitness_list):
        adjusted_fitness_list.append(fitness - lowest_fitness + 1)

    # compute for the total fitness of the population
    total_fitness = 0
    for adjusted_fitness in adjusted_fitness_list:
        if adjusted_fitness != float('-inf'):
            total_fitness +=  adjusted_fitness
    
    average_fitness = total_fitness/len(adjusted_fitness_list)

    # compute for the selection probability of an individual 
    # based on the total fitness of the population
    selection_probability_list = list()
    for adjusted_fitness in adjusted_fitness_list:
        selection_probability_list.append(adjusted_fitness/total_fitness)

    for i in range(num_new_population):
        if len(new_population_list) > 50:
            break
        else:
            idx = 0
            probability_sum = selection_probability_list[idx]
            selection_probability = random.uniform(0,1)
            while probability_sum < selection_probability:
                idx += 1
                probability_sum += selection_probability_list[idx]
            new_population_list.append(valid_genome_list[idx])

    new_population = Population(new_population_list)

    return new_population, average_fitness

def rank(population: Population, fitness_func: callable, series: pd.DataFrame, num_population:int = 100, num_new_population = 50) -> Population:
    """
    This function selects the genomes in a population through
    rank selection

    Arguments:
        population:Populatoion
    Returns:
        new_population:Population
    """
    fitness_list = list()
    series_list = list()
    func_args_list = list()
    genome_list = population.population
    valid_fitness_list = list()
    valid_genome_list = list()
    new_population_list = list()
    genome_rank_list = list()

    # create a list containing the training data set with the same length as the population list 
    for _ in range(len(genome_list)):
        series_list.append(copy.deepcopy(series))
        
    # join the series list and population list to produce one single iterable
    # this will be used in the starmap function in the multiprocessing module
    for i in range(len(genome_list)):
        func_args_list.append((series_list[i], genome_list[i]))
    
    # evaluate the genomes in the population
    with Pool(cpu_count()) as p:
        fitness_list = p.starmap(fitness_func, func_args_list) 
    
    # sequential processing
    # for genome in genome_list:
    #     fitness_list.append(fitness_func(series = series, genome = genome))

    for idx, fitness in enumerate(fitness_list):
        if fitness != float('-inf'):
            valid_fitness_list.append(fitness)
            valid_genome_list.append(genome_list[idx])

    # get the lowest fitness value in the population
    lowest_fitness = 0.
    for fitness in valid_fitness_list:
        if (fitness < lowest_fitness):
            lowest_fitness = fitness
    
    # adjust the fitness of all individuals in the population
    adjusted_fitness_list = list()
    for idx, fitness in enumerate(valid_fitness_list):
        adjusted_fitness_list.append(fitness - lowest_fitness + 1)

    # compute for the total fitness of the population
    total_fitness = 0
    for adjusted_fitness in adjusted_fitness_list:
        if adjusted_fitness != float('-inf'):
            total_fitness +=  adjusted_fitness
    
    average_fitness = total_fitness/len(adjusted_fitness_list)    

    # sort the list of genomes
    temp_fitness_value = 0
    temp_genome = None
    for i in range(len(adjusted_fitness_list)):
        for j in range(len(adjusted_fitness_list)-i):
            if adjusted_fitness_list[j+i] < adjusted_fitness_list[i]:
                temp_fitness_value = adjusted_fitness_list[i]
                adjusted_fitness_list[i] = adjusted_fitness_list[j+i]
                adjusted_fitness_list[j+i] = temp_fitness_value

                temp_genome = valid_genome_list[i]
                valid_genome_list[i] = valid_genome_list[j+i]
                valid_genome_list[j+i] = temp_genome

    for i in range(len(adjusted_fitness_list)):
        genome_rank_list.append(i+1)

    # compute for the total fitness of the population
    total_rank = 0
    for rank in genome_rank_list:
        total_rank +=  rank

    # compute for the selection probability of an individual 
    # based on the total rank of the population
    selection_probability_list = list()
    for rank in genome_rank_list:
        selection_probability_list.append(rank/total_rank)

    # select the new population based on ranking selection
    for i in range(num_new_population):
        if len(new_population_list) > 50:
            break
        else:
            idx = 0
            probability_sum = selection_probability_list[idx]
            selection_probability = random.uniform(0,1)
            while probability_sum < selection_probability:
                idx += 1
                probability_sum += selection_probability_list[idx]
            new_population_list.append(valid_genome_list[idx])

    new_population = Population(new_population_list)

    return new_population, average_fitness
    
def tournament(population: Population, fitness_func: callable, series: pd.DataFrame, num_population:int = 100, num_new_population = 50) -> Population:
    """
    This function selects the genomes in a population through
    tournament selection

    Arguments:
        population:Populatoion
    Returns:
        new_population:Population
    """
    fitness_list = list()
    series_list = list()
    func_args_list = list()
    genome_list = population.population
    valid_fitness_list = list()
    valid_genome_list = list()
    new_population_list = list()
    
    # create a list containing the training data set with the same length as the population list 
    for _ in range(len(genome_list)):
        series_list.append(copy.deepcopy(series))
        
    # join the series list and population list to produce one single iterable
    # this will be used in the starmap function in the multiprocessing module
    for i in range(len(genome_list)):
        func_args_list.append((series_list[i], genome_list[i]))
    
    # evaluate the genomes in the population
    with Pool(cpu_count()) as p:
        fitness_list = p.starmap(fitness_func, func_args_list) 

    # sequential processing
    # for genome in genome_list:
    #     fitness_list.append(fitness_func(series = series, genome = genome))

    for idx, fitness in enumerate(fitness_list):
        if fitness != float('-inf'):
            valid_fitness_list.append(fitness)
            valid_genome_list.append(genome_list[idx])

    # get the lowest fitness value in the population
    lowest_fitness = 0.
    for fitness in valid_fitness_list:
        if (fitness < lowest_fitness):
            lowest_fitness = fitness
    
    # adjust the fitness of all individuals in the population
    adjusted_fitness_list = list()
    for idx, fitness in enumerate(valid_fitness_list):
        adjusted_fitness_list.append(fitness - lowest_fitness + 1)

    # compute for the total fitness of the population
    total_fitness = 0
    for adjusted_fitness in adjusted_fitness_list:
        if adjusted_fitness != float('-inf'):
            total_fitness +=  adjusted_fitness

    average_fitness = total_fitness/len(adjusted_fitness_list)    

    # select the genomes for the new population
    for i in range(num_new_population):
        idx_a = random.randint(0, len(adjusted_fitness_list)-1)
        idx_b = random.randint(0, len(adjusted_fitness_list)-1)

        if adjusted_fitness_list[idx_a] > adjusted_fitness_list[idx_b]:
            new_population_list.append(valid_genome_list[idx_a])
        else:
            new_population_list.append(valid_genome_list[idx_b])

    new_population = Population(new_population_list)

    return new_population, average_fitness
    
def SUS(population: Population, fitness_func: callable, series: pd.DataFrame, num_population:int = 100, num_new_population = 50) -> Population:
    """
    This function selects the genomes in a population through
    Stochastic universal sampling
    
    Reference:
    https://en.wikipedia.org/wiki/Stochastic_universal_sampling

    Arguments:
        population:Populatoion
    Returns:
        new_population:Population
    """
    fitness_list = list()
    series_list = list()
    func_args_list = list()
    genome_list = population.population
    valid_fitness_list = list()
    valid_genome_list = list()
    new_population_list = list()
    
    # create a list containing the training data set with the same length as the population list 
    for _ in range(len(genome_list)):
        series_list.append(copy.deepcopy(series))
        
    # join the series list and population list to produce one single iterable
    # this will be used in the starmap function in the multiprocessing module
    for i in range(len(genome_list)):
        func_args_list.append((series_list[i], genome_list[i]))
    
    # evaluate the genomes in the population
    with Pool(cpu_count()) as p:
        fitness_list = p.starmap(fitness_func, func_args_list) 
    
    # sequential processing
    # for genome in genome_list:
    #     fitness_list.append(fitness_func(series = series, genome = genome))

    for idx, fitness in enumerate(fitness_list):
        if fitness != float('-inf'):
            valid_fitness_list.append(fitness)
            valid_genome_list.append(genome_list[idx])

    # get the lowest fitness value in the population
    lowest_fitness = 0.
    for fitness in valid_fitness_list:
        if (fitness < lowest_fitness):
            lowest_fitness = fitness
    
    # adjust the fitness of all individuals in the population
    adjusted_fitness_list = list()
    for idx, fitness in enumerate(valid_fitness_list):
        adjusted_fitness_list.append(fitness - lowest_fitness + 1)

    # compute for the total fitness of the population
    total_fitness = 0
    for adjusted_fitness in adjusted_fitness_list:
        if adjusted_fitness != float('-inf'):
            total_fitness +=  adjusted_fitness
    
    average_fitness = total_fitness/len(adjusted_fitness_list)    

    # compute for the selection probability of an individual 
    # based on the total fitness of the population
    selection_probability_list = list()
    for adjusted_fitness in adjusted_fitness_list:
        selection_probability_list.append(adjusted_fitness/total_fitness)

    # define the pointer distance and the list of pointers to be used
    pointer_distance = total_fitness/num_new_population
    start = random.uniform(0,1)
    pointers = [start + i*pointer_distance for i in range(num_new_population)]

    # select the genomes for the new population
    new_population_list = list()
    for point in pointers:
        idx = 0
        fitness_sum = adjusted_fitness_list[idx]
        while fitness_sum < point:
            idx += 1
            fitness_sum += adjusted_fitness_list[idx]
        new_population_list.append(copy.deepcopy(valid_genome_list[idx]))

    new_population = Population(new_population_list)

    return new_population, average_fitness