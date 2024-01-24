import copy
import math
import pandas as pd

# create a function that splits the data into train and test sets
def split_train_test_sets(series: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    This function splits the time series data into train and test sets
    
    Arguments:
        series: pd.DataFrame
            a time series data of type
            
    Returns:
        train, test: tuple(pd.DataFrame, pd.DataFrame)
            the splitted train and test sets
    """
    # split into train and test sets
    train, test = series[1:-math.floor(len(series)*0.2)], series[-math.floor(len(series)*0.2):]
    return train, test

def split_train_set(series:pd.DataFrame, window:int = 500) -> list[pd.DataFrame]:
    """
    This function splits or slices the train set into batches with a corresponding window length

    Arguments:
        series:pd.DataFrame
            a pandas dataframe containing the training set of the 

    Returns:
        train_set:list[pd.DataFrame]
            a list containing multiple pandas dataframes
    """
    train_set = list()
    for i in range(len(series)-window):
        train_set.append(copy.deepcopy(series[i:i+window]))
    return train_set