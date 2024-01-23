from Population import Population


def reproduce(population:Population) -> Population:
    """
    This function takes in a population and reproduces them to 
    
    Arguments:
        population:Population
            The population to be reproduced
    
    Returns:
        new_population:
            The new population to be returned
    """
    
    new_population = Population
    if len(population == 0):
        new_population