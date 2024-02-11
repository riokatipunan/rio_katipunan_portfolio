import random
import numpy as np
from numpy.typing import NDArray
from enum import Enum
from typing import Tuple, Union
import copy


class crossover_operator(Enum):
    uniform = 'uniform'
    single_point = 'single point'
    two_point = 'two point'
    linear = 'linear'
    SBX = 'SBX'
    
# perform uniform crossover
def crossover(flat_nn1: NDArray, flat_nn2: NDArray) -> Tuple[NDArray, NDArray]:
    crossover_operators = [crossover_operator.uniform, 
                           crossover_operator.single_point,
                           crossover_operator.two_point,
                           crossover_operator.linear,
                           crossover_operator.SBX]

    # randomly select a crossover operator
    crossover_type = random.choice(crossover_operators)
    
    match crossover_type:
        case crossover_operator.uniform:
            return uniform_crossover(flat_nn1=flat_nn1, flat_nn2=flat_nn2)
        
        case crossover_operator.single_point:
            return single_point_crossover(flat_nn1=flat_nn1, flat_nn2=flat_nn2)
        
        case crossover_operator.two_point:
            return two_point_crossover(flat_nn1=flat_nn1, flat_nn2=flat_nn2)
        
        case crossover_operator.linear:
            return linear_crossover(flat_nn1=flat_nn1, flat_nn2=flat_nn2)   

        case crossover_operator.SBX:
            return SBX(flat_nn1=flat_nn1, flat_nn2=flat_nn2)   
        
        case _:
            raise Exception('Not a valid crossover operator')

def uniform_crossover(flat_nn1, flat_nn2) -> Tuple[NDArray, NDArray]:
    offspring1 = list()
    offspring2 = list()

    # loop through the nodes of the boths NNs
    # and perform uniform crossover
    for nn1_node, nn2_node in zip(flat_nn1, flat_nn2):
        if random.uniform(0,1) >=0.5:
            offspring1.append(nn1_node)
            offspring2.append(nn2_node)
        else:
            offspring1.append(nn2_node)
            offspring2.append(nn1_node)
    
    # instatiate the offsprings as numpy arrays
    offspring1_ndarray = np.array(offspring1)
    offspring2_ndarray = np.array(offspring2)

    # release some memory
    del offspring1
    del offspring2

    return offspring1_ndarray, offspring2_ndarray

def single_point_crossover(flat_nn1, flat_nn2) -> Tuple[NDArray, NDArray]:
    # initialize the offspring
    offspring1 = list()
    offspring2 = list()
    
    # assert that the length of the two NNs are the same
    assert len(flat_nn1) == len(flat_nn2), 'The two neural networs should be the same length' 
    
    # identify the crossover point
    crossover_point = random.randint(1, len(flat_nn1)-1)
    
    # at the crossoverpoint, swap the genes of the two parent genomes
    for i in range(len(flat_nn1)):
        if i < crossover_point:
            offspring1.append(copy.deepcopy(flat_nn1[i]))
            offspring2.append(copy.deepcopy(flat_nn2[i]))
        else:
            offspring1.append(copy.deepcopy(flat_nn2[i]))
            offspring2.append(copy.deepcopy(flat_nn1[i]))
    
    # instatiate the offsprings as numpy arrays
    offspring1_ndarray = np.array(offspring1)
    offspring2_ndarray = np.array(offspring2)

    # release some memory
    del offspring1
    del offspring2

    return offspring1_ndarray, offspring2_ndarray

def two_point_crossover(flat_nn1, flat_nn2) -> Tuple[NDArray, NDArray]:
    # instantiate the offsprings as lists
    offspring1 = list()
    offspring2 = list()
    
    # assert that the length of the two NNs are the same
    assert len(flat_nn1) == len(flat_nn2), 'The two neural networs should be the same length'    
    
    # identify the two crossoverpoints
    #  the code below checks and ensures that the first crossover point
    # is less than the second crossoverpoint
    while True:
        crossover_point1 = random.randint(1, len(flat_nn1)-1)
        crossover_point2 = random.randint(1, len(flat_nn1)-1)
        
        if crossover_point1 < crossover_point2:
            break
    
    # do the two-point crossover
    for i in range(len(flat_nn1)):
        if i < crossover_point1:
            offspring1.append(copy.deepcopy(flat_nn1[i]))
            offspring2.append(copy.deepcopy(flat_nn2[i]))
        elif (i > crossover_point1) and (i < crossover_point2):
            offspring1.append(copy.deepcopy(flat_nn2[i]))
            offspring2.append(copy.deepcopy(flat_nn1[i]))
        else:
            offspring1.append(copy.deepcopy(flat_nn1[i]))
            offspring2.append(copy.deepcopy(flat_nn2[i]))
    
    # instatiate the offsprings as numpy arrays
    offspring1_ndarray = np.array(offspring1)
    offspring2_ndarray = np.array(offspring2)

    # release some memory
    del offspring1
    del offspring2

    return offspring1_ndarray, offspring2_ndarray

def linear_crossover(flat_nn1, flat_nn2) -> Tuple[NDArray, NDArray]:
    # instantiate the offspring as a list
    offspring1 = list()
    offspring2 = list()
    
    # assert that the length of the two NNs are the same
    assert len(flat_nn1) == len(flat_nn2), 'The two neural networs should be the same length'    
    
    # loop through the genome of the parents and do linear crossover
    for i in range(len(flat_nn1)):
        # determine the scaling factors for the linear crossover
        alpha = random.uniform(0,1)
        beta = random.uniform(0,1)
 
        # perform linear crossover
        offspring1_value = ((alpha * flat_nn1[i]) + (beta * flat_nn2[i]))/(alpha+beta)
        offspring2_value = ((beta * flat_nn1[i]) + (alpha * flat_nn2[i]))/(alpha+beta)

        # append the offspring values in the offspring genome
        offspring1.append(copy.deepcopy(offspring1_value))
        offspring2.append(copy.deepcopy(offspring2_value))

    # instatiate the offsprings as numpy arrays
    offspring1_ndarray = np.array(offspring1)
    offspring2_ndarray = np.array(offspring2)

    # release some memory
    del offspring1
    del offspring2

    return offspring1_ndarray, offspring2_ndarray

def SBX(flat_nn1, flat_nn2) -> Tuple[NDArray, NDArray]:
    # initialize the offsprings as list
    offspring1 = list()
    offspring2 = list()
    
    # assert that the length of the two NNs are the same
    assert len(flat_nn1) == len(flat_nn2), 'The two neural networs should be the same length'        
    
    # loop through each gene in the genome of the parents
    for i in range(len(flat_nn1)):        
        # initialilze the factors for the SBX
        u = random.uniform(0,1)
        n = random.choice([2,3,4,5])
        
        # determine the value of beta
        if u <= 0.5:
            beta = (2*u)**(1/(n+1))
        else:
            beta = (1/(2*(1-u)))**(1/(n+1))
            
        # compute for the values of the offsprings
        offspring1_value = 0.5*(((1+beta)*flat_nn1[i]) + ((1-beta)*flat_nn2[i]))
        offspring2_value = 0.5*(((1+beta)*flat_nn2[i]) + ((1-beta)*flat_nn1[i]))
    
        # append the offspring values in the offspring genome
        offspring1.append(copy.deepcopy(offspring1_value))
        offspring2.append(copy.deepcopy(offspring2_value))
    
    # instatiate the offsprings as numpy arrays
    offspring1_ndarray = np.array(offspring1)
    offspring2_ndarray = np.array(offspring2)
    
    # release some memory
    del offspring1
    del offspring2

    return offspring1_ndarray, offspring2_ndarray
