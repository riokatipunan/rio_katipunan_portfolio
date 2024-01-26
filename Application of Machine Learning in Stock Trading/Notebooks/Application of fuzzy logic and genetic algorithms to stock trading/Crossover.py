import math
import random
import copy
from Gene import Gene
from Genome import Genome
from Population import Population

def single_point(genome1:Genome, genome2:Genome) -> (Genome, Genome):
    """
    This function performs a single point crossover between two genomes; 
    this function returns two offsprings.
    
    Arguments:
        genome1: Genome
            a genome object to be crossed over to genome2
        
        genome2: Genome
            a genome object to be crossed over to genome1
            
    Returns:
        offspring1, offspring2: Genome, Genome
            the offspring due to the crossover of genome1 and genome2;
    """
    
    # initialize the offspring
    offspring1 = list()
    offspring2 = list()
    
    # identify the crossover point
    crossover_point = random.randint(1, len(genome1.genome)-1)
    
    # at the crossoverpoint, swap the genes of the two parent genomes
    for i in range(len(genome1.genome)):
        if i < crossover_point:
            offspring1.append(copy.deepcopy(genome1.genome[i]))
            offspring2.append(copy.deepcopy(genome2.genome[i]))
        else:
            offspring1.append(copy.deepcopy(genome2.genome[i]))
            offspring2.append(copy.deepcopy(genome1.genome[i]))
    
    # instantiate the offsprings as genomes
    offspring1 = Genome(offspring1)
    offspring2 = Genome(offspring2)
    
    # apply mutation to the offsprings
    offspring1.mutate()
    offspring2.mutate()
    
    return offspring1, offspring2

def two_point(genome1:Genome, genome2:Genome) -> (Genome, Genome):
    """
    This function performs a two-point crossover between two genomes; 
    this function returns two offsprings.
    
    Arguments:
        genome1: Genome
            a genome object to be crossed over to genome2
        
        genome2: Genome
            a genome object to be crossed over to genome1
            
    Returns:
        offspring1, offspring2: Genome, Genome
            the offspring due to the crossover of genome1 and genome2
    """
    # instantiate the offsprings as lists
    offspring1 = list()
    offspring2 = list()
    
    # identify the two crossoverpoints
    #  the code below checks and ensures that the first crossover point
    # is less than the second crossoverpoint
    while True:
        crossover_point1 = random.randint(1, len(genome1.genome)-1)
        crossover_point2 = random.randint(1, len(genome1.genome)-1)
        
        if crossover_point1 < crossover_point2:
            break
    
    # do the two-point crossover
    for i in range(len(genome1.genome)):
        if i < crossover_point1:
            offspring1.append(copy.deepcopy(genome1.genome[i]))
            offspring2.append(copy.deepcopy(genome2.genome[i]))
        elif (i > crossover_point1) and (i < crossover_point2):
            offspring1.append(copy.deepcopy(genome2.genome[i]))
            offspring2.append(copy.deepcopy(genome1.genome[i]))
        else:
            offspring1.append(copy.deepcopy(genome1.genome[i]))
            offspring2.append(copy.deepcopy(genome2.genome[i]))
    
    # instantiate the offspring as a genome
    offspring1 = Genome(offspring1)
    offspring2 = Genome(offspring2)
    
    return offspring1, offspring2
    
def uniform(genome1:Genome, genome2:Genome) -> (Genome, Genome):
    """
    This function performs a uniform crossover between two genomes; 
    this function returns two offsprings.
    
    Arguments:
        genome1: Genome
            a genome object to be crossed over to genome2
        
        genome2: Genome
            a genome object to be crossed over to genome1
            
    Returns:
        offspring: Genome
            the offspring due to the crossover of genome1 and genome2;
    """
    # instantiate the offsprings as a list
    offspring1 = list()
    offspring2 = list()
    
    # do uniform crossover
    for i in range(len(genome1.genome)):
        if random.uniform(0,1) >=0.5:
            offspring1.append(copy.deepcopy(genome1.genome[i]))
            offspring2.append(copy.deepcopy(genome2.genome[i]))
        else:
            offspring1.append(copy.deepcopy(genome2.genome[i]))
            offspring2.append(copy.deepcopy(genome1.genome[i]))
    
    # instatiate the offsprings as genomes
    offspring1 = Genome(offspring1)
    offspring2 = Genome(offspring2)

    # apply mutation to the offsprings
    offspring1.mutate()
    offspring2.mutate()
    
    return offspring1, offspring2
    
def linear(genome1:Genome, genome2:Genome) -> Genome:
    """
    This function performs a linear crossover between two genomes; 
    this function returns one offspring.
    
    Arguments:
        genome1: Genome
            a genome object to be crossed over to genome2
        
        genome2: Genome
            a genome object to be crossed over to genome1
            
    Returns:
        offspring: Genome
            the offspring due to the crossover of genome1 and genome2;
    """
    # instantiate the offspring as a list
    offspring = list()
    
    # loop through the genome of the parents and do linear crossover
    for i in range(len(genome1.genome)):
        
        # determine the scaling factors for the linear crossover
        alpha = random.uniform(0,1)
        beta = random.uniform(0,1)
        
        # the next block of code checks the types of genes in the genome 
        # and applies the appropriate crossover operation
        if genome1.genome[i].type is "int":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"
            
            # perform linear crossover
            offspring_value = math.floor(((alpha * genome1.genome[i].value) + (beta * genome2.genome[i].value))/(alpha + beta))
            
            # instantiate the offspring gene
            offspring_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = offspring_value)
            
            # append the offspring gene in the offspring genome
            offspring.append(copy.deepcopy(offspring_gene))
            continue
            
        elif genome1.genome[i].type is "float":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"
            
            # perform linear crossover
            offspring_value = ((alpha * genome1.genome[i].value) + (beta * genome2.genome[i].value))/(alpha+beta)
            
            # instantiate the offspring gene
            offspring_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = offspring_value)
            
            # append the offspring gene in the offspring genome
            offspring.append(copy.deepcopy(offspring_gene))
            continue

        elif genome1.genome[i].type is "linear_membership":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"  
            
            # instantiate the left and right nodes of the offspring
            offspring_left_node = 0
            offspring_right_node = 0

            # initialize loop counter
            loop_counter = 0
            
            # loop until offspring left node is less than the offspring right node
            while True:
                # increase the loop counter
                loop_counter += 1
                
                # perform linear crossover on the left and right nodes to produce an offspring
                offspring_left_node = ((alpha * genome1.genome[i].value[0]) + (beta * genome2.genome[i].value[0]))/(alpha + beta)
                offspring_right_node = ((alpha * genome1.genome[i].value[1]) + (beta * genome2.genome[i].value[1]))/(alpha + beta)
                
                # check for break condition
                if offspring_left_node < offspring_right_node:
                    break
                
                # if while loop takes to long, degenerate into uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring_left_node = genome1.genome[i].value[0]
                    else:
                        offspring_left_node = genome2.genome[i].value[0]
                    
                    if random.uniform(0,1) > 0.5:
                        offspring_right_node = genome1.genome[i].value[1]
                    else:
                        offspring_right_node = genome2.genome[i].value[1]
                    break
                        
            # instantiate the offspring gene
            offspring_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring_left_node, offspring_right_node]) 
            
            # append the offspring gene in the offspring genome
            offspring.append(copy.deepcopy(offspring_gene))
            continue 
            
        elif genome1.genome[i].type is "triangular_membership":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"  
            
            # initialize the left, middle, and right node values of the offspring
            offspring_left_node = 0
            offspring_middle_node = 0
            offspring_right_node = 0
            
            # initialize loop counter
            loop_counter = 0
            
            # loop until the condition left_node < middle_node < right_node is met
            while True:
                # increase loop counter
                loop_counter += 1

                # perform linear crossover on the left, middle, and right nodes
                offspring_left_node = ((alpha * genome1.genome[i].value[0]) + (beta * genome2.genome[i].value[0]))/(alpha + beta)
                offspring_middle_node = ((alpha * genome1.genome[i].value[1]) + (beta * genome2.genome[i].value[1]))/(alpha + beta)
                offspring_right_node = ((alpha * genome1.genome[i].value[2]) + (beta * genome2.genome[i].value[2]))/(alpha + beta)
                
                # check for break condition
                condition = (offspring_left_node < offspring_middle_node) and (offspring_middle_node < offspring_right_node)
                if condition:
                    break
                
                # if while loop takes to long, degenerate into uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring_left_node = genome1.genome[i].value[0]
                    else:
                        offspring_left_node = genome2.genome[i].value[0]
                    
                    if random.uniform(0,1) > 0.5:
                        offspring_middle_node = genome1.genome[i].value[1]
                    else:
                        offspring_middle_node = genome2.genome[i].value[1]                         
                    
                    if random.uniform(0,1) > 0.5:
                        offspring_right_node = genome1.genome[i].value[2]
                    else:
                        offspring_right_node = genome2.genome[i].value[2]
                    break                        
        
            # instantiate the offspring gene
            offspring_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring_left_node, offspring_middle_node, offspring_right_node]) 
            
            # append the offspring gene in the offspring genome
            offspring.append(copy.deepcopy(offspring_gene))
            continue 

        elif genome1.genome[i].type is "entry_condition":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"  
            
            # loop until offspring left node is less than the offspring right node
            offspring_left_node = 0
            offspring_right_node = 0
            
            # initialize loop counter
            loop_counter = 0

            # # loop until the condition left_node < right_node is met
            while True:
                # increase loop counter
                loop_counter += 1

                # perform linear crossover on the left and right nodes
                offspring_left_node = ((alpha * genome1.genome[i].value[0]) + (beta * genome2.genome[i].value[0]))/(alpha + beta)      
                offspring_right_node = ((alpha * genome1.genome[i].value[1]) + (beta * genome2.genome[i].value[1]))/(alpha + beta)
                
                # check for break condition
                if offspring_left_node < offspring_right_node:
                    break
                
                # if while loop takes to long, degenerate into uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring_left_node = genome1.genome[i].value[0]
                    else:
                        offspring_left_node = genome2.genome[i].value[0]
                    
                    if random.uniform(0,1) > 0.5:
                        offspring_right_node = genome1.genome[i].value[1]
                    else:
                        offspring_right_node = genome2.genome[i].value[1]
                    break                        

            # instantiate the offspring gene
            offspring_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring_left_node, offspring_right_node]) 
            
            # append the offspring gene in the offspring genome
            offspring.append(copy.deepcopy(offspring_gene))
            continue
    
    # instantiate the offsprings as a genome object
    offspring1 = Genome(offspring)
    offspring2 = Genome(offspring)

    # mutate the offsprings
    offspring1.mutate()
    offspring2.mutate()

    return offspring1, offspring2
    
def SBX(genome1:Genome, genome2:Genome) -> (Genome, Genome):
    """
    Simulated Binary Crossover
    
    This function performs a simulated binary crossover between two genomes; 
    this function returns two offsprings.
    
    Arguments:
        genome1: Genome
            a genome object to be crossed over to genome2
        
        genome2: Genome
            a genome object to be crossed over to genome1
            
    Returns:
        offspring: Genome
            the offspring due to the crossover of genome1 and genome2;
    """

    # initialize the offsprings as list
    offspring1 = list()
    offspring2 = list()
    
    # loop through each gene in the genome of the parents
    for i in range(len(genome1.genome)):
        if genome1.genome[i].type is "int":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"
            
            # initialize loop counter
            loop_counter = 0

            # loop until break condition is met
            while True:
                # increase loop counter
                loop_counter += 1

                # initialize SBX factors
                u = random.uniform(0,1)
                n = random.choice([2,3,4,5])
                if u <= 0.5:
                    beta = (2*u)**(1/(n+1))
                else:
                    beta = (1/(2*(1-u)))**(1/(n+1))
                
                # compute for the values of the offsprings
                offspring1_value = math.floor(0.5*(((1+beta)*genome1.genome[i].value) + ((1-beta)*genome2.genome[i].value)))
                offspring2_value = math.floor(0.5*(((1+beta)*genome2.genome[i].value) + ((1-beta)*genome1.genome[i].value)))
                
                condition1 = genome1.genome[i].lower_bound < offspring1_value
                condition2 = genome1.genome[i].upper_bound > offspring1_value
                condition3 = genome1.genome[i].lower_bound < offspring2_value
                condition4 = genome1.genome[i].upper_bound > offspring2_value                    
                if condition1 and condition2 and condition3 and condition4:
                    break
                
                # if SBX takes too long, degenerate to uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring1_value = genome1.genome[i].value
                    else:
                        offspring1_value = genome2.genome[i].value
                    
                    if random.uniform(0,1) > 0.5:
                        offspring2_value = genome1.genome[i].value
                    else:
                        offspring2_value = genome2.genome[i].value
                    break                                      

            # instantiate the offsprings genes
            offspring1_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = offspring1_value)
            offspring2_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = offspring2_value)                

            # append the offspring gene in the offspring genome
            offspring1.append(copy.deepcopy(offspring1_gene))
            offspring2.append(copy.deepcopy(offspring2_gene))
            continue
        
        elif genome1.genome[i].type is "float":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"
        
            loop_counter = 0
            while True: 
                loop_counter += 1               
                u = random.uniform(0,1)
                n = random.choice([2,3,4,5])
                if u <= 0.5:
                    beta = (2*u)**(1/(n+1))
                else:
                    beta = (1/(2*(1-u)))**(1/(n+1))
                
                # compute for the values of the offsprings
                offspring1_value = 0.5*(((1+beta)*genome1.genome[i].value) + ((1-beta)*genome2.genome[i].value))
                offspring2_value = 0.5*(((1+beta)*genome2.genome[i].value) + ((1-beta)*genome1.genome[i].value))

                condition1 = genome1.genome[i].lower_bound < offspring1_value
                condition2 = genome1.genome[i].upper_bound > offspring1_value
                condition3 = genome1.genome[i].lower_bound < offspring2_value
                condition4 = genome1.genome[i].upper_bound > offspring2_value                    
                if condition1 and condition2 and condition3 and condition4:
                    break
                
                # if SBX takes too long, degenerate to uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring1_value = genome1.genome[i].value
                    else:
                        offspring1_value = genome2.genome[i].value
                    
                    if random.uniform(0,1) > 0.5:
                        offspring2_value = genome1.genome[i].value
                    else:
                        offspring2_value = genome2.genome[i].value
                    break                      
                
            # instantiate the offsprings genes
            offspring1_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = offspring1_value)
            offspring2_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = offspring2_value)                

            # append the offspring gene in the offspring genome
            offspring1.append(copy.deepcopy(offspring1_gene))
            offspring2.append(copy.deepcopy(offspring2_gene))
            continue
        
        elif genome1.genome[i].type is "linear_membership":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"
        
            loop_counter = 0
        
            while True:
                loop_counter += 1
                u = random.uniform(0,1)
                n = random.choice([2,3,4,5])
                if u <= 0.5:
                    beta = (2*u)**(1/(n+1))
                else:
                    beta = (1/(2*(1-u)))**(1/(n+1))
                
                # compute for the values of the offsprings
                offspring1_left_node_value = 0.5*(((1+beta)*genome1.genome[i].value[0]) + ((1-beta)*genome2.genome[i].value[0]))
                offspring2_left_node_value = 0.5*(((1+beta)*genome2.genome[i].value[0]) + ((1-beta)*genome1.genome[i].value[0]))

                offspring1_right_node_value = 0.5*(((1+beta)*genome1.genome[i].value[1]) + ((1-beta)*genome2.genome[i].value[1]))
                offspring2_right_node_value = 0.5*(((1+beta)*genome2.genome[i].value[1]) + ((1-beta)*genome1.genome[i].value[1]))

                # check for exit
                condition1 = offspring1_left_node_value < offspring1_right_node_value
                condition2 = (genome1.genome[i].lower_bound < offspring1_left_node_value) and (genome1.genome[i].upper_bound > offspring1_left_node_value)
                condition3 = (genome1.genome[i].lower_bound < offspring1_right_node_value) and (genome1.genome[i].upper_bound > offspring1_right_node_value)
                condition4 = offspring2_left_node_value < offspring2_right_node_value
                condition5 = (genome1.genome[i].lower_bound < offspring2_left_node_value)and(genome1.genome[i].upper_bound > offspring2_left_node_value)
                condition6 = (genome1.genome[i].lower_bound < offspring2_right_node_value)and(genome1.genome[i].upper_bound > offspring2_right_node_value)
                condition7 = condition1 and condition2 and condition3
                condition8 = condition4 and condition5 and condition6
                if condition7 and condition8:
                    break
                
                # if while loop takes to long, degenerate into uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring1_left_node_value = genome1.genome[i].value[0]
                    else:
                        offspring1_left_node_value = genome2.genome[i].value[0]                         
                    
                    if random.uniform(0,1) > 0.5:
                        offspring1_right_node_value = genome1.genome[i].value[1]
                    else:
                        offspring1_right_node_value = genome2.genome[i].value[1]
                        
                    if random.uniform(0,1) > 0.5:
                        offspring2_left_node_value = genome1.genome[i].value[0]
                    else:
                        offspring2_left_node_value = genome2.genome[i].value[0]                         
                    
                    if random.uniform(0,1) > 0.5:
                        offspring2_right_node_value = genome1.genome[i].value[1]
                    else:
                        offspring2_right_node_value = genome2.genome[i].value[1]                            
                    break                        

            # instantiate the offsprings genes
            offspring1_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring1_left_node_value, offspring1_right_node_value])
            offspring2_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring2_left_node_value, offspring2_right_node_value])                

            # append the offspring gene in the offspring genome
            offspring1.append(copy.deepcopy(offspring1_gene))
            offspring2.append(copy.deepcopy(offspring2_gene))
            continue
        
        elif genome1.genome[i].type is "triangular_membership":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"
        
            loop_counter = 0
            while True:
                loop_counter += 1
                u = random.uniform(0,1)
                n = random.choice([2,3,4,5])
                if u <= 0.5:
                    beta = (2*u)**(1/(n+1))
                else:
                    beta = (1/(2*(1-u)))**(1/(n+1))
                
                # compute for the values of the offsprings
                offspring1_left_node_value = 0.5*(((1+beta)*genome1.genome[i].value[0]) + ((1-beta)*genome2.genome[i].value[0]))
                offspring2_left_node_value = 0.5*(((1+beta)*genome2.genome[i].value[0]) + ((1-beta)*genome1.genome[i].value[0]))

                offspring1_middle_node_value = 0.5*(((1+beta)*genome1.genome[i].value[1]) + ((1-beta)*genome2.genome[i].value[1]))
                offspring2_middle_node_value = 0.5*(((1+beta)*genome2.genome[i].value[1]) + ((1-beta)*genome1.genome[i].value[1]))
                
                offspring1_right_node_value = 0.5*(((1+beta)*genome1.genome[i].value[2]) + ((1-beta)*genome2.genome[i].value[2]))
                offspring2_right_node_value = 0.5*(((1+beta)*genome2.genome[i].value[2]) + ((1-beta)*genome1.genome[i].value[2]))                    

                # check for exit
                condition1 = (offspring1_left_node_value < offspring1_middle_node_value) and (offspring1_middle_node_value < offspring1_right_node_value) 
                condition2 = (genome1.genome[i].lower_bound < offspring1_left_node_value) and (genome1.genome[i].upper_bound > offspring1_left_node_value)
                condition3 = (genome1.genome[i].lower_bound < offspring1_middle_node_value) and (genome1.genome[i].upper_bound > offspring1_middle_node_value)
                condition4 = (genome1.genome[i].lower_bound < offspring1_right_node_value) and (genome1.genome[i].upper_bound > offspring1_right_node_value) 
                condition5 = (offspring2_left_node_value < offspring2_middle_node_value) and (offspring2_middle_node_value < offspring2_right_node_value) 
                condition6 = (genome1.genome[i].lower_bound < offspring2_left_node_value) and (genome1.genome[i].upper_bound > offspring2_left_node_value)
                condition7 = (genome1.genome[i].lower_bound < offspring2_middle_node_value) and (genome1.genome[i].upper_bound > offspring2_middle_node_value)
                condition8 = (genome1.genome[i].lower_bound < offspring2_right_node_value) and (genome1.genome[i].upper_bound > offspring2_right_node_value)                    
                condition9 = condition1 and condition2 and condition3 and condition4
                condition10 = condition5 and condition6 and condition7 and condition8
                
                if condition9 and condition10:
                    break
                
                # if while loop takes to long, degenerate into uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring1_left_node_value = genome1.genome[i].value[0]
                    else:
                        offspring1_left_node_value = genome2.genome[i].value[0]                         

                    if random.uniform(0,1) > 0.5:
                        offspring1_middle_node_value = genome1.genome[i].value[1]
                    else:
                        offspring1_middle_node_value = genome2.genome[i].value[1]
                    
                    if random.uniform(0,1) > 0.5:
                        offspring1_right_node_value = genome1.genome[i].value[2]
                    else:
                        offspring1_right_node_value = genome2.genome[i].value[2]
                        
                    if random.uniform(0,1) > 0.5:
                        offspring2_left_node_value = genome1.genome[i].value[0]
                    else:
                        offspring2_left_node_value = genome2.genome[i].value[0]                         

                    if random.uniform(0,1) > 0.5:
                        offspring2_middle_node_value = genome1.genome[i].value[1]
                    else:
                        offspring2_middle_node_value = genome2.genome[i].value[1]
                    
                    if random.uniform(0,1) > 0.5:
                        offspring2_right_node_value = genome1.genome[i].value[2]
                    else:
                        offspring2_right_node_value = genome2.genome[i].value[2]                            
                    break                        

            # instantiate the offsprings genes
            offspring1_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring1_left_node_value, offspring1_middle_node_value, offspring1_right_node_value])
            offspring2_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring2_left_node_value, offspring2_middle_node_value, offspring2_right_node_value])                

            # append the offspring gene in the offspring genome
            offspring1.append(copy.deepcopy(offspring1_gene))
            offspring2.append(copy.deepcopy(offspring2_gene))
            continue

        elif genome1.genome[i].type is "entry_condition":
            # check that both genes are the same in terms of type and name
            assert genome1.genome[i].name == genome2.genome[i].name, "The name genes of the genome should be the same"
            assert genome1.genome[i].type == genome2.genome[i].type, "The type genes of the genome should be the same"
        
            loop_counter = 0
        
            while True:
                loop_counter += 1
                u = random.uniform(0,1)
                n = random.choice([2,3,4,5])
                if u <= 0.5:
                    beta = (2*u)**(1/(n+1))
                else:
                    beta = (1/(2*(1-u)))**(1/(n+1))
                
                # compute for the values of the offsprings
                offspring1_left_node_value = 0.5*(((1+beta)*genome1.genome[i].value[0]) + ((1-beta)*genome2.genome[i].value[0]))
                offspring2_left_node_value = 0.5*(((1+beta)*genome2.genome[i].value[0]) + ((1-beta)*genome1.genome[i].value[0]))

                offspring1_right_node_value = 0.5*(((1+beta)*genome1.genome[i].value[1]) + ((1-beta)*genome2.genome[i].value[1]))
                offspring2_right_node_value = 0.5*(((1+beta)*genome2.genome[i].value[1]) + ((1-beta)*genome1.genome[i].value[1]))

                # check for exit
                # check for exit
                condition1 = offspring1_left_node_value < offspring1_right_node_value
                condition2 = (genome1.genome[i].lower_bound < offspring1_left_node_value) and (genome1.genome[i].upper_bound > offspring1_left_node_value)
                condition3 = (genome1.genome[i].lower_bound < offspring1_right_node_value) and (genome1.genome[i].upper_bound > offspring1_right_node_value)
                condition4 = offspring2_left_node_value < offspring2_right_node_value
                condition5 = (genome1.genome[i].lower_bound < offspring2_left_node_value)and(genome1.genome[i].upper_bound > offspring2_left_node_value)
                condition6 = (genome1.genome[i].lower_bound < offspring2_right_node_value)and(genome1.genome[i].upper_bound > offspring2_right_node_value)
                condition7 = condition1 and condition2 and condition3
                condition8 = condition4 and condition5 and condition6
                if condition7 and condition8:
                    break
                
                # if while loop takes to long, degenerate into uniform crossover
                if loop_counter > 100:
                    if random.uniform(0,1) > 0.5:
                        offspring1_left_node_value = genome1.genome[i].value[0]
                    else:
                        offspring1_left_node_value = genome2.genome[i].value[0]                         
                    
                    if random.uniform(0,1) > 0.5:
                        offspring1_right_node_value = genome1.genome[i].value[1]
                    else:
                        offspring1_right_node_value = genome2.genome[i].value[1]
                        
                    if random.uniform(0,1) > 0.5:
                        offspring2_left_node_value = genome1.genome[i].value[0]
                    else:
                        offspring2_left_node_value = genome2.genome[i].value[0]                         
                    
                    if random.uniform(0,1) > 0.5:
                        offspring2_right_node_value = genome1.genome[i].value[1]
                    else:
                        offspring2_right_node_value = genome2.genome[i].value[1]                            
                    break                        

            # instantiate the offsprings genes
            offspring1_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring1_left_node_value, offspring1_right_node_value])
            offspring2_gene = Gene(name = genome1.genome[i].name,
                                    lower_bound = genome1.genome[i].lower_bound,
                                    upper_bound = genome1.genome[i].upper_bound,
                                    type = genome1.genome[i].type,
                                    value = [offspring2_left_node_value, offspring2_right_node_value])                

            # append the offspring gene in the offspring genome
            offspring1.append(copy.deepcopy(offspring1_gene))
            offspring2.append(copy.deepcopy(offspring2_gene))
            continue
    
    
    offspring1 = Genome(offspring1)
    offspring2 = Genome(offspring2)
    offspring1.mutate()
    offspring2.mutate()
    return offspring1, offspring2

def crossover(population:Population, num_crossover:int =  25) -> Population:
    """
    This function is a wrapper for all the crossover operators
    as provided above.

    Arguments:
        population:Population
            the population to be 
    """
    new_population = list()
    population_list = population.population
    CROSSOVER_OPERATORS = ["single_point", "two_point", "uniform", "linear", "SBX"]
    
    for i in range(num_crossover):

        # choose two random parents and let them perform crossover
        parent1_idx = random.randint(0, len(population.population)-1)
        parent2_idx = random.randint(0, len(population.population)-1)
        
        # randomly choose a crossover operator
        crossover_type = random.choice(CROSSOVER_OPERATORS)
        
        if crossover_type == "single_point":
            offspring1, offspring2 = single_point(population.population[parent1_idx], population.population[parent2_idx])
        
        if crossover_type == "two_point":
            offspring1, offspring2 = two_point(population.population[parent1_idx], population.population[parent2_idx])
        
        if crossover_type == "uniform":
            offspring1, offspring2 = uniform(population.population[parent1_idx], population.population[parent2_idx])

        if crossover_type == "linear":
            offspring1, offspring2 = linear(population.population[parent1_idx], population.population[parent2_idx])

        if crossover_type == "SBX":
            offspring1, offspring2 = SBX(population.population[parent1_idx], population.population[parent2_idx])

        # extend the population list by appending the two new offsprings
        population_list.extend([offspring1, offspring2])
    
    # initialize the new population as a Population object
    new_population = Population(population_list)
    
    return new_population
    
    
    