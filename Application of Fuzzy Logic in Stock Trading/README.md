# Application of Fuzzy Logic to Stock Trading

This project explores the application of fuzzy logic (in particular, the Tsukamoto fuzzy inference model) in stock trading. This notebook uses multiple technical indicators and consolidates them through fuzzy logic and inferes either a buy, hold, or sell signal for a particular stock (through the Tsukamoto inference model).

## Methodology

The stock used in this study was the historical stock price data of Globe Telecommunications, Incorporated (a publicly listed company in the Philippines). The coverage of the historical stock price data was from 1986 up until 2023.

### Technical Indicators

The technical indicators used for this study are the following:

#### I. Momentum indicators
1. Relative Strength Index
2. Stochastic RSI
3. Williams R
4. Ultimate
5. True Strength Index

#### II. Volume indicator

1. Chaikin Money Flow
2. Money Flow Index
3. Stochastic On-Balance Volume
4. RSI On-Balance Volume

#### III. Volatility Indicator

1. Bollinger Percentage Band

#### IV. Trend indicators

1. Commodity Channel Index
2. Schaff Trend Cycle
3. Parabolic SAR

#### V. Other indicators

1. Fisher transform

### Fuzzy Inference System

Inference is made through the use of the Tsukamoto inference model. To do this, the outputs of the abovementioned technical indicators are fuzzified and their membership values in "small", "medium", or "high" partitions are computed. The consequent is then computed using a monotonically increaseing or decreasing function; computation of the consequent produces the corresponding values for buy, hold, or sell signals. 

For example, for any given value of RSI (antecedent), its membership values is computed for buy, hold, or sell (consequent). 

## Conclusions and Recommendations
1. The model seems to show that it generates higher returns for the particular stock studies; however, this is not a strong indication that the model can beat the buy-and hold strategy in general. Further investigation is needed to assess the model if it is able to generalize to other stocks (initial investigations shows that the model performs poorly on other stocks; a much more quantitative analysis is needed to further assess the performance of the model)
2. It is recommended to optimize the hyperparameters of the model (e.g. the windows used in the computation of the technical indicators, the nodes for the fuzzification and inference layers, and the signals for buy, hold or sell). This can be done through the use of genetic algorithms to search for the optimal hyperparameters. 
3. It is recommended to investigate other machine learning models and their application in stock trading. Other relatively easy models to create are multi-layer perceptrons and clustering methods. Deep learning models could also be investigated, but it is recommended to explore first the much more simpler models before proceeding to much more complex models.
4. With the given strategy, it is recommended to investage its use in conjuction with a portfolio optimization model (e.g. optimal-F model) to see and check its performance.

If you find this interesting, please feel free to send me an email at riokatipunan@gmail.com.

Thank you!
