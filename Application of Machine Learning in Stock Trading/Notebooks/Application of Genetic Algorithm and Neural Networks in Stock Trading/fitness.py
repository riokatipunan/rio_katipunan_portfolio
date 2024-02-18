from math import inf, isnan
from os import cpu_count
from typing import Callable, MutableSequence
import numpy as np
import pandas as pd
from enum import Enum
from numpy.typing import NDArray
from network import Network
from functools import partial
from multiprocessing import Pool, cpu_count
import math
from statistics import mean
from speciation import cluster, cluster_population

def sortino_ratio(portfolio_returns:float ,std_downside_portfolio_returns:float, risk_free_rate_returns:float = 2.5) -> float:
    """
    This function computes for the sortino ratio of a given strategy

    Arguments:
        portoflio_returns:float
            the portfolio returns of a strategy
        
        std_downside_portfolio_returns:float
            the standard deviation of the downside of the portfolio retunrs of a strategy

        risk_free_rate_returns:flaot
            the percent return of a risk free strategy (e.g. bonds, bank interests, time deposits, etc.)
    
    Returns:
        sortino_ratio:float
            the sortino ratio of the strategy
    """
    if std_downside_portfolio_returns == 0:
        return float("-inf")

    else:
        sortino_ratio = (portfolio_returns-risk_free_rate_returns)/std_downside_portfolio_returns
        return sortino_ratio

def sharpe_ratio(portfolio_returns:float ,std_portfolio_returns :float, risk_free_rate_returns:float = 2.5) -> float:
    """
    This function computes the sharpe ratio of a given strategy

    Arguments:
        portfolio_returns:float
            the portfolio returns of a strategy
        
        std_portfolio_returns:float
            the standard deviation of the portfolio returns

        risk_free_rate_returns:float
            the percent return of a risk free strategy (e.g. bonds, bank interests, time deposits, etc.) 
    
    Returns:
        sharpe_ratio:float
            the sharpe ratio of a given strategy
    """
    if std_portfolio_returns == 0:
        return float("-inf")
    
    else:
        sharpe_ratio = (portfolio_returns-risk_free_rate_returns)/std_portfolio_returns
        return sharpe_ratio

def fitness(nn: Network, window, train_set: pd.Series, regime):
    fitness = 0
    
    # get the strategy regime
    regime = partial(regime, nn = nn)
    regime_output = train_set.rolling(window=window).apply(regime, raw = True)
    regime_series = pd.Series(data = regime_output, name = 'Regime')

    series = pd.concat([train_set, regime_series], axis = 1)
    series['Returns'] = 1.
    has_long_position:bool = False
    num_trades:int = 0
    
    # loop through all the elements in the series
    for i in range(len(series)):
        if series['Regime'].iat[i] == trading_action.Buy.value and has_long_position == False:
            has_long_position = True
            num_trades += 1
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]
            
        elif series['Regime'].iat[i] == trading_action.Sell.value and has_long_position == True:
            has_long_position = False
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]
            
        elif series['Regime'].iat[i] == trading_action.Hold.value and has_long_position == True:
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]
            
        elif series['Regime'].iat[i] == trading_action.Buy.value and has_long_position == True:
            series['Regime'].iat[i] = trading_action.Hold.value
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]
        # print(series['Returns'].iat[i], '\t', series['Regime'].iat[i], '\t', series['Close_pct_change'].iat[i])

    # compute for the cumulative retunrs
    
    series['Cumulative_Returns'] = series['Returns'] - 1
    series['Cumulative_Returns'] = series['Cumulative_Returns'].cumsum()

    # get returns for buy and hold strategy
    # bnh_returns = series['Close_pct_change'].cumprod().iat[-1]
    bnh_returns = series['Close_pct_change'].cumprod() - 1
    bnh_returns = bnh_returns.iat[-1] * 100
    
    # get the returns of the strategy
    strat_returns = series['Returns'].cumprod() - 1 
    strat_returns = strat_returns.iat[-1] * 100

    # get the downside returns
    # and compute for the downside returns standard deviation
    downside_returns_series = series.loc[series['Returns'] < 1]
    downside_returns_std = downside_returns_series['Returns'].std()

    # compute for the sortino ration of the strategy
    strat_sortino_ratio = sortino_ratio(portfolio_returns = strat_returns, 
                                        std_downside_portfolio_returns = downside_returns_std)
    
    # compute for max drawdown
    s = series["Returns"].cumprod()
    # max_drawdown = np.ptp(series["Returns"].cumprod())/series["Returns"].cumprod().max()
    max_drawdown = np.ptp(s)/s.max()

    # check if sortino ratio is negative or NaN;
    # if it is negative or NaN, or if the total number entry trades is 20
    # degenerate it into negative infinity
    # if np.isnan(strat_sortino_ratio) or num_trades > 20 or max_drawdown > 0.5:
    #     strat_sortino_ratio = float('-inf')
        
    # if np.isnan(strat_sortino_ratio):
    #     strat_sortino_ratio = float('-inf')        
        
    if np.isnan(strat_sortino_ratio):
        strat_sortino_ratio = float('-inf')  
        


    # if (strat_sortino_ratio == float('-inf')) and (max_drawdown == 0.):
    #     fitness = float("-inf")
    
    # if (strat_sortino_ratio == float('-inf')) and (max_drawdown == 0.):
    #     fitness = float("-inf")    

    # if strat_sortino_ratio > 0:
    #     # fitness = strat_sortino_ratio * (1/(1+num_trades)) * max_drawdown
    #     fitness = strat_sortino_ratio * (1-max_drawdown)
    
    # elif strat_sortino_ratio < 0:
    #     # fitness = strat_sortino_ratio * (1/(1+num_trades)) * max_drawdown
    #     fitness = strat_sortino_ratio * max_drawdown
    
    fitness = 0.001*strat_sortino_ratio + (num_trades) * (1-max_drawdown)
    # fitness = (0.001*strat_sortino_ratio + (1/(1+num_trades))) * (1-max_drawdown)
    # fitness = 0.01*strat_sortino_ratio * (1/(1+num_trades)) * (1-max_drawdown)
    # fitness = strat_sortino_ratio * (1/(1+num_trades)) * (1-max_drawdown)
    # fitness  = strat_sortino_ratio
    # fitness = (1-max_drawdown)
    # fitness = num_trades
    
    if num_trades > 20:
        fitness = float('-inf')    
    
    return fitness
    # return fitness, bnh_returns, strat_returns, max_drawdown, series, strat_sortino_ratio

class trading_action(Enum):
    Buy = 0
    Hold = 1
    Sell = 2

def regime(features: NDArray, nn:Network):
    probabilities = nn.propagate_forward(np.array([features]))
    index = np.argmax(probabilities)

    match index:
        case 0:
            return trading_action.Buy.value
        
        case 1:
            return trading_action.Hold.value
        
        case 2:
            return trading_action.Sell.value
        
        case _:
            pass

def compute_population_fitness(population: MutableSequence[Network], fitness: Callable, regime: Callable, train_set: pd.Series ):
    
    # sequential processing of the fitness of a neural network
    # for individual in population:
    #     individual.fitness = fitness(window = 150, 
    #                                 train_set = train_set, 
    #                                 nn = individual,
    #                                 regime = regime)
        
    # using multiprocessing
    fitness = partial(fitness, window = 150, train_set = train_set, regime = regime)
    pool = Pool(cpu_count())
    population_fitness = pool.map(fitness, population)

    # assign the fitness values of the individuals in the population
    for individual, fitness_value in zip(population, population_fitness):
        individual.fitness = fitness_value
      
    # clustered_population = cluster_population(population, eps = 0.2)  
      
    # print(len(clustered_population))
    # print(clustered_population)
    # for specie in clustered_population:
    #     num_indiv_in_specie = len(specie)
    #     for individual in specie:
    #         # adjust the fitness of the individual
    #         individual.fitness = individual.fitness/num_indiv_in_specie
    #         print(individual.cluster, individual.fitness)



    return population

def compute_average_population_fitness(population):
    # initialize some values
    average_fitness = 0
    counter = 0
    
    for individual in population:
        if individual.fitness != float('-inf'):
            average_fitness += individual.fitness
            counter += 1            

    try:
        average_fitness = average_fitness/counter
    except ZeroDivisionError:
        # if an error occors, assign a zero average fitness for the population
        average_fitness = 0    

    return average_fitness


def compute_population_clusters():
    pass

def evaluate_nn(nn: Network, train_set, regime, window):
    fitness = 0
    
    # get the strategy regime
    regime = partial(regime, nn = nn)
    regime_output = train_set.rolling(window=window).apply(regime, raw = True)
    regime_series = pd.Series(data = regime_output, name = 'Regime')

    series = pd.concat([train_set, regime_series], axis = 1)
    series['Returns'] = 1.
    has_long_position:bool = False
    num_trades:int = 0
    
    # loop through all the elements in the series
    for i in range(len(series)):
        if series['Regime'].iat[i] == trading_action.Buy.value and has_long_position == False:
            has_long_position = True
            num_trades += 1
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]
            
        elif series['Regime'].iat[i] == trading_action.Sell.value and has_long_position == True:
            has_long_position = False
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]
            
        elif (series['Regime'].iat[i] == trading_action.Hold.value and has_long_position == True):
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]
            
        elif series['Regime'].iat[i] == trading_action.Buy.value and has_long_position == True:
            series['Regime'].iat[i] = trading_action.Hold.value
            series['Returns'].iat[i] = series['Close_pct_change'].iat[i]  
        
        # print(series['Returns'].iat[i], '\t', series['Regime'].iat[i], '\t', series['Close_pct_change'].iat[i])

    series['Cumulative_Returns'] = series['Returns'] - 1
    series['Cumulative_Returns'] = series['Cumulative_Returns'].cumsum()

    # get returns for buy and hold strategy
    # bnh_returns = series['Close_pct_change'].cumprod().iat[-1]
    bnh_returns = series['Close_pct_change'].cumprod() - 1
    bnh_returns = bnh_returns.iat[-1] * 100
    
    # get the returns of the strategy
    strat_returns = series['Returns'].cumprod() - 1 
    strat_returns = strat_returns.iat[-1] * 100

    # get the downside returns
    # and compute for the downside returns standard deviation
    downside_returns_series = series.loc[series['Returns'] < 1]
    downside_returns_std = downside_returns_series['Returns'].std()

    # compute for the sortino ration of the strategy
    strat_sortino_ratio = sortino_ratio(portfolio_returns = strat_returns, 
                                        std_downside_portfolio_returns = downside_returns_std)
    
    # compute for max drawdown
    s = series["Returns"].cumprod()
    # max_drawdown = np.ptp(series["Returns"].cumprod())/series["Returns"].cumprod().max()
    max_drawdown = np.ptp(s)/s.max()

    # check if sortino ratio is negative or NaN;
    # if it is negative or NaN, or if the total number entry trades is 20
    # degenerate it into negative infinity
    # if np.isnan(strat_sortino_ratio) or (num_trades > 20) or (max_drawdown > 0.1):
    #     strat_sortino_ratio = float('-inf')

    # if (strat_sortino_ratio == float('-inf')) and (max_drawdown == 0.):
    #     fitness = float("-inf")

    # if strat_sortino_ratio > 0:
    #     # fitness = strat_sortino_ratio * (1/(1+num_trades)) * max_drawdown
    #     fitness = strat_sortino_ratio * (1-max_drawdown)
    
    # elif strat_sortino_ratio < 0:
    #     # fitness = strat_sortino_ratio * (1/(1+num_trades)) * max_drawdown
    #     fitness = strat_sortino_ratio * max_drawdown
    
    # fitness = 0.001*strat_sortino_ratio * (num_trades) * (1-max_drawdown)
    # fitness = strat_sortino_ratio * (1/(1+num_trades)) * (1-max_drawdown)
    fitness = strat_sortino_ratio
    
    # return fitness
    return fitness, bnh_returns, strat_returns, max_drawdown, series, strat_sortino_ratio, num_trades