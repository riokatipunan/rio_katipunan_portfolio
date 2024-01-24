import copy
import itertools
from Genome import Genome

class Population():
    """
    This class provides details on the population object
    
    """
    population_id = itertools.count()
    
    
    def __init__(self, genome_list:list[Genome] | None = None) -> None:
        """
        This function initializes a gene object
        
        Arguments:
            self:
                the instance of the class
                
        Returns:
        """
        self.population_id = next(Population.population_id)
        if genome_list is not None and len(genome_list) > 0:
            self.population = genome_list
        else:
            self.population = list()
    
    def add_and_initialize_to_population(self, base_genome:Genome, num_genomes:int = 75):
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
            base_genome_copy = Genome(base_genome.genome)
            base_genome_copy.initialize_genome()
            self.population.append(copy.deepcopy(base_genome_copy))
        del base_genome_copy
            
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
            seed_genome_copy = Genome(seed_genome.genome)
            self.population.append(copy.deepcopy(seed_genome_copy))

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
    
    def _isvalid_genome(genome:Genome) -> bool:
        """
        This method checks if a genome is valid or not
        
        Arguments:
            genome:Genome
                the genome to be check if it is a valid genome or not
        Returns
            isvalid:bool
        """
        
    def __len__(self) -> int:
        """
        This function returns the number of genomes in the population
        Arguments:
            self:
                instance of the class
                
        Returns:
            num_population:
                the number of genomes in the population
        """
        
        
        return len(self.population)
    
    def __str__(self):
        """
        This function provides information about the instance of the population

        Arguments:
            self
                instance of the class

        Returns:
            text:str
                a text string containing some information about the genome instance
        """

        # loop through all the genes in the genome and provide the 
        # gene name and gene value of the gene
        text = str()
        text = f"Population {self.population_id} has {len(self.population)} genome/s\n"
        text = text + "It has the following gene/s:\n"
        for genome in self.population:
            text = text + genome.__str__()
            
        return text
        
        
        
        
        
        
        
    