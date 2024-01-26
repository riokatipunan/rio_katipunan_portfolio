from Gene import Gene
from Genome import Genome
from Population import Population
from Crossover import single_point, two_point, uniform, linear, SBX, crossover
from Fitness import evaluate_fitness
from Selection import roulette_wheel, RWS, SUS, tournament, rank
import random
import pandas as pd
import os
import pickle

def run(train_set:list[pd.DataFrame], base_genome:Genome, seed_genome:Genome, fitness_func:callable, num_generations:int = 100, checkpoint_interval:int = 5) -> None:
    """
    This function simulates evolution through the population
    of genes
    
    Arguments:
        population: population class
            a class of population
        
        generations: int
            the number of generations the evolution should run
            
        checkpoints: int
            the interval for saving a checkpoint in the evolution of the genomes
            
    Returns:
        None
        
    """
    SEED_GENOME:Genome = seed_genome
    BASE_GENOME:Genome = base_genome
    population = Population()
    population.seed_population(seed_genome = SEED_GENOME, num_seeds = 25)
    population.add_and_initialize_to_population(base_genome = BASE_GENOME, num_genomes = 75)
    new_population = Population()
    for generation in range(num_generations):
        selection_choices = ["RWS", "SUS", "tournament", "rank"]
        selection_operator = random.choice(selection_choices)
        
        if selection_operator == "RWS":
            new_population, average_fitness = RWS(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
            
        if selection_operator == "SUS":
            new_population, average_fitness = SUS(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
            
        if selection_operator == "tournament":
            new_population, average_fitness = tournament(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
            
        if selection_operator == "rank":
            new_population, average_fitness = rank(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
        
        population = new_population
        
        print(average_fitness)
        
        # set checkpoints in the evolution
        if generation % checkpoint_interval == 0:
            set_checkpoint(population, checkpoint_path = "./checkpoints")        
    return population
    
    
def set_checkpoint(population:Population, checkpoint_path:str) -> None:
    """
    This function sets a checkpoint during the run of the evolution
    
    Arguments:
        population:Population
            the population to be saved
        
            
    Returns:
        None
    """
    
    # check if the directory of the checkpoint exists
    # if it does not exists yet, create the direcotry
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)
        
    # 
    with open(f'./checkpoints/checkpoints{population.population_id}.pkl', 'wb') as output:
        pickle.dump(population, output, pickle.HIGHEST_PROTOCOL)
    
    
def load_checkpoint(checkpoint_path:str, train_set:list[pd.DataFrame], base_genome:Genome, seed_genome:Genome, fitness_func:callable, num_generations:int = 100, checkpoint_interval:int = 5):
    """
    Some text
    """
    with open(checkpoint_path, 'rb') as input:
        population = pickle.load(input)

    # population = run(train_set, base_genome, seed_genome, fitness_func, num_generations, checkpoint_interval)
    
    
def run_evolution(population:Population, train_set:list[pd.DataFrame], fitness_func:callable, num_generations:int = 100, checkpoint_interval:int = 5) -> Population:
    """
    This function simulates evolution through the population
    of genes
    
    Arguments:
        population:Population
            the population to be evolved
            
        train_set:list[pd.DataFrame]
            the list of training data to be used in evolving the population
            
        fitness_func:callable
            the fitness function to be used in assessing the performance of an
            individual in the population
        
        num_generations:int
           the number of generations the evolution should run
           
        checkpoint_interval:int
            the interval for saving a checkpoint in the evolution of the genomes
            
    Returns:
        population:Population
            the evolved population after n-generations
        
    """
    new_population = Population()
    
    # run the evolution
    for generation in range(num_generations):
        selection_choices = ["RWS", "SUS", "tournament", "rank"]
        selection_operator = random.choice(selection_choices)
        
        if selection_operator == "RWS":
            new_population, average_fitness = RWS(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
            
        if selection_operator == "SUS":
            new_population, average_fitness = SUS(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
            
        if selection_operator == "tournament":
            new_population, average_fitness = tournament(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
            
        if selection_operator == "rank":
            new_population, average_fitness = rank(population = population, fitness_func = fitness_func, series = train_set[random.randint(1, len(train_set))])
            new_population = crossover(population=new_population)
        
        population = new_population
        print(average_fitness)
        
        # set checkpoints in the evolution
        if generation % checkpoint_interval == 0:
            set_checkpoint(population, checkpoint_path = "./checkpoints")        
    return population