from typing import Union
import itertools
import random
import numpy as np

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

    def mutate(self, mutation_rate = 0.1) -> None:
        """
        This function mutates the gene

        Arguments:
            self
                the instance of the class
        
        Returns:
        """
        probability_of_mutation = random.uniform(0,1)
        if probability_of_mutation <=  mutation_rate:
            mutation_type_choices = ["uniform", "normal"]
            mutation_type = random.choice(mutation_type_choices)
            print(f"Gene {self.gene_id} with gene name: {self.name} is being mutated")
            print(f"Mutation type is {mutation_type}")
            if mutation_type is "uniform":
                self.initialize_gene()

            elif mutation_type is "normal":

                if self.type == "int":
                    loop_counter = 0
                    while True:
                        loop_counter += 1
                        self.value = np.random.normal(loc = self.value)
                        if self.value > self.lower_bound and self.value < self.upper_bound:
                            break

                        # if the code above takes too long,
                        # degenerate into uniform mutation
                        if loop_counter > 100:
                            self.initialize_gene()
                            break
                
                elif self.type == "float":
                    loop_counter = 0
                    while True:
                        loop_counter += 1
                        self.value = np.random.normal(loc = self.value)
                        if self.value > self.lower_bound and self.value < self.upper_bound:
                            break

                        # if the code above takes too long,
                        # degenerate into uniform mutation
                        if loop_counter > 100:
                            self.initialize_gene()
                            break

                elif self.type == "linear_membership":
                    loop_counter = 0
                    while True:
                        loop_counter += 1
                        left_node = np.random.normal(loc = self.value[0])
                        right_node = np.random.normal(loc = self.value[1])
                        self.value = [left_node, right_node]
                        condition1 = left_node > self.lower_bound and left_node < self.upper_bound
                        condition2 = right_node > self.lower_bound and right_node < self.upper_bound
                        condition3 = left_node < right_node
                        if condition1 and condition2 and condition3:
                            break
                        # if the above code takes too long, 
                        # degenerate to uniform initialization
                        if loop_counter > 100:
                            self.initialize_gene()
                            break

                
                elif self.type == "triangular_membership":
                    loop_counter = 0 
                    while True:
                        loop_counter += 1
                        left_node = np.random.normal(loc = self.value[0])
                        middle_node = np.random.normal(loc = self.value[1])
                        right_node = np.random.normal(loc = self.value[2])
                        self.value = [left_node, middle_node, right_node]
                        condition1 = left_node > self.lower_bound and left_node < self.upper_bound
                        condition2 = middle_node > self.lower_bound and middle_node < self.upper_bound
                        condition3 = right_node > self.lower_bound and right_node < self.upper_bound
                        condition4 = left_node < middle_node and middle_node < right_node
                        if condition1 and condition2 and condition3 and condition4:
                            break

                        # if the above code takes too long, 
                        # degenerate to uniform initialization
                        if loop_counter > 100:
                            self.initialize_gene()
                            break

                elif self.type == "entry_condition":
                    loop_counter = 0
                    while True:
                        loop_counter += 1
                        short_condition = np.random.normal(loc = self.value[0])
                        long_condition = np.random.normal(loc = self.value[1])
                        self.value = [short_condition, long_condition]
                        condition1 = short_condition > self.lower_bound and short_condition < self.upper_bound
                        condition2 = long_condition > self.lower_bound and long_condition < self.upper_bound
                        condition3 = left_node < right_node
                        if condition1 and condition2 and condition3:
                            break
                        # if the above code takes too long, 
                        # degenerate to uniform initialization
                        if loop_counter > 100:
                            self.initialize_gene()
                            break
        else:
            pass

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