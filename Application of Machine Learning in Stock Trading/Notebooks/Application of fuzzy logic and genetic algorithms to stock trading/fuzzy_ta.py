import pandas as pd
import numpy as np
import ta
from fuzzy_membership_func import trimf, linearf

# build a class that will encapsulate a stock and perform fuzzy technical analysis on it
class fuzzy_TA:
    def __init__(self, df: pd.DataFrame):
        """
        Arguments:
            df: pd.DataFrame
                pandas dataframe containing the closing, opening, high, low, and volume of a stock
                
        Returns:
        """
        
        self.df = df
        self.u = pd.DataFrame(index = self.df.index)
        self.z = pd.DataFrame(index = self.df.index)
        self.u_sum = pd.DataFrame(index = self.df.index)
        self.z_sum = pd.DataFrame(index = self.df.index)
    # MOMENTUM INDICATORS
    
    def RSI(self, 
            window:int          = 14,
            fillna:bool         = False,
            p1:float            = 1,
            p2:float            = 1,
            p3:float            = 1,
            p4:float            = 1,
            lo_left_node: int   = 0,
            lo_right_node: int  = 50,
            md_left_node: int   = 0,
            md_middle_node: int = 50,
            md_right_node: int  = 100,
            hi_left_node: int   = 50,
            hi_right_node: int  = 100
            ):
        """
        Relative Stregth Index
    
        Arguments
            window: int
                window or number of elements to be included in the calculation

            fillna: bool
                if True, fill NaN values
            
            p1: float
                value to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant
                this value ranges from 0 to 1

            p2: float
                value to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant
                this value ranges from 0 to 1

            p3: float
                value to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant
                this value ranges from 0 to 1

            p3: float
                value to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant
                this value ranges from 0 to 1    
                
        Returns
        """
        
        # compute for the RSI of the stock
        self.df[f'RSI{window}'] = (ta.momentum.RSIIndicator(
            close = self.df['Close'],
            window = window,
            fillna = fillna)
            .rsi()
        )
        
        # compute for the membership values of the RSI values
        self.u[f'RSI{window}_lo'] = self.df[f'RSI{window}'].apply(lambda x: linearf(x, [lo_left_node, lo_right_node], positive_slope = False))
        self.u[f'RSI{window}_md'] = self.df[f'RSI{window}'].apply(lambda x: trimf(x, [md_left_node, md_middle_node, md_right_node])) 
        self.u[f'RSI{window}_hi'] = self.df[f'RSI{window}'].apply(lambda x: linearf(x, [hi_left_node, hi_right_node], positive_slope = True))
        
        # the following are the fuzzy rules for RSI
        # if RSI is low, then buy
        self.z[f'RSI{window}_lo'] = (p1 * ((self.u[f'RSI{window}_lo'] * 25)  + 75))
        
        # # if RSI is medium, then hold
        mask = (self.df[f'RSI{window}'] < 50)
        self.z.loc[mask, f'RSI{window}_md'] = (p2 * ((self.u[f'RSI{window}_md'] * -25) + 75))
        
        mask = (self.df[f'RSI{window}'] > 50)
        self.z.loc[mask, f'RSI{window}_md'] = (p3 * ((self.u[f'RSI{window}_md'] * 25) + 25))

        # if RSI is high then sell
        self.z[f'RSI{window}_hi'] = (p4 * ((self.u[f'RSI{window}_hi'] * -25) + 25))
        
    def StochRSI(self, window:int = 14, smooth1:int = 3, smooth2:int = 3, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Stochastic RSI
        
            This method computes for the stochastic RSI of a given series.


        Arguments:
            window: int
                window or number of elements to be included in the calculation of RSI

            smooth1: int
                first smoothing constant in computing the stochasting RSI

            smooth2: int
                second smoothing constant in computing the stochasting RSI

            fillna: bool
                if True, fill NaN values        
            
            p0: float
                constant to be passed in the consequent of the Tsukamoto model
            
            p1: float
                constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant

        Returns:
            None
        """
        
        # calculate the stochasting RSI
        self.df[f'StochRSI{window}'] = (
            ta.momentum.StochRSIIndicator(
                close = self.df['Close'],
                window = window,
                smooth1 = smooth1,
                smooth2 = smooth2,
                fillna = fillna)
            .stochrsi_d()
        )

        # calculate the membership values for low, medium and high RSI
        self.u[f'StochRSI{window}_lo'] = self.df[f'StochRSI{window}'].apply(lambda x: linearf(x, [0, 0.2], positive_slope = False))
        self.u[f'StochRSI{window}_md'] = self.df[f'StochRSI{window}'].apply(lambda x: trimf(x, [0, 0.5, 1])) 
        self.u[f'StochRSI{window}_hi'] = self.df[f'StochRSI{window}'].apply(lambda x: linearf(x, [0.8, 1], positive_slope = True))
        
        # the following are the fuzzy rules for StochRSI
        # if StochRSI is low, then buy
        self.z[f'StochRSI{window}_lo'] = p0 + (p1 * ((self.u[f'StochRSI{window}_lo'] * 25)  + 75))
        
        # if StochRSI is medium and StochRSI is less than 0.5, then buy
        mask = (self.df[f'StochRSI{window}'] < 0.5)
        self.z.loc[mask, f'StochRSI{window}_md'] = p0 + (p1 * ((self.u[f'StochRSI{window}_md'] * -25) + 75))
        
        # if StochRSI is medium and StochRSI is more than 0.5, then sell
        mask = (self.df[f'StochRSI{window}'] > 0.5)
        self.z.loc[mask, f'StochRSI{window}_md'] = p0 + (p1 * ((self.u[f'StochRSI{window}_md'] * 25) + 25))

        # if StochRSI is high then sell
        self.z[f'StochRSI{window}_hi'] = p0 + (p1 * ((self.u[f'StochRSI{window}_hi'] * -25) + 25))

    def StochRSI_KxD(self, window:int = 14, smooth1:int = 1, smooth2:int = 3, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Stochastic RSI Cross
        
            This method computes for the stochastic RSI
            k is the slow indicator
            d is the fast indicator
        
        Arguments:
            window: int
                window used in the computation of the stochastic RSI
                
            smooth1: int
                first smoothing constant used in computing the stochasting RSI
                
            smooth2: int
                second smoothing constant used in computing the stochastic RSI
                
            fillna: bool
                if True, fill NaN values

            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant

        Returns:
            None
        """
        
        # compute for the fast stochastic
        self.df[f'StochRSI_d{window}'] = (
            ta.momentum.StochRSIIndicator(
                close = self.df['Close'],
                window = window,
                smooth1 = smooth1,
                smooth2 = smooth2,
                fillna = fillna)
            .stochrsi_d()
        )
        
        # compute for the slow stochastic
        self.df[f'StochRSI_k{window}'] = (
            ta.momentum.StochRSIIndicator(
                close = self.df['Close'],
                window = window,
                smooth1 = smooth1,
                smooth2 = smooth2,
                fillna = fillna)
            .stochrsi_k()
        )
        
        # compute for the KxD difference
        KxD_diff =  self.df[f'StochRSI_k{window}'] - self.df[f'StochRSI_d{window}']
        
        # calculate the membership values for low, medium and high RSI
        self.u[f'StochRSI_KxD{window}_neg'] = KxD_diff.apply(lambda x: linearf(x, [-0.10, 0], positive_slope = False))
        self.u[f'StochRSI_KxD{window}_zero'] = KxD_diff.apply(lambda x: trimf(x, [-0.10, 0, 0.10])) 
        self.u[f'StochRSI_KxD{window}_pos'] = KxD_diff.apply(lambda x: linearf(x, [0, 0.10], positive_slope = True))
        
        # the following are the fuzzy rules for PPO
        # if PPO_hist is postive then buy
        self.z[f'StochRSI_KxD{window}_pos'] = p0 + (p1 * ((self.u[f'StochRSI_KxD{window}_pos'] * 25) + 75))
        
        # if PPO_hist is zero
        mask = (KxD_diff > 0)
        # if KxD_diff is above 0, then lean towards buying
        self.z.loc[mask, f'StochRSI_KxD{window}_zero'] = p0 + (p1 * ((self.u[f'StochRSI_KxD{window}_zero'] * -25) + 75))

        mask = (KxD_diff <= 0)
        # if KxD_diff is less than or equal to  0, then lean towards selling
        self.z.loc[mask, f'StochRSI_KxD{window}_zero'] = p0 + (p1 * ((self.u[f'StochRSI_KxD{window}_zero'] * 25) + 25))

        # if KxD_diff is negative then sell
        self.z[f'StochRSI_KxD{window}_neg'] = p0 + (p1 * ((self.u[f'StochRSI_KxD{window}_neg'] * -25) + 25))
        
    def WilliamsR(self, window:int = 14, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Compute for the williams R 
        
        Arguments:
            window: int
                the window used in the computation of the WilliamsR

            fillna: bool
                if True, fill NaN values

            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant

        Returns:
            None        
        """
        # compute for Williams % R
        self.df[f'WilliamsR{window}'] = (
            ta.momentum.WilliamsRIndicator(
                high = self.df['High'],
                low = self.df['Low'],
                close = self.df['Close'],
                lbp = window,
                fillna = fillna)
            .williams_r()
        )

        # calculate the membership values for low, medium and high RSI
        self.u[f'WilliamsR{window}_lo'] = self.df[f'WilliamsR{window}'].apply(lambda x: linearf(x, [-100, -80], positive_slope = False))
        self.u[f'WilliamsR{window}_md'] = self.df[f'WilliamsR{window}'].apply(lambda x: trimf(x, [-100, -50, 0])) 
        self.u[f'WilliamsR{window}_hi'] = self.df[f'WilliamsR{window}'].apply(lambda x: linearf(x, [-20, 0], positive_slope = True))
        
        # the following are the fuzzy rules for StochRSI
        # if StochRSI is low, then buy
        self.z[f'WilliamsR{window}_lo'] = p0 + (p1 * ((self.u[f'WilliamsR{window}_lo'] * 25)  + 75))
        
        # if StochRSI is medium and StochRSI is less than 0.5, then buy
        mask = (self.df[f'WilliamsR{window}'] < -50)
        self.z.loc[mask, f'WilliamsR{window}_md'] = p0 + (p1 * ((self.u[f'WilliamsR{window}_md'] * -25) + 75))
        
        # if StochRSI is medium and StochRSI is more than 0.5, then sell
        mask = (self.df[f'WilliamsR{window}'] >= -50)
        self.z.loc[mask, f'WilliamsR{window}_md'] = p0 + (p1 * ((self.u[f'WilliamsR{window}_md'] * 25) + 25))

        # if StochRSI is high then sell
        self.z[f'WilliamsR{window}_hi'] = p0 + (p1 * ((self.u[f'WilliamsR{window}_hi'] * -25) + 25))

    def Ultimate(self, window1:int = 7, window2:int = 14, window3:int = 28, weight1:float = 4.0, weight2:float = 2.0, weight3:float = 1.0, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Ultiimate oscilator
        
        Arguments:
            window1:int
                short period

            window2:int
                medium period

            window3:int
                long period

            weight1:float
                weight of short BP average for UO

            weight2:float
                weight of medium BP average for UO

            weight3:float
                weight of long BP average for UO

            fillna: bool
                if True, fill NaN values    

            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant
                
        Returns:
            None
        """
        
        # compute for the Ultimate oscillator
        self.df[f'Ultimate{window1}'] = ta.momentum.ultimate_oscillator(
            high = self.df['High'], 
            low = self.df['Low'], 
            close = self.df['Close'], 
            window1 = window1, 
            window2 = window2, 
            window3 = window3, 
            weight1 = weight1, 
            weight2 = weight2, 
            weight3 = weight3, 
            fillna = fillna)
    
        # calculate the membership values for low, medium and high ultimate oscillator
        self.u[f'Ultimate{window1}_lo'] = self.df[f'Ultimate{window1}'].apply(lambda x: linearf(x, [0, 20], positive_slope = False))
        self.u[f'Ultimate{window1}_md'] = self.df[f'Ultimate{window1}'].apply(lambda x: trimf(x, [0, 50, 100])) 
        self.u[f'Ultimate{window1}_hi'] = self.df[f'Ultimate{window1}'].apply(lambda x: linearf(x, [80, 100], positive_slope = True))
        
        # the following are the fuzzy rules for ultimate oscillator
        # if ultimate is low, then buy
        self.z[f'Ultimate{window1}_lo'] = p0 + (p1 * ((self.u[f'Ultimate{window1}_lo'] * 25)  + 75))
        
        # if ultimate is medium and ultimate is below 50 then do this; borderlining to buying
        mask = (self.df[f'Ultimate{window1}'] < 50)
        self.z.loc[mask, f'Ultimate{window1}_md'] = p0 + (p1 * ((self.u[f'Ultimate{window1}_md'] * -25) + 75))
        
        # if ultimate is medium and ultimate is above or equal to  50 then do this; borderlining to selling
        mask = (self.df[f'Ultimate{window1}'] >= 50)
        self.z.loc[mask, f'Ultimate{window1}_md'] = p0 + (p1 * ((self.u[f'Ultimate{window1}_md'] * 25) + 25))

        # if ultimate is high then sell
        self.z[f'Ultimate{window1}_hi'] = p0 + (p1 * ((self.u[f'Ultimate{window1}_hi'] * -25) + 25))

    def TSI(self, window_slow:int = 25, window_fast:int = 13, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        True Strength Index
        
        Arguments:
            window_slow:int
                window for calculating the slow period
            
            window_fast:int
                window for calculating the slow period
            
            fillna: bool
                if True, fill NaN values

            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant

        Returns:
            None
        """

        # compute for the TSI of the stock
        self.df[f'TSI{window_slow}x{window_fast}'] = (ta.momentum.tsi(
            close = self.df['Close'],
            window_slow = 25,
            window_fast = 13,
            fillna = False)
        )

        # calculate the membership values for low, medium and high ultimate oscillator
        self.u[f'TSI{window_slow}x{window_fast}_lo'] = self.df[f'TSI{window_slow}x{window_fast}'].apply(lambda x: linearf(x, [-0.5, -0.25], positive_slope = False))
        self.u[f'TSI{window_slow}x{window_fast}_md'] = self.df[f'TSI{window_slow}x{window_fast}'].apply(lambda x: trimf(x, [-0.5, 0, 0.5])) 
        self.u[f'TSI{window_slow}x{window_fast}_hi'] = self.df[f'TSI{window_slow}x{window_fast}'].apply(lambda x: linearf(x, [0.25, 0.5], positive_slope = True))


        # the following are the fuzzy rules for ultimate oscillator
        # if TSI is low, then buy
        self.z[f'TSI{window_slow}x{window_fast}_lo'] = p0 + (p1 * ((self.u[f'TSI{window_slow}x{window_fast}_lo'] * 25)  + 75))
        
        # if TSI is medium, then hold
        self.z[f'TSI{window_slow}x{window_fast}_md'] = p0 + (p1 * (50))

        # if TSI is high then sell
        self.z[f'TSI{window_slow}x{window_fast}_hi'] = p0 + (p1 * ((self.u[f'TSI{window_slow}x{window_fast}_hi'] * -25) + 25))


    # VOLUME INDICATORS

    def CMF(self, window:int = 20, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Chaikin Money Flow
        
        Arguments:
            window:int
                window or number of elements to be included in the calculation of CMF

            fillna: bool
                if True, fill NaN values
            
            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant

        
        Returns:
            None
        """
        
        
        self.df[f'CMF{window}'] = (
            ta.volume.chaikin_money_flow(
                high = self.df['High'], 
                low = self.df['Low'], 
                close = self.df['Close'], 
                volume = self.df['Volume'], 
                window = window, 
                fillna = fillna)
            )

        # CMF_val = self.df[f'CMF{window}'].iloc[-1]
        
        # calculate the membership values for low, medium and high CMF
        self.u[f'CMF{window}_lo'] = self.df[f'CMF{window}'].apply(lambda x: linearf(x, [-1, 0], positive_slope = False))
        self.u[f'CMF{window}_md'] = self.df[f'CMF{window}'].apply(lambda x: trimf(x, [-1, 0, 1])) 
        self.u[f'CMF{window}_hi'] = self.df[f'CMF{window}'].apply(lambda x: linearf(x, [0, 1], positive_slope = True))        
        
        # the following are the fuzzy rules for CMF
        # if CMF_val is negative then buy
        self.z[f'CMF{window}_lo'] = p0 + (p1 * ((self.u[f'CMF{window}_lo'] * 25)  + 75))
        
        # if CMF is medium and ultimate is below 0 then do this; borderlining to buying
        mask = (self.df[f'CMF{window}'] < 0)
        self.z.loc[mask, f'CMF{window}_md'] = p0 + (p1 * ((self.u[f'CMF{window}_md'] * -25) + 75))
        
        # if CMF is medium and ultimate is above or equal to  0 then do this; borderlining to selling
        mask = (self.df[f'CMF{window}'] >= 0)
        self.z.loc[mask, f'CMF{window}_md'] = p0 + (p1 * ((self.u[f'CMF{window}_md'] * 25) + 25))

        # if CMF is high then sell
        self.z[f'CMF{window}_hi'] = p0 + (p1 * ((self.u[f'CMF{window}_hi'] * -25) + 25))
        
    def MFI(self, window:int = 14, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Money Flow Index
        
        Arguments:
            window:int
                window or number of elements to be included in the calculation of MFI
            
            fillna: bool
                if True, fill NaN values
            
            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant

        Returns:
            None
        """
        # calculate the money flow index for the window
        self.df[f'MFI{window}'] = (
            ta.volume.MFIIndicator(
                high = self.df['High'], 
                low = self.df['Low'], 
                close = self.df['Close'], 
                volume = self.df['Volume'], 
                window = window, 
                fillna = fillna)
            .money_flow_index()
        )
        
        # calculate the membership values for low, medium and high MFI
        self.u[f'MFI{window}_lo'] = self.df[f'MFI{window}'].apply(lambda x: linearf(x, [0, 20], positive_slope = False))
        self.u[f'MFI{window}_md'] = self.df[f'MFI{window}'].apply(lambda x: trimf(x, [0, 50, 100])) 
        self.u[f'MFI{window}_hi'] = self.df[f'MFI{window}'].apply(lambda x: linearf(x, [80, 100], positive_slope = True))


        # the following are the fuzzy rules for MFI
        # if CMF_val is negative then buy
        self.z[f'MFI{window}_lo'] = p0 + (p1 * ((self.u[f'MFI{window}_lo'] * 25)  + 75))
        
        # if CMF is medium and ultimate is below 0 then do this; borderlining to buying
        mask = (self.df[f'MFI{window}'] < 0)
        self.z.loc[mask, f'MFI{window}_md'] = p0 + (p1 * ((self.u[f'MFI{window}_md'] * -25) + 75))
        
        # if CMF is medium and ultimate is above or equal to  0 then do this; borderlining to selling
        mask = (self.df[f'MFI{window}'] >= 0)
        self.z.loc[mask, f'MFI{window}_md'] = p0 + (p1 * ((self.u[f'MFI{window}_md'] * 25) + 25))

        # if CMF is high then sell
        self.z[f'MFI{window}_hi'] = p0 + (p1 * ((self.u[f'MFI{window}_hi'] * -25) + 25))
            
    def RSI_OBV(self, window:int = 14, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Relative Stregth Index as applied on the On Balance Volume
        
        Arguments:
            window:
                window or number of elements to be included in the calculation of RSI_OBV

            fillna: bool
                if True, fill NaN values
                
            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant
        
        Returns:
            None
        
        """

        # compute for OBV
        self.df['OBV'] = (
            ta.volume.OnBalanceVolumeIndicator(
                close = self.df['Close'], 
                volume = self.df['Volume'], 
                fillna = False)
            .on_balance_volume()
        )

        # normalize OBV
        volume_sum = self.df['OBV'].sum()
        self.df['OBV'] = (self.df['OBV']/volume_sum)*100

        # compute for the RSI of the stock
        self.df[f'RSI_OBV{window}'] = (
            ta.momentum.RSIIndicator(
                close = self.df['OBV'], 
                window = window, 
                fillna = fillna)
            .rsi()
        )
        
        # calculate the membership values for low, medium and high RSI_OBV
        self.u[f'RSI_OBV{window}_lo'] = self.df[f'RSI_OBV{window}'].apply(lambda x: linearf(x, [0, 20], positive_slope = False))
        self.u[f'RSI_OBV{window}_md'] = self.df[f'RSI_OBV{window}'].apply(lambda x: trimf(x, [0, 50, 100])) 
        self.u[f'RSI_OBV{window}_hi'] = self.df[f'RSI_OBV{window}'].apply(lambda x: linearf(x, [80, 100], positive_slope = True))
        
        # the following are the fuzzy rules for RSI_OBV
        # if RSI_OBV is low then buy
        self.z[f'RSI_OBV{window}_lo'] = p0 + (p1 * ((self.u[f'RSI_OBV{window}_lo'] * 25)  + 75))
        
        # if RSI_OBV is medium and RSI_OBV is below 50 then do this; borderlining to buying
        mask = (self.df[f'RSI_OBV{window}'] < 50)
        self.z.loc[mask, f'RSI_OBV{window}_md'] = p0 + (p1 * ((self.u[f'RSI_OBV{window}_md'] * -25) + 75))
        
        # if RSI_OBV is medium and RSI_OBV is above or equal to  50 then do this; borderlining to selling
        mask = (self.df[f'RSI_OBV{window}'] >= 50)
        self.z.loc[mask, f'RSI_OBV{window}_md'] = p0 + (p1 * ((self.u[f'RSI_OBV{window}_md'] * 25) + 25))

        # if RSI_OBV is high then sell
        self.z[f'RSI_OBV{window}_hi'] = p0 + (p1 * ((self.u[f'RSI_OBV{window}_hi'] * -25) + 25))
    
    def StochOBV_KxD(self, window:int = 14, smooth1:int = 1, smooth2:int =3, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Stochastic OBV
        
            This method computes for the stochastic OBV 
            k is the slow indicator
            d is the fast indicator
        
        Arguments:
            window: int
                the window used in computing the stochastic OBV
                
            smooth1: int
                first smoothing factor used in computing stochastic OBV
                
            smooth2: int
                second smoothing factor used in computing stochastic OBV
                
            fillna: bool
                if True, fill NaN values

            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant

        Returns:
            None
        """
        
        # compute for OBV
        self.df['OBV'] = (
            ta.volume.OnBalanceVolumeIndicator(
                close = self.df['Close'], 
                volume = self.df['Volume'], 
                fillna = False)
            .on_balance_volume()
        )

        # normalize OBV
        volume_sum = self.df['OBV'].sum()
        self.df['OBV'] = (self.df['OBV']/volume_sum)*100
        
        # compute for the stochastic of OBV
        self.df[f'StochOBV_d{window}'] = (
            ta.momentum.StochRSIIndicator(
                close = self.df['OBV'],
                window = window,
                smooth1 = smooth1,
                smooth2 = smooth2,
                fillna = fillna)
            .stochrsi_d()
        )
        self.df[f'StochOBV_k{window}'] = (
            ta.momentum.StochRSIIndicator(
                close = self.df['OBV'],
                window = window,
                smooth1 = smooth1,
                smooth2 = smooth2,
                fillna = fillna)
            .stochrsi_k()
        )
        
        # compute for the KxD difference
        KxD_diff =  self.df[f'StochOBV_k{window}'] - self.df[f'StochOBV_d{window}']

        # calculate the membership values for low, medium and high RSI
        self.u[f'StochOBV_KxD{window}_neg'] = KxD_diff.apply(lambda x: linearf(x, [-0.4, 0], positive_slope = False))
        self.u[f'StochOBV_KxD{window}_zero'] = KxD_diff.apply(lambda x: trimf(x, [-0.4, 0, 0.4])) 
        self.u[f'StochOBV_KxD{window}_pos'] = KxD_diff.apply(lambda x: linearf(x, [0, 0.4], positive_slope = True))
        
        # the following are the fuzzy rules for PPO
        # if PPO_hist is postive then buy
        self.z[f'StochOBV_KxD{window}_pos'] = p0 + (p1 * ((self.u[f'StochOBV_KxD{window}_pos'] * 25) + 75))
        
        # if PPO_hist is zero
        mask = (KxD_diff > 0)
        # if KxD_diff is above  0, then lean towards buying
        self.z.loc[mask, f'StochOBV_KxD{window}_zero'] = p0 + (p1 * ((self.u[f'StochOBV_KxD{window}_zero'] * -25) + 75))

        mask = (KxD_diff <= 0)
        # if KxD_diff is less than or equal to  0, then lean towards selling
        self.z.loc[mask, f'StochOBV_KxD{window}_zero'] = p0 + (p1 * ((self.u[f'StochOBV_KxD{window}_zero'] * 25) + 25))

        # if KxD_diff is negative then sell
        self.z[f'StochOBV_KxD{window}_neg'] = p0 + (p1 * ((self.u[f'StochOBV_KxD{window}_neg'] * -25) + 25))
        
    # VOLATILITY INDICATORS
    def BB_pband(self, window:int = 20, window_dev:int = 2, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Bolinger percentage band
        
        Arguments:
            window: int
                window or number of elements to be included in the calculation of BB_pband

            window_dev:int
                n factor standard deviation

            fillna: bool
                if True, fill NaN values
                
            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model; this will act as a weighing constant
        
        Returns:
            None
        """
        
        self.df[f'BB_pband{window}'] = (ta.volatility.bollinger_pband(
            close = self.df['Close'], 
            window = window, 
            window_dev = window_dev, 
            fillna = fillna)
        )

        
        # calculate the membership values for low, medium and high RSI
        self.u[f'BB_pband{window}_lo'] = self.df[f'BB_pband{window}'].apply(lambda x: linearf(x, [-0.2, 0], positive_slope = False))
        self.u[f'BB_pband{window}_md'] = self.df[f'BB_pband{window}'].apply(lambda x: trimf(x, [0, 0.5, 1])) 
        self.u[f'BB_pband{window}_hi'] = self.df[f'BB_pband{window}'].apply(lambda x: linearf(x, [1, 1.2], positive_slope = True))
        

        # the following are the fuzzy rules for BB_pband
        # if BB_pband is low then buy
        self.z[f'BB_pband{window}_lo'] = p0 + (p1 * ((self.u[f'BB_pband{window}_lo'] * 25) + 75))
        
        # if BB_pband is low
        mask = self.df[f'BB_pband{window}'] < 0
        # if BB_pband is less than 0, then lean towards buying
        self.z.loc[mask, f'BB_pband{window}_md'] = p0 + (p1 * ((self.u[f'BB_pband{window}_md'] * -25) + 75))

        mask = self.df[f'BB_pband{window}'] >= 0
        # if BB_pband is greater than or equal to  0, then lean towards selling
        self.z.loc[mask, f'BB_pband{window}_md'] = p0 + (p1 * ((self.u[f'BB_pband{window}_md'] * 25) + 25))

        # if BB_pband is high then sell
        self.z[f'BB_pband{window}_hi'] = p0 + (p1 * ((self.u[f'BB_pband{window}_hi'] * -25) + 25))
        
    # TREND INDICATORS
    
    def MACD(self, window_fast:int = 12, window_slow:int = 26, window_sign:int = 9, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        
        Arguments:
            window_fast: int
                some text
            
            window_slow: int
                some text

            window_sign: int
                some text
                
            fillna: bool
                some text
            
            p0: float
                some text
                
            p1: float
                some text
            
        Returns:
            None
        """
    
    
        # compute for MACD Line
        self.df[f'MACD{window_fast}_{window_slow}_line'] = (
            ta.trend.MACD(
                close = self.df['Close'], 
                window_fast = window_fast,
                window_slow = window_slow,
                window_sign = window_sign, 
                fillna = False)
            .macd()
        )
        
        # compute for MACD Difference
        self.df[f'MACD{window_fast}_{window_slow}_diff'] = (
            ta.trend.MACD(
                close = self.df['Close'], 
                window_fast = window_fast,
                window_slow = window_slow,
                window_sign = window_sign, 
                fillna = False)
            .macd_diff()
        )
        
        # compute for MACD signal
        self.df[f'MACD{window_fast}_{window_slow}_signal'] = (
            ta.trend.MACD(
                close = self.df['Close'], 
                window_fast = window_fast,
                window_slow = window_slow,
                window_sign = window_sign, 
                fillna = False)
            .macd_signal()
        )
        # set the index in u and z
        self.u = pd.DataFrame(index = self.df.index )
        self.z = pd.DataFrame(index = self.df.index )
 
        # get mask
        mask = (self.df[f'MACD{window_fast}_{window_slow}_signal'] < self.df[f'MACD{window_fast}_{window_slow}_line'])
        
        # this rule sets the buying condition of the MACD rule
        self.u.loc[mask, f'MACD{window_fast}_{window_slow}_lo'] = 0
        self.u.loc[mask, f'MACD{window_fast}_{window_slow}_hi'] = 1
        self.z.loc[mask, f'MACD{window_fast}_{window_slow}_lo'] = p1 * 0
        self.z.loc[mask, f'MACD{window_fast}_{window_slow}_hi'] = p1 * 100
        
        # get mask
        mask = (self.df[f'MACD{window_fast}_{window_slow}_signal'] > self.df[f'MACD{window_fast}_{window_slow}_line'])
        
        # this rule sets the selling condition of the MACD rule
        self.u.loc[mask, f'MACD{window_fast}_{window_slow}_lo'] = 1
        self.u.loc[mask, f'MACD{window_fast}_{window_slow}_hi'] = 0
        self.z.loc[mask, f'MACD{window_fast}_{window_slow}_lo'] = p1 * 0
        self.z.loc[mask, f'MACD{window_fast}_{window_slow}_hi'] = p1 * 100


    def CCI(self, window:int = 20, constant:float = 0.0015, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Compute for the commodity channel index
        
        Arguments:
            window: int
                some text

            constant:float
                some text

            fillna: bool
                if True, fill NaN values
                
            p0: float
                a constant to be passed in the consequent of the Tsukamoto model
            
            p1: float
                a constant to be passed in the consequent of the Tsukamoto model
        
        Returns:
            None
        """
        # compute for the commodity channel index
        self.df[f'CCI{window}'] = (
            ta.trend.CCIIndicator(
                high = self.df['High'],
                low = self.df['Low'],
                close = self.df['Close'],
                window = window,
                constant = constant,
                fillna = fillna)
            .cci()
        )

    
        # calculate the membership values for low, medium and high CCI
        self.u[f'CCI{window}_lo'] = self.df[f'CCI{window}'].apply(lambda x: linearf(x, [-200, -100], positive_slope = False))
        self.u[f'CCI{window}_md'] = self.df[f'CCI{window}'].apply(lambda x: trimf(x, [-200, 0, 200])) 
        self.u[f'CCI{window}_hi'] = self.df[f'CCI{window}'].apply(lambda x: linearf(x, [100, 200], positive_slope = True))
        
        # the following are the fuzzy rules for CCI
        # if BB_pband is low then buy
        self.z[f'CCI{window}_lo'] = p0 + (p1 * ((self.u[f'CCI{window}_lo'] * 25) + 75))
        
        # if CCI is low
        mask = self.df[f'CCI{window}'] < 0
        # if CCI is less than 0, then lean towards buying
        self.z.loc[mask, f'CCI{window}_md'] = p0 + (p1 * ((self.u[f'CCI{window}_md'] * -25) + 75))

        mask = self.df[f'CCI{window}'] >= 0
        # if CCI is greater than or equal to  0, then lean towards selling
        self.z.loc[mask, f'CCI{window}_md'] = p0 + (p1 * ((self.u[f'CCI{window}_md'] * 25) + 25))

        # if CCI is high then sell
        self.z[f'CCI{window}_hi'] = p0 + (p1 * ((self.u[f'CCI{window}_hi'] * -25) + 25))
    
    def STC(self, window_slow:int = 50, window_fast:int = 30, cycle:int = 30, smooth1:int = 3, smooth2:int = 3, fillna = False, p0:float = 0, p1:float = 1) -> None:
        """
        Schaff Trend Cycle
        
        Arguments:
            window_slow:int
                some text

            window_fast:int
                some text

            cycle:int
                some text
            
            smooth1:int
                some text

            smooth2:int
                some text
            
            fillna: bool
                if True, fill NaN values

            p0: int
                a constant to be passed in the consequent of the Tsukamoto model

            p1: int
                a constant to be passed in the consequent of the Tsukamoto model
                
        Returns:
            None
        """
        
        self.df[f'STC{window_slow}'] = (
            ta.trend.STCIndicator(
                close = self.df['Close'],
                window_slow = window_slow,
                window_fast = window_fast,
                cycle = cycle,
                smooth1 = smooth1,
                smooth2 = smooth2,
                fillna = fillna)
            .stc()
        )
        
        # calculate the membership values for low, medium and high CCI
        self.u[f'STC{window_slow}_lo'] = self.df[f'STC{window_slow}'].apply(lambda x: linearf(x, [0, 20], positive_slope = False))
        self.u[f'STC{window_slow}_md'] = self.df[f'STC{window_slow}'].apply(lambda x: trimf(x, [0, 50, 100])) 
        self.u[f'STC{window_slow}_hi'] = self.df[f'STC{window_slow}'].apply(lambda x: linearf(x, [80, 100], positive_slope = True))
        
        # the following are the fuzzy rules for CCI
        # if BB_pband is low then buy
        self.z[f'STC{window_slow}_lo'] = p0 + (p1 * ((self.u[f'STC{window_slow}_lo'] * 25) + 75))
        
        # if CCI is low
        mask = self.df[f'STC{window_slow}'] < 50
        # if CCI is less than 0, then lean towards buying
        self.z.loc[mask, f'STC{window_slow}_md'] = p0 + (p1 * ((self.u[f'STC{window_slow}_md'] * -25) + 75))

        mask = self.df[f'STC{window_slow}'] >= 50
        # if CCI is greater than or equal to  0, then lean towards selling
        self.z.loc[mask, f'STC{window_slow}_md'] = p0 + (p1 * ((self.u[f'STC{window_slow}_md'] * 25) + 25))

        # if CCI is high then sell
        self.z[f'STC{window_slow}_hi'] = p0 + (p1 * ((self.u[f'STC{window_slow}_hi'] * -25) + 25))
        
    def PSAR(self, step:float = 0.02, max_step:float = 0.2, fillna:bool = False, p0:float = 0, p1:float = 1) -> None:
        """
        Parabolic SAR
        
        Arguments:        
            step:float
                some text
                
            max_step:float
                some text
                
            fillna: bool
                if True, fill NaN values
            
            p0:float
                a constant to be passed in the consequent of the Tsukamoto model

            p1:float
                a constant to be passed in the consequent of the Tsukamoto model

        Returns:
            None
        """
        
        # parabolic SAR
        self.df[f'PSAR{step}{max_step}'] = (ta.trend.PSARIndicator(
            high = self.df['High'],
            low = self.df['Low'],
            close = self.df['Close'],
            step = step,
            max_step = max_step,
            fillna = fillna)
            .psar()
        )
         
        # crude implementation of the PSAR rule
        # this rule defines the sell rule
        mask = (self.df[f'PSAR{step}{max_step}'] > self.df[f'Close'])
        self.u.loc[mask, f'PSAR{step}{max_step}_lo'] = 1
        self.u.loc[mask, f'PSAR{step}{max_step}_hi'] = 0
        self.z.loc[mask, f'PSAR{step}{max_step}_lo'] = p1 * 0
        self.z.loc[mask, f'PSAR{step}{max_step}_hi'] = p1 * 100
        
        # crude implementation of the PSAR rule
        # this rule defines the buy rule
        mask = (self.df[f'PSAR{step}{max_step}'] < self.df[f'Close'])
        self.u.loc[mask, f'PSAR{step}{max_step}_lo'] = 0
        self.u.loc[mask, f'PSAR{step}{max_step}_hi'] = 1
        self.z.loc[mask, f'PSAR{step}{max_step}_lo'] = p1 * 0
        self.z.loc[mask, f'PSAR{step}{max_step}_hi'] = p1 * 100

    # OTHER INDICATORS
    
    def Fisher_trans(self, window: int = 14, smooth2: int = 3, adjust: bool = True, p0 = 0, p1 = 1) -> None:
        """
        Fisher Transform
        
        Arguments:
            window: int
                some text
            
            smooth2: int
                some text
            
            adjust: bool
                some text
            
            fillna: bool
                if True, fill NaN values
            
            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model

        Returns
            None
        """
        
        np.seterr(divide='ignore')

        med = (self.df['High'] + self.df['Low']) / 2
        ndaylow = med.rolling(window=window).min()
        ndayhigh = med.rolling(window=window).max()
        raw = (2 * ((med - ndaylow) / (ndayhigh - ndaylow))) - 1
        smooth = raw.ewm(span=5, adjust=adjust).mean()
        _smooth = smooth.fillna(0)
        
        self.df[f'Fisher{window}'] = (
            (np.log((1 + _smooth) / (1 - _smooth)))
            .ewm(span=3, adjust=adjust)
            .mean()
        )
        
        # calculate the membership values for low, medium and high Fisher
        self.u[f'Fisher{window}_lo'] = self.df[f'Fisher{window}'].apply(lambda x: linearf(x, [-4, 0], positive_slope = False))
        self.u[f'Fisher{window}_md'] = self.df[f'Fisher{window}'].apply(lambda x: trimf(x, [-2, 0, 2])) 
        self.u[f'Fisher{window}_hi'] = self.df[f'Fisher{window}'].apply(lambda x: linearf(x, [0, 4], positive_slope = True))
        
        # the following are the fuzzy rules for Fisher
        # if Fisher is low, then buy
        self.z[f'Fisher{window}_lo'] = p0 + (p1 * ((self.u[f'Fisher{window}_lo'] * 25)  + 75))
        
        # if Fisher is medium and Fisher is less than 0, then buy
        mask = (self.df[f'Fisher{window}'] < 0)
        self.z.loc[mask, f'Fisher{window}_md'] = p0 + (p1 * ((self.u[f'Fisher{window}_md'] * -25) + 75))
        
        # if Fisher is medium and Fisher is more than 0, then sell
        mask = (self.df[f'Fisher{window}'] >= 0)
        self.z.loc[mask, f'Fisher{window}_md'] = p0 + (p1 * ((self.u[f'Fisher{window}_md'] * 25) + 25))

        # if Fisher is high then sell
        self.z[f'Fisher{window}_hi'] = p0 + (p1 * ((self.u[f'Fisher{window}_hi'] * -25) + 25))
    
    def Fisher_trans_KxD(self, window: int = 14, smooth2: int = 3, adjust: bool = True, weekly = False, monthly = False, p0 = 0, p1 = 1) -> None:
        """
        Fisher Transformation Cross
        
        Arguments:
            fillna: bool
                if True, fill NaN values
            
            p0: float
                a constant to be passed in the consequent of the Tsukamoto model

            p1: float
                a constant to be passed in the consequent of the Tsukamoto model
                
        Returns
            None
        """
        
        np.seterr(divide='ignore')

        med = (self.df['High'] + self.df['Low']) / 2
        ndaylow = med.rolling(window=window).min()
        ndayhigh = med.rolling(window=window).max()
        raw = (2 * ((med - ndaylow) / (ndayhigh - ndaylow))) - 1
        smooth = raw.ewm(span=5, adjust=adjust).mean()
        _smooth = smooth.fillna(0)

        # compute for the k and d smoothed fisher transforms
        fish_series_k = (np.log((1 + _smooth) / (1 - _smooth))).ewm(span=3, adjust=adjust).mean()
        fish_series_d = fish_series_k.rolling(smooth2).mean()
        
        # compute for the KxD difference
        KxD_diff = fish_series_k - fish_series_d
        
        # calculate the membership values for low, medium and high KxD_diff
        self.u[f'Fisher_KxD{window}_neg'] = KxD_diff.apply(lambda x: linearf(x, [-0.25, 0], positive_slope = False))
        self.u[f'Fisher_KxD{window}_zero'] = KxD_diff.apply(lambda x: trimf(x, [-0.13, 0, 0.13])) 
        self.u[f'Fisher_KxD{window}_pos'] = KxD_diff.apply(lambda x: linearf(x, [0, 0.25], positive_slope = True))
        
        # the following are the fuzzy rules for KxD_diff
        # if KxD_diff is postive then buy
        self.z[f'Fisher_KxD{window}_pos'] = p0 + (p1 * ((self.u[f'Fisher_KxD{window}_pos'] * 25) + 75))
        
        # if KxD_diff is zero
        mask = (KxD_diff > 0)
        # if KxD_diff is above 0, then lean towards buying
        self.z.loc[mask, f'Fisher_KxD{window}_zero'] = p0 + (p1 * ((self.u[f'Fisher_KxD{window}_zero'] * -25) + 75))

        mask = (KxD_diff <= 0)
        # if KxD_diff is less than or equal to  0, then lean towards selling
        self.z.loc[mask, f'Fisher_KxD{window}_zero'] = p0 + (p1 * ((self.u[f'Fisher_KxD{window}_zero'] * 25) + 25))

        # if KxD_diff is negative then sell
        self.z[f'Fisher_KxD{window}_neg'] = p0 + (p1 * ((self.u[f'Fisher_KxD{window}_neg'] * -25) + 25))
    
    
    def z_total(self):
        """
        Computes for the total z value for the consequent of the Tsukamoto model
        
        Arguments:        
            self
                the instance of the class
        
        Returns:
        """
        
        # add all u along axis 1 or the column
        self.u_sum['sum'] = self.u.sum(axis = 1)
        
        # initialize z_sum to be 0
        self.z['z_sum'] = 0
        
        # add all values of z across different technical indicator
        for col_name in self.u.columns:
            # produce mask that would remove NANs in the dataframe
            mask = ~(self.z['z_sum'] + (self.z[f'{col_name}'] * self.u[f'{col_name}'])).isna()
            
            # apply mask
            self.z.loc[mask, 'z_sum'] = self.z['z_sum'] + (self.z[f'{col_name}'] * self.u[f'{col_name}'])
        
        # compute for the normalized z_sum by u_sum
        self.df['z_sum'] = self.z['z_sum'] / self.u_sum['sum']
    