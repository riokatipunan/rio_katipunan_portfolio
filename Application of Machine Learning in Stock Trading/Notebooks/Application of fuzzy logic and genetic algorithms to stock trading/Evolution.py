from Gene import Gene
from Genome import Genome
from Population import Population
from Crossover import single_point, two_point, uniform, linear, SBX, crossover
from Fitness import evaluate_fitness
from Selection import RWS, SUS, tournament, rank
import random
import pandas as pd
import os
import pickle


class Evolution():
    """
    Some text
    """
    
    def __init__(self, population:Population = None) -> None:
        """
        Some text
        """
        if population is None:
            self.population = Population
        else:
            self.population = population
        
    def define_train_set(self, train_set:pd.DataFrame):
        """
        Some text
        """
        self.train_set = train_set
        
    def initialize_population(self, base_genome:Genome, seed_genome:Genome):
        """
        Some text
        """
        self.population.seed_population(seed_genome = seed_genome, num_seeds = 25)
        self.population.add_and_initialize_to_population(base_genome = base_genome, num_genomes = 75)        
        
    def define_fitness_func(self, fitness_func:callable):
        """
        Some text
        """
        self.fitness_func = fitness_func
        
    def define_checkpoint_path(self, checkpoint_path:str = "./checkpoint"):
        self.checkpoint_path = checkpoint_path
    
    def run(self, num_generations:int = 100,  checkpoint_interval:int = 5, checkpoint_path:str = "./checkpoints" ):
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
        self.checkpoint_path = checkpoint_path
        new_population = Population()
        for generation in range(num_generations):
            
            print(f"Generation {generation}")
            selection_choices = ["RWS", "SUS", "tournament", "rank"]
            selection_operator = random.choice(selection_choices)
            
            if selection_operator == "RWS":
                new_population, average_fitness = RWS(population = self.population, fitness_func = self.fitness_func, series = self.train_set[random.randint(1, len(self.train_set))])
                new_population = crossover(population=new_population)
                
            if selection_operator == "SUS":
                new_population, average_fitness = SUS(population = self.population, fitness_func = self.fitness_func, series = self.train_set[random.randint(1, len(self.train_set))])
                new_population = crossover(population=new_population)
                
            if selection_operator == "tournament":
                new_population, average_fitness = tournament(population = self.population, fitness_func = self.fitness_func, series = self.train_set[random.randint(1, len(self.train_set))])
                new_population = crossover(population=new_population)
                
            if selection_operator == "rank":
                new_population, average_fitness = rank(population = self.population, fitness_func = self.fitness_func, series = self.train_set[random.randint(1, len(self.train_set))])
                new_population = crossover(population=new_population)
            
            self.population = new_population
            
            print(f"fitness of generation {generation}:\t{average_fitness}")
            
            # set checkpoints in the evolution
            if generation % checkpoint_interval == 0:
                self._set_checkpoint()        
        
        return self.population
        
    def _set_checkpoint(self) -> None:
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
        if not os.path.exists(self.checkpoint_path):
            os.makedirs(self.checkpoint_path)
            
        # write the information of the population object to the directory
        with open(f'./checkpoints/checkpoint{self.population.population_id}.pkl', 'wb') as output:
            pickle.dump(self.population, output, 0)
        
        
    def load_checkpoint(self, checkpoint_path:str):
        """
        Some text
        """
        with open(checkpoint_path, 'rb') as input:
            self.population = pickle.load(input)
            
        return self.population
    