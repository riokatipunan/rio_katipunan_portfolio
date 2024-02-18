def cluster(points, eps = 0.2):

    clusters = []
    points_sorted = sorted(points)
    curr_point = points_sorted[0]
    curr_cluster = [curr_point]
    for point in points_sorted[1:]:
        if point <= curr_point + eps:
            curr_cluster.append(point)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [point]
        curr_point = point
    clusters.append(curr_cluster)
    
    return clusters

def cluster_population(population, eps = 0.2):
    clusters = list()
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    curr_individual= sorted_population[0]
    curr_cluster = [curr_individual]
    
    for invididual in sorted_population[1:]:
        if (invididual.fitness >= curr_individual.fitness + eps):
            curr_cluster.append(invididual)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [invididual]
        curr_individual = invididual
    clusters.append(curr_cluster)

    cluster_id = 0
    for specie in clusters:
        for individual in specie:
            individual.cluster = cluster_id
        cluster_id += 1
    
    return clusters

def adjust_population_fitness(population):
    
    clustered_population = cluster_population(population)
    population = list()
    
    # print(len(clustered_population))
    # print(clustered_population)
    for specie in clustered_population:
        num_indiv_in_specie = len(specie)
        for individual in specie:
            # adjust the fitness of the individual
            individual.fitness = individual.fitness/num_indiv_in_specie
            population.append(individual)
            # print(individual.cluster, individual.fitness)
    
    return population