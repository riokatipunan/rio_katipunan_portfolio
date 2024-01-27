from Gene import Gene

def seed_genome() -> list[Gene]:
    """
    This function returns a list of genes that will be used 
    as the seed for genetic algorithm

    Arguments:
        None

    Returns:
        seed_gene_list:list[Gene]
            a list of genes that will be the seed in the genetic algorithm
    """

    # create the seed gene; this gene contains initial values believed to be good instance values
    seed_gene_list = list()
    seed_gene_list = [
                    Gene(
                        name = "RSI_window",
                        lower_bound = 1,
                        upper_bound = 300,
                        type = "int",
                        value = 30),
                
                    Gene(
                        name = "RSI_p1",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float",
                        value = 1),
                    
                    Gene(
                        name = "RSI_p2",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float",
                        value = 1),
                    
                    Gene(
                        name = "RSI_p3",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float",
                        value = 1),

                    Gene(
                        name = "RSI_p4",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float",
                        value = 1),

                    Gene(
                        name = "RSI_low_membership",
                        lower_bound = 0,
                        upper_bound = 100,
                        type = "linear_membership",
                        value = [0, 25]),

                    Gene(
                        name = "RSI_middle_membership",
                        lower_bound = 0,
                        upper_bound = 100,
                        type = "triangular_membership",
                        value = [25, 50, 75]),

                    Gene(
                        name = "RSI_high_membership",
                        lower_bound = 0,
                        upper_bound = 100,
                        type = "linear_membership",
                        value = [75,100]),

                    Gene(
                        name = "entry_condition",
                        lower_bound = 1,
                        upper_bound = 100,
                        type = "entry_condition",
                        value = [50,50]),

                    Gene(
                        name = "stop_loss",
                        lower_bound = 0.01,
                        upper_bound = 0.99,
                        type = "float",
                        value = 0.95),

                    Gene(
                        name = "z_rolling_window",
                        lower_bound = 1,
                        upper_bound = 300,
                        type = "int",
                        value = 30)

                                      
                ]
    
    return seed_gene_list