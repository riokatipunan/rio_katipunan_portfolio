# Application of Fuzzy Logic and Genetic Algorithm in Stock Trading

## Introduction

This project explores the application of fuzzy logic and genetic algorithm in stock trading. This is a natural extension of an earlier project where a fuzzy inference system was used in stock trading. In this project, the parameters of the fuzzy inference system are optimized using genetic algorithm.

## Methodology

This project uses real-coded genetic algorithm in optimizing the parameters of the fuzzy inference system. The genes of the genetic algorithm are the parameters of the fuzzy inference system, for example, the parameters are:

1. RSI window
2. the values of the nodes of the membership function
3. the threshold for the buy and sell signals

The algorithm pseudo-code of this project is provided below:

population = init_population()
for _ in NUM_GENERATION:
    for individual in population:
        individual.fitness = evaluate_fitness(individual)

    selected_population = selection(population)
    offsprings = crossover(selected_population)
    offsprings = mutate(offsprings)

    population = selected_population + offsprings
### Selection

1. Roullete Wheel
2. Rank
3. Tournament
4. Stochastic Universal Sampling

### Crossover

1. Single point
2. Two point
3. Uniform 
4. Linear
5. Simulated Binary Crossover

### Mutation

1. Uniform 
2. Normal

## Results and Discussion

## Conclusions

If you find this interesting, please feel free to send me an email at riokatipunan@gmail.com.

Thank you.