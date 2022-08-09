import ccxt
import databutton as db
import pandas as pd
import ta
import numpy as np


# Making it easy to register a new strategy 
list_of_strategies = dict()
def register_indicator(name):
    def F(func):
        list_of_strategies[name] = func
        return func
    return F



#Register the strategy using a decorator
@register_indicator('MACD with RSI')
def macdrsi_indicator(ticker):
    #Define exchange
    ftx = ccxt.ftx()
    ftx.load_markets()

    #Fetch candle data
    candle = ftx.fetchOHLCV(ticker, '1h')
    df = pd.DataFrame(data=candle, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Date'] = pd.to_datetime(df.Date, unit='ms')

    #start eval
    macd_result, final_result = 'WAIT','WAIT'

    # BUY or SELL based on MACD crossover points and the RSI value at that point
    M = ta.trend.MACD(df['Close'], window_fast = 12, window_slow = 26, window_sign = 9)
    macd = M.macd()
    hist = M.macd_diff() 
    signal= M.macd_signal() 

    last_hist = hist.iloc[-1]
    prev_hist = hist.iloc[-2]
    if not np.isnan(prev_hist) and not np.isnan(last_hist):
        # If hist value has changed from negative to positive or vice versa, it indicates a crossover
        macd_crossover = (abs(last_hist + prev_hist)) != (abs(last_hist) + abs(prev_hist))
        if macd_crossover:
            macd_result = 'BUY' if last_hist > 0 else 'SELL'
            
        if macd_result != 'WAIT':
            rsi = ta.momentum.rsi(df['Close'], window = 14)
            last_rsi = rsi.iloc[-1]

            if (last_rsi <= 30):
                final_result = 'BUY'
            elif (last_rsi >= 70):
                final_result = 'SELL'

    
    return final_result


#Register the strategy using a decorator
@register_indicator('MACD')
def macd_indicator(ticker):
    #Define exchange
    ftx = ccxt.ftx()
    ftx.load_markets()

    #Fetch candle data
    candle = ftx.fetchOHLCV(ticker, '1h')
    df = pd.DataFrame(data=candle, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Date'] = pd.to_datetime(df.Date, unit='ms')

    #start eval
    macd_result, final_result = 'WAIT','WAIT'

    # BUY or SELL based on MACD crossover points and the RSI value at that point
    M = ta.trend.MACD(df['Close'], window_fast = 12, window_slow = 26, window_sign = 9)
    macd = M.macd()
    hist = M.macd_diff() 
    signal= M.macd_signal() 

    last_hist = hist.iloc[-1]
    prev_hist = hist.iloc[-2]
    if not np.isnan(prev_hist) and not np.isnan(last_hist):
        # If hist value has changed from negative to positive or vice versa, it indicates a crossover
        macd_crossover = (abs(last_hist + prev_hist)) != (abs(last_hist) + abs(prev_hist))
        if macd_crossover:
            macd_result = 'BUY' if last_hist > 0 else 'SELL'
            
    return macd_result



#Register the strategy using a decorator
@register_indicator('RSI')
def rsi_indicator(ticker):
    #Define exchange
    ftx = ccxt.ftx()
    ftx.load_markets()

    #Fetch candle data
    candle = ftx.fetchOHLCV(ticker, '1h')
    df = pd.DataFrame(data=candle, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Date'] = pd.to_datetime(df.Date, unit='ms')

    #start eval
    final_result = 'WAIT','WAIT'
    rsi = ta.momentum.rsi(df['Close'], window = 14)
    last_rsi = rsi.iloc[-1]

    if (last_rsi <= 30):
        final_result = 'BUY'
    elif (last_rsi >= 70):
        final_result = 'SELL'
    
    return final_result


#Register the strategy using a decorator
@register_indicator('Stochastic Oscillator')
def stochastic_indicator(ticker):
    #Define exchange
    ftx = ccxt.ftx()
    ftx.load_markets()

    #Fetch candle data
    candle = ftx.fetchOHLCV(ticker, '1h')
    df = pd.DataFrame(data=candle, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Date'] = pd.to_datetime(df.Date, unit='ms')

    #start eval
    final_result = 'WAIT','WAIT'
    si = ta.momentum.stoch_signal(df.High, df.Low, df.Close)
    last_si = si.iloc[-1]

    if (last_si <= 20):
        final_result = 'BUY'
    elif (last_si >= 80):
        final_result = 'SELL'
    
    return final_result



#Register the strategy using a decorator
@register_indicator(name='My Cool Strategy')  
def my_cool_indicator(ticker):
    # Write your code here
    return 'BUY'
