from Gene import Gene
import itertools

class Genome():
    """
    This class provides details on the genome object
    
    """
    genome_id = itertools.count()
    
    def __init__(self, gene_list:list[Gene] = list()):
        """
        Initializes the Genome class
        
        Arguments:
            self
                the instance of the class

            gene_list:list[Gene]
                a list containing gene objects
        
        Returns:
        """
        self.genome_id = next(Genome.genome_id)
        self.genome = gene_list
        self.genome_dict = dict()
        self.update_genome_dict()
        self.fitness = None
        
    def initialize_genome(self):
        """
        This function initializes the genome
        
        Arguments:
            self
                instance of the class
        Returns:
        """

        # loop through all the genes in the genome and initialize them individually
        for gene in self.genome:
            gene.initialize_gene()
        
        # update the ID of the genome
        self.genome_id = next(Genome.genome_id)
        
        # update the dictionary of the genome
        self.update_genome_dict()

    def update_genome_dict(self):
        """
        This function updates the genome dictionary

        Arguments:
            self
                instance of the class

        Returns:
        """
        # loop through all the genes in the genome and assign them to the genome dictionary
        for gene in self.genome:
            self.genome_dict[gene.name] = gene
            
    def mutate(self) -> None:
        """
        This function mutates the genome
        
        Arguments:
            None
        
        Returns:
            None
        """
        # attempt to mutate all genes in the genome
        for gene in self.genome:
            gene.mutate()
        
        # updated the genome if there have been mutated genes
        self.update_genome_dict()  
        
    def __str__(self) -> str:
        """
        This function provides information about the instance of the genome

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
        text = text + f"GENE_ID: {self.genome_id}\n"
        for gene in self.genome:
            text = text + gene.__str__()
            
        return text
    
    def __len__(self):
        return len(self.genome)