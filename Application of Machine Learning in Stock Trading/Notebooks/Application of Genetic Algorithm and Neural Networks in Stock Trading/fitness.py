from math import inf, isnan
from numbers import Real
from os import cpu_count
from sys import int_info
from typing import Callable, MutableSequence, Union
import numpy as np
import pandas as pd
from enum import Enum
from numpy.typing import NDArray
from network import Network
from functools import partial
from multiprocessing import Pool, cpu_count

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

def fitness(nn: Network, window:int, train_set: pd.Series, regime:Callable) -> float:
    """
    This function computes for the fitness of a neural network.

    Arguments:
        nn:Network
            the neural network to be checked for its fitness

        windo:int
            the window to be used in checking the fitness of a neural network
            this corresponds to the number of features in the neural network

        train_set:pd.Series
            the training set to be used in evaluating the fitness of a neural network
        
        regime:Callable
            this is a function that predicts the regime or action to be taken
            given the previous number of windows seen prior

    Returns:
        fitness:float
            the fitness of the neural network
    
    """

    # initialize the value for the fitness
    fitness:float = 0.
    
    # get the strategy regime
    # partially apply the neural network in the regime function
    regime = partial(regime, nn = nn)

    # apply the regime function to the training set
    regime_output = train_set.rolling(window = window).apply(regime, raw = True)

    # transform regime_output as a pandas Series
    regime_series = pd.Series(data = regime_output, name = 'Regime')

    # concatenate the train_set pandas series with the regime_series pandas series
    series = pd.concat([train_set, regime_series], axis = 1)

    # initialize a new column in the pandas dataframe with value 1.
    series['Returns'] = 1.

    # initialize a few variables
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
        
        elif series['Regime'].iat[i] == trading_action.Sell.value and has_long_position == False:
            series['Regime'].iat[i] = trading_action.Hold.value

    # compute for the cumulative returns of the strategy
    series['Cumulative_Returns'] = series['Returns'] - 1
    series['Cumulative_Returns'] = series['Cumulative_Returns'].cumsum()

    # get returns for buy and hold strategy
    # this is used in checking the performance of the strategy
    # bnh_returns = series['Close_pct_change'].cumprod().iat[-1]
    # bnh_returns = series['Close_pct_change'].cumprod() - 1
    # bnh_returns = bnh_returns.iat[-1] * 100
    
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
    max_drawdown = np.ptp(s)/s.max()
    # this is another way of computing the max drawdown of the strategy
    # max_drawdown = np.ptp(series["Returns"].cumprod())/series["Returns"].cumprod().max()
        
    if np.isnan(strat_sortino_ratio):
        fitness = float('-inf')
    
    # the following are the different fitness functions 
    # that I have experimented with this project.
    # fitness = 0.01*strat_sortino_ratio + (num_trades)
    # fitness = 0.01*strat_sortino_ratio + (num_trades) * (1-max_drawdown)
    # fitness = (0.001*strat_sortino_ratio + (1/(1+num_trades))) * (1-max_drawdown)
    # fitness = 0.01*strat_sortino_ratio * (1/(1+num_trades)) * (1-max_drawdown)
    # fitness = strat_sortino_ratio * (1/(1+num_trades)) * (1-max_drawdown)
    fitness  = strat_sortino_ratio
    # fitness = (1-max_drawdown)
    # fitness = num_trades
    
    # check if the strategy performs more than 100 trades
    # if it is more than 100, return a fitness of -inf
    # if num_trades > 100:
    #     fitness = float('-inf')    
    
    # check if the computed fitness is NAN
    # if it is NAN, return a fitness of -inf
    if np.isnan(fitness):
        fitness = float('-inf')  
    
    return fitness
    # return fitness, bnh_returns, strat_returns, max_drawdown, series, strat_sortino_ratio

class trading_action(Enum):
    Buy = 0
    Hold = 1
    Sell = 2

def regime(features:NDArray, nn:Network):
    """
    This function performs a forward propagation of a neural network given a set of feaures
    The output of the forward propagation are the probabilties of taking a certain trading action
    i.e. Buy, Hold, or Sell.

    Arguments:
        features:NDArray
            the features or inputs to the neural network

        nn:Network
            the neural network to be tested

    Returns:
        this function returns an integer corresponding to a trading action
        i.e. 0 is for Buy, 1 is for Hold, and 2 is for Sell
    
    """
    # perform feed forward propagation
    probabilities = nn.propagate_forward(np.array([features]))

    # perform argmax in the outputs
    index = np.argmax(probabilities)

    match index:
        case 0:
            return trading_action.Buy.value
        
        case 1:
            return trading_action.Hold.value
        
        case 2:
            return trading_action.Sell.value
        
        case _:
            raise Exception('Invalid index')

def compute_population_fitness(population:MutableSequence[Network], window:int, fitness:Callable, regime:Callable, train_set:pd.Series) -> MutableSequence[Network]:
    """
    This function computes the fitness of a whole population

    Arguments:
        population:MutableSequence[Network]
            the population whose fitness will be calculated

        window:int
            the window to be used in checking the fitness of a neural network
            this corresponds to the number of features in the neural network

        fitness:Callable
            the fitness function to be used in checking the fitness of a
            neural network
        
        regime:Callable
            this is a function that predicts the regime or action to be taken
            given the previous number of windows seen prior;
            this is an input to the fitness function
        
        train_set:pd.Series
            the training set to be used in evaluating the fitness of a neural network

    Returns:
        population:MutableSequence[Network]
            the population with the computed fitness as part of their attribute
    """

    # compute for the fitness of the population using sequential processing 
    # of the fitness of a neural network
    # uncomment is this section for testing purposes
    # for individual in population:
    #     individual.fitness = fitness(window = window, 
    #                                 train_set = train_set, 
    #                                 nn = individual,
    #                                 regime = regime)
        
    # compute the fitness of the population using multiprocessing 
    fitness = partial(fitness, window = window, train_set = train_set, regime = regime)
    pool = Pool(cpu_count())
    population_fitness = pool.map(fitness, population)

    # assign the fitness values of the individuals in the population
    for individual, fitness_value in zip(population, population_fitness):
        individual.fitness = fitness_value

    return population

def compute_average_population_fitness(population:MutableSequence[Network]) -> float:
    """
    This function computes for the average fitness of a population
    
    Arguments:
        population:MutableSequence[Network]
            a list of neural networks

    Returns:
        average_fitness:float
            the average fitness of the population
    """

    # initialize some values
    average_fitness = 0.
    total_fitness = 0.
    counter = 0
    
    # compute for the average fitness
    for individual in population:
        # check if the fitness of a neural network is -inf
        # if it is not, add this to the total fitness
        if individual.fitness != float('-inf'):
            total_fitness += individual.fitness
            counter += 1            

    try:
        average_fitness = total_fitness/counter
    except ZeroDivisionError:
        # if an error occurs, assign a zero average fitness for the population
        # this usually happens of all neural networks in the population has a -inf fitness
        average_fitness = 0

    # release some memory
    del total_fitness

    return average_fitness

def evaluate_nn(nn: Network, train_set, regime, window):
    fitness = 0.
    
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
            
        elif series['Regime'].iat[i] == trading_action.Sell.value and has_long_position == False:
            series['Regime'].iat[i] = trading_action.Hold.value 
        
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
    
    return fitness, bnh_returns, strat_returns, max_drawdown, series, strat_sortino_ratio, num_trades