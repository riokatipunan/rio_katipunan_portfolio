import random
import os
from fitness import fitness, compute_population_fitness, regime
from selection import keep_elites, selection
from mate import reproduce_population, reduce_population
from checkpoint import checkpoint


def run_evolution(population, 
                  num_generations, 
                  train_set, 
                  checkpoint_filepath, 
                  checkpoint_interval = 1, 
                  starting_generation = 0):
    
    for _ in range(num_generations):
        
        train_sample = random.choice(train_set)
        # compute the fitness of each NN
        population = compute_population_fitness(population = population,
                                                fitness = fitness,
                                                regime = regime, 
                                                train_set = train_sample)
        # keep the elites in the population
        elites = keep_elites(percentage_elites = 0.1, population = population)

        # select the NNs to keep
        selected = selection(population = population)

        # join the elites and selected NNs
        new_population = elites + selected

        # reproduce the population
        new_population = reproduce_population(population=new_population)

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

    return population