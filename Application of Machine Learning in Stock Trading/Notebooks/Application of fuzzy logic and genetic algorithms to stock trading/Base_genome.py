from Gene import Gene

def base_genome() -> list[Gene]:
    """
    This function creates the base genome to be used in the algorithm
    
    Arguments:
        None
        
    Returns:
        gene_list:list[Gene]
            a list of containing the genes of the genome
    
    """
    gene_list = list()
    gene_list = [
                    Gene(
                        name = "RSI_window",
                        lower_bound = 1,
                        upper_bound = 300,
                        type = "int"),
                
                    Gene(
                        name = "RSI_p1",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float"),
                    
                    Gene(
                        name = "RSI_p2",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float"),
                    
                    Gene(
                        name = "RSI_p3",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float"),

                    Gene(
                        name = "RSI_p4",
                        lower_bound = -1,
                        upper_bound = 1,
                        type = "float"),

                    Gene(
                        name = "RSI_low_membership",
                        lower_bound = 0,
                        upper_bound = 100,
                        type = "linear_membership"),

                    Gene(
                        name = "RSI_middle_membership",
                        lower_bound = 0,
                        upper_bound = 100,
                        type = "triangular_membership"),

                    Gene(
                        name = "RSI_high_membership",
                        lower_bound = 0,
                        upper_bound = 100,
                        type = "linear_membership"),

                    Gene(
                        name = "entry_condition",
                        lower_bound = 1,
                        upper_bound = 100,
                        type = "entry_condition"),

                    Gene(
                        name = "stop_loss",
                        lower_bound = 0.01,
                        upper_bound = 0.99,
                        type = "float"),

                    Gene(
                        name = "z_rolling_window",
                        lower_bound = 1,
                        upper_bound = 300,
                        type = "int")

                ]
    
    return gene_list