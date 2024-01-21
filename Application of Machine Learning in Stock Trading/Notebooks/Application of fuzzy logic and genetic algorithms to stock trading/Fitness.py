from typing import Union
import numpy as np
import pandas as pd
from Genome import Genome
from fuzzy_ta import fuzzy_TA
import matplotlib.pyplot as plt


def evaluate_fitness(series:pd.DataFrame, genome:Genome) -> list[Union[int, float]]:
    """
    This function evaluates the fitness of the genome
    
    Arguments:
        self:
            some text
            
    Returns:
        None:        
    """     

    # initialize the fuzzy_TA instance
    stock = fuzzy_TA(series)

    # momentum indicators
    stock.RSI(
        window = genome.genome_dict["RSI_window"].value,
        p1 = genome.genome_dict["RSI_p1"].value,
        p2 = genome.genome_dict["RSI_p2"].value,
        p3 = genome.genome_dict["RSI_p3"].value,
        p4 = genome.genome_dict["RSI_p4"].value,
        lo_left_node = genome.genome_dict["RSI_low_membership"].value[0],
        lo_right_node = genome.genome_dict["RSI_low_membership"].value[1],
        md_left_node = genome.genome_dict["RSI_middle_membership"].value[0],
        md_middle_node = genome.genome_dict["RSI_middle_membership"].value[1],
        md_right_node = genome.genome_dict["RSI_middle_membership"].value[2],
        hi_left_node = genome.genome_dict["RSI_high_membership"].value[0],
        hi_right_node = genome.genome_dict["RSI_high_membership"].value[1]
    )

    
    # compute for the total value of z
    stock.z_total()
    stock.df['z_sum_rolling']=stock.df['z_sum'].rolling(genome.genome_dict["z_rolling_window"].value).mean()
    # stock.df['z_sum_ewm'] = stock.df['z_sum'].ewm(span=7).mean()
    # print(stock.df[['z_sum', 'z_sum_rolling', 'z_sum_ewm']].tail(20))

    # plot the z values
    # fig, axs = plt.subplots(4, 1, layout='constrained')
    # axs[0].plot(stock.df['Close'].tail(450))
    # axs[1].plot(stock.df['z_sum'].tail(450))
    # axs[2].plot(stock.df['z_sum_rolling'].tail(450))
    # axs[3].plot(stock.df['z_sum_ewm'].tail(200))
    plt.show()

    # initialize the following variables
    stock.df['trailingstop'] = 0
    stock.df['returns'] = 1
    stock.df['change'] = stock.df['Close'].pct_change()+1
    stock.df['regime'] = 0
    has_long_position = False
    num_trades = 0
    buy_locator = list()
    sell_locator = list()
    trailingstop = 1
    
    for i in range(0, len(stock.df)-1):
        # check condition for entry
        condition1 = stock.df['z_sum_rolling'][i] >= genome.genome_dict["entry_condition"].value[1]
        condition2 = has_long_position is False
        condition3 = stock.df['regime'][i] != -1
        if condition1 and condition2 and condition3:
            # buy stock in the next day
            stock.df['regime'][i+1] = 1
            has_long_position = True
            num_trades += 1
            buy_locator.append(stock.df.iloc[i])
            trailingstop = 1
            continue
            
        # establish trailing stop
        if has_long_position is True:
            trailingstop *= stock.df['change'][i]
                
        # check conditions for exit
        condition1 = stock.df['z_sum_rolling'][i] < genome.genome_dict["entry_condition"].value[0]
        condition2 = trailingstop < genome.genome_dict["stop_loss"].value
        condition3 = has_long_position is True
        if( (condition1) or (condition2) ) and condition3:
            stock.df['regime'][i+1] = -1
            has_long_position = False
            sell_locator.append(stock.df.iloc[i])
            trailingstop = 1

    # put 1 between 1 and -1 
    for i in range(1, len(stock.df)):
        if stock.df['regime'][i-1] == 1 and stock.df['regime'][i] == 0:
            stock.df['regime'][i] = 1

    # compute returns
    for i in range(0, len(stock.df)):
        if stock.df['regime'][i] != 0:
            stock.df['returns'][i] = stock.df['change'][i]
    
    # get returns for buy and hold strategy
    bnh_returns = stock.df['change'].cumprod()[-1]
    
    # get the returns of the strategy
    strat_returns = stock.df['returns'].cumprod()[-1]
    
    # get the downside returns
    downside_returns_df = None
    downside_returns_df = stock.df.loc[stock.df['returns'] < 1]
    
    # compute for the downside returns standard deviation
    downside_returns_std = downside_returns_df['returns'].std()

    # compute for the sortino ration of the strategy
    strat_sortino_ratio = sortino_ratio(portfolio_returns = stock.df['returns'].cumprod()[-1], std_downside_portfolio_returns = downside_returns_std)
    
    # check if sortino ratio is negative or NaN;
    # if it is negative or NaN, degenerate it into 0
    if strat_sortino_ratio < 0 or np.isnan(strat_sortino_ratio):
        strat_sortino_ratio = 0
        
    
    # compute for the standard deviation of the strategy
    # return_std = stock.df['returns'].std()
    
    # compute for the sharpe ration of the strategy
    # strat_sharpe_ratio = sharpe_ratio(portfolio_returns = stock.df['returns'].cumprod()[-1], std_portfolio_returns = return_std)
    
    # compute for max drawdown
    # max_drawdown = np.ptp(stock.df["returns"])/stock.df["returns"].max()

    # compute for the total returns and plot these
    # stock.df['change'].cumprod().plot(label = 'Buy and hold')
    # stock.df['returns'].cumprod().plot(label = 'Fuzzy Logic').legend()
    # stock.df['returns'].cumprod().tail(450).plot(label = 'Fuzzy Logic')
    
    # show the percent change of the returns for buy and hold vs fuzzy logic
    # print(stock.df['change'].cumprod()[-1], stock.df['returns'].cumprod()[-1])
    
    return strat_sortino_ratio
    # return (stock, num_trades, bnh_returns, strat_returns, strat_sharpe_ratio, strat_sortino_ratio, max_drawdown)

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
    
    sharpe_ratio = (portfolio_returns-risk_free_rate_returns)/std_portfolio_returns
    return sharpe_ratio