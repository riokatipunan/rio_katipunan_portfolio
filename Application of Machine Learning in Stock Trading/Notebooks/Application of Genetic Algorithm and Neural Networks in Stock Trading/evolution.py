import random
import os
from fitness import compute_average_population_fitness, fitness, compute_population_fitness, regime
from network import Network
from selection import keep_elites, selection
from mate import reproduce_population, reduce_population
from checkpoint import checkpoint
from statistics import mean
from speciation import adjust_population_fitness
from typing import MutableSequence, List
import pandas as pd


def run_evolution(population: MutableSequence[Network], 
                  window:int,
                  num_generations: int, 
                  train_set: List[pd.Series], 
                  checkpoint_filepath: str, 
                  checkpoint_interval: int = 1, 
                  starting_generation:int = 0):
    
    mutation_rate = 0.1
    historical_average_fitness = list()
    
    for _ in range(num_generations):
        
        # get a random sample from the list of training sets
        train_sample = random.choice(train_set)
        
        # compute the fitness of each NN
        # this returns a list of networks that has a correspinding fitness attribute
        population = compute_population_fitness(population = population,
                                                window = window,
                                                fitness = fitness,
                                                regime = regime, 
                                                train_set = train_sample)
        
    
        # adjust the fitness of the population based on the number of species
        population = adjust_population_fitness(population)
        
        # compute for the average fitness of the population
        average_fitness = compute_average_population_fitness(population)
        
        print(f'Generation: {_+starting_generation} -> {average_fitness:.2f}')        
        
        # append the average fitness in the history
        historical_average_fitness.append(average_fitness)
        
        
        # TODO transfer this to a separate function
        try:
            if len(historical_average_fitness) >=5:
                mean_historical_average_fitness = mean(historical_average_fitness[-5::])
                print(f'Mean historical average fitness: {mean_historical_average_fitness:.2f}')
                if average_fitness < mean_historical_average_fitness:
                    if mutation_rate <= 1:
                        mutation_rate += 0.05
                        print(f'Mutation rate: {mutation_rate:.2f}')
                else:
                    if mutation_rate > 0.1:
                        mutation_rate -= 0.05
                        print(f'Mutation rate: {mutation_rate:.2f}')
                    else:
                        mutation_rate = 0.1
                        print(f'Mutation rate: {mutation_rate:.2f}')
            else:
                mutation_rate = 0.1
                print(f'Mutation rate: {mutation_rate:.2f}')
        except:
            pass
        
        # keep the elites in the population
        elites = keep_elites(percentage_elites = 0.1, population = population)

        # adjust the fitness of the population based on the number of species
        population = adjust_population_fitness(population)

        # select the NNs to keep
        selected = selection(population = population)

        # join the elites and selected NNs
        new_population = elites + selected

        # mutation_rate = 1/(1 + num_generations)

        # reproduce the population
        new_population = reproduce_population(population=new_population, mutation_rate = mutation_rate)

        # trim the population
        new_population = reduce_population(population=new_population, remove_percentage=0.17)

        # assign new population to the old population 
        population = new_population

        if _ % checkpoint_interval == 0:
            # create filepath if it does not exists
            if not os.path.exists(checkpoint_filepath):
                os.makedirs(checkpoint_filepath)
            
            # save to checkpoint
            checkpoint(population = population, generation_number = _+starting_generation, checkpoint_filepath = checkpoint_filepath)
            
        # print(f'Generation: {_+starting_generation} -> {average_fitness}')        

    return elites