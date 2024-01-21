import copy
import itertools
from Genome import Genome

class Population():
    """
    This class provides details on the population object
    
    """
    population_id = itertools.count()
    
    
    def __init__(self):
        """
        This function initializes a gene object
        
        Arguments:
            self:
                the instance of the class
                
        Returns:
        """
        self.population_id = next(Population.population_id)
        self.population = list()
    
    def initialize_population(self, genome:Genome, num_genomes:int = 75):
        """
        This function initializes the first population of the genetic algorithm
        
        Arguments:
            self:
                the instance of the class
                
            genome:Genome
                the base genome where its structure will be the basis of the
                structure of all genomes in the population
            
            num_genomes:int
                the number of genomes to be produced in the population
                
        Returns:
            None
        """
        for _ in range(num_genomes):
            genome_copy = copy.deepcopy(genome)
            genome_copy.initialize_genome()
            self.population.append(copy.deepcopy(genome_copy))
        del genome_copy
            
    def seed_population(self, seed_genome:Genome, num_seeds:int = 25):
        """
        This funciton seeds the population with the seed_genome
        
        Arguments:
            self
                the instance of the class
                
            seed_genome:Genome
                the genome that will be used as the seed in the population
                
            num_seeds:int
                the number of seeds that will be inserted in the population7
        
        """
        for _ in range(num_seeds):
            self.population.append(copy.deepcopy(seed_genome))

    
    def select_genes(self):
        """
        This function is the selection phase of the genetic algorithm
        
        Arguments:
            population: list[gene]
                a list of genes to be evaluated and selected for the next generation
                
        Returns
            selected_population: list[gene]
                a list of genes selected to proceed to the next generation
        """
        pass
        
        
    