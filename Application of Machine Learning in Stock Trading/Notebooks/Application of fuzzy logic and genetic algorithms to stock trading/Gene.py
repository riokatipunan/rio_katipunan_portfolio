from typing import Union
import itertools
import random

class Gene():
    """
    This class provides details on a gene object
    """
    gene_id = itertools.count()

    def __init__(self, name:str, lower_bound:Union[int, float], upper_bound:Union[int, float], type:str, value: Union[int, float] = None):
        self.gene_id = next(Gene.gene_id)
        self.name = name
        self.value = value
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.type = type

    def initialize_gene(self):
        """
        This function initializes the gene
        
        Argument:
            self
                the instance of the class
        Returns:
        """

        if self.type == "int":
            self.value = random.randint(self.lower_bound, self.upper_bound)
        
        elif self.type == "float":
            self.value = random.uniform(self.lower_bound, self.upper_bound)
        
        elif self.type == "linear_membership":
            while True:
                left_node = random.randint(self.lower_bound, self.upper_bound)
                right_node = random.randint(left_node, self.upper_bound)
                if left_node < right_node:
                    break
            self.value = [left_node, right_node]
        
        elif self.type == "triangular_membership":
            while True:
                middle_node = random.randint(self.lower_bound, self.upper_bound)
                left_node = random.randint(self.lower_bound, middle_node)
                right_node = random.randint(middle_node, self.upper_bound)
                if left_node < middle_node and middle_node < right_node:
                    break
            self.value = [left_node, middle_node, right_node]

        elif self.type == "entry_condition":
            while True:
                short_condition = random.randint(self.lower_bound, self.upper_bound)
                long_condition = random.randint(short_condition, self.upper_bound)
                if short_condition < long_condition:
                    break
            self.value = [short_condition, long_condition]

    def mutate(self):
        """
        This function mutates the gene

        Arguments:
            self
                the instance of the class
        
        Returns:
        """
        mutation_distribution_choices = ["uniform", "normal"]
        mutation_distribution = random.choice(mutation_distribution_choices)

        if mutation_distribution is "uniform":
            self.initialize_gene()

        elif mutation_distribution is "normal":

            if self.type == "int":
                self.value = random.normal(self.value, )
            
            elif self.type == "float":
                self.value = random.uniform(self.lower_bound, self.upper_bound)
            
            elif self.type == "linear_membership":
                left_node = random.randint(self.lower_bound, self.upper_bound-1)
                right_node = random.randint(left_node + 1, self.upper_bound)
                self.value = [left_node, right_node]
            
            elif self.type == "triangular_membership":
                middle_node = random.randint(self.lower_bound+1, self.upper_bound-1)
                left_node = random.randint(self.lower_bound, middle_node-1)
                right_node = random.randint(middle_node+1, self.upper_bound)
                self.value = [left_node, middle_node, right_node]

            elif self.type == "entry_condition":
                short_condition = random.randint(self.lower_bound, self.upper_bound-1)
                long_condition = random.randint(short_condition, self.upper_bound)
                self.value = [short_condition, long_condition]

    def __str__(self) -> str:
        """
        This function provides details of the instance of the class

        Arguments:
            self
                the instance of the class
        
        Returns:
            text:str
                a text string containing some information on the instance of the class
        """

        text = str()
        text = text + f"Gene name: {self.name}\nValue: {self.value}\n\n"
        return text