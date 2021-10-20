import numpy as np
import pandas as pd
import requests
import yfinance as yf
from datetime import datetime
import warnings
import schedule
import time
import pandas_ta as ta

warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def datetotimestamp(date):
    time_tuple = date.timetuple()
    timestamp = round(time.mktime(time_tuple))
    return timestamp


def timestamptodate(timestamp):
    return datetime.fromtimestamp(timestamp)


def Stock_data(stock='SBIN', period='6d', interval='5m'):
    ticker = yf.Ticker("{}.NS".format(stock))
    data = ticker.history(period=period, interval=interval)
    return data


def atr(data, period):
    data['previous_close'] = data['Close'].shift(1)
    data['high-low'] = abs(data['High'] - data['Low'])
    data['high-pc'] = abs(data['High'] - data['previous_close'])
    data['low-pc'] = abs(data['Low'] - data['previous_close'])
    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    data['tr'] = tr
    atr = data['tr'].rolling(period).mean()
    data['atr'] = atr
    return atr


def supertrend(data, period=7, atr_multiplier=3):
    hl2 = (data['High'] + data['Low']) / 2
    data['atr'] = atr(data, period)
    data['upperband'] = hl2 + (atr_multiplier * data['atr'])
    data['lowerband'] = hl2 - (atr_multiplier * data['atr'])
    data['in_uptrend'] = True

    for current in range(1, len(data.index)):
        previous = current - 1
        if data['Close'][current] > data['upperband'][previous]:
            data['in_uptrend'][current] = True
        elif data['Close'][current] < data['lowerband'][previous]:
            data['in_uptrend'][current] = False
        else:
            data['in_uptrend'][current] = data['in_uptrend'][previous]

            if data['in_uptrend'][current] and data['lowerband'][current] < data['lowerband'][previous]:
                data['lowerband'][current] = data['lowerband'][previous]

            if not data['in_uptrend'][current] and data['upperband'][current] > data['upperband'][previous]:
                data['upperband'][current] = data['upperband'][previous]
    data['ST_trend'] = 'NaN'
    for current in range(len(data.index)):
        if data['in_uptrend'][current] == True:
            data['ST_trend'][current] = "Buy"
        elif data['in_uptrend'][current] == False:
            data['ST_trend'][current] = "Short"

    return data


def adx(data):
    adx = ta.adx(data["High"], data['Low'], data['Close'])
    data = pd.concat([data, adx], axis=1).reindex(data.index)
    data['adx_indicator'] = 'Nan'

    for i in range(len(data.index)):
        if data['ADX_14'][i] >= 25:
            if data['DMP_14'][i] > data['DMN_14'][i]:
                data['adx_indicator'][i] = "STRONG UPTREND"
                if data['adx_indicator'][i - 1] == "STRONG UPTREND" or "⏫ UPTREND" and data['ADX_14'][i] > \
                        data['ADX_14'][i - 1]:
                    data['adx_indicator'][i] = "⏫ UP-TREND"
                elif data['adx_indicator'][i - 1] == "STRONG UPTREND" or "⏬ UPTREND" and data['ADX_14'][i] < \
                        data['ADX_14'][i - 1]:
                    data['adx_indicator'][i] = "⏬ UP-TREND"
            elif data['DMN_14'][i] > data['DMP_14'][i]:
                data['adx_indicator'][i] = "STRONG DOWNTREND"
                if data['adx_indicator'][i - 1] == "STRONG DOWNTREND" or "⏫ DOWNTREND" and data['ADX_14'][i] > \
                        data['ADX_14'][i - 1]:
                    data['adx_indicator'][i] = "⏫ DOWN-TREND"
                elif data['adx_indicator'][i - 1] == "STRONG DOWNTREND" or "⏬ DOWNTREND" and data['ADX_14'][i] < \
                        data['ADX_14'][i - 1]:
                    data['adx_indicator'][i] = "⏬ DOWN-TREND"

        elif data['ADX_14'][i] < 25:
            data['adx_indicator'][i] = "NO-TREND"

    return data


def run_bot():
    print(f"Fetched data of at {datetime.now().isoformat()}")
    data = Stock_data(stock='MRF')
    print(data)
    st = supertrend(data)
    adx1 = adx(st)
    #print(adx1[['Close', 'ST_trend', 'adx_indicator']])
    print('I am working.......')


schedule.every(2).seconds.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)

    