import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
import schedule
import time
import pandas_ta as ta
import smtplib
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def Stock_data(stock, period='5d', interval='5m'):
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


def sma(data):
    data['SMA 6'] = data['Close'].rolling(6).mean()
    data['SMA 20'] = data['Close'].rolling(20).mean()
    data['SMA_Indicator'] = 'NaN'
    for i in range(len(data.index)):
        if data['SMA 6'][i] > data['SMA 20'][i]:
            data['SMA_Indicator'][i] = "Buy"
        elif data['SMA 20'][i] > data['SMA 6'][i]:
            data['SMA_Indicator'][i] = "Short"
        else:
            data['SMA_Indicator'][i] = np.NAN

    return data


def macd(data):
    macd = ta.macd(data['Close'])
    data = pd.concat([data, macd], axis=1).reindex(data.index)
    data['macd_Indicator'] = 'NaN'

    for i in range(len(data.index)):
        if data['MACD_12_26_9'][i] > data['MACDs_12_26_9'][i]:
            data['macd_Indicator'][i] = "Buy"
        elif data['MACDs_12_26_9'][i] > data['MACD_12_26_9'][i]:
            data['macd_Indicator'][i] = "Short"
        else:
            data['macd_Indicator'][i] = np.NAN

    return data


def Final_Signal(data):
    data["Final_Signal"] = 'NaN'
    for i in range(len(data.index)):
        if data["ST_trend"][i] == "Buy" and data["SMA_Indicator"][i] == "Buy" and data["macd_Indicator"][i] == "Buy":
            data["Final_Signal"][i] = 'Buy'
        elif data["ST_trend"][i] == "Short" and data["SMA_Indicator"][i] == "Short" and data["macd_Indicator"][
            i] == "Short":
            data["Final_Signal"][i] = "Short"
        else:
            data["Final_Signal"][i] = 'No Clear trend'
    return data


def send_alert(data, i):
    sendrf_mail = ""
    password = ""
    receiver_mail = ""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(s_mail, password)
    print('login successful')
    last_row_index = len(data.index) - 1
    previous_row_index = last_row_index - 1

    if not data['Final_Signal'][previous_row_index] and data['Final_Signal'][last_row_index]:
        price = str(data['Close'].tail(1))
        price = price[34:]
        message = '{}  BUY at price {}'.format(i,price)
        server.sendmail(s_mail, r_mail, message)
        print('Mail send')
    elif data['Final_Signal'][previous_row_index] and not data['Final_Signal'][last_row_index]:
        price = str(data['Close'].tail(1))
        price = price[34:]
        message = '{}  SELL at price {}'.format(i, price)
        server.sendmail(s_mail, r_mail, message)
        print('Mail send')

def run_intraday():
    print(f"Fetched data at {datetime.now().isoformat()}", end='')
    f = open("watchlist.txt", "r")
    watchlist1 = f.readlines()
    watchlist2 = []
    for ele in watchlist1:
        watchlist2.append(ele.strip())
    f.close()
    print(' for yours watchlist :', watchlist2)
    for i in watchlist2:
        data = Stock_data(stock=i, period='5d', interval="5m")
        st = supertrend(data)
        adx1 = adx(st)
        sma1 = sma(adx1)
        md = macd(sma1)
        fs = Final_Signal(md)
        send_alert(fs, i)
        print('................................................................')
        print(i, fs[['Close', 'Final_Signal', 'adx_indicator']].tail(5))
    print('I am working.......')


def run_longterm():
    print(f"Fetched data at {datetime.now().isoformat()}", end='')
    f = open("watchlist.txt", "r")
    watchlist1 = f.readlines()
    watchlist2 = []
    for ele in watchlist1:
        watchlist2.append(ele.strip())
    f.close()
    print(' for yours watchlist :', watchlist2)
    for i in watchlist2:
        data = Stock_data(stock=i, period='30d',interval="1h")
        st = supertrend(data)
        adx1 = adx(st)
        sma1 = sma(adx1)
        md = macd(sma1)
        fs = Final_Signal(md)
        send_alert(fs, i)
        print('................................................................')
        print(i, fs[['Close', 'Final_Signal', 'adx_indicator']].tail(5))
    print('I am working.......')


watchlist = []
while True:
    print('Hello I am trading Bot developed by Mr Dileep Chakravarthi')
    f = open("watchlist.txt", "r")
    watchlist1 = f.readlines()
    watchlist2 = []
    for ele in watchlist1:
        watchlist2.append(ele.strip())
    f.close()
    print('Yours watchlist :', watchlist2)
    print('Select options below')
    print('1. Edit watchlist')
    print('2. Intraday')
    print('3. Long term')
    val = int(input())
    if val == 1:
        while True:
            print('Select options below')
            print('1. Add stock to watchlist')
            print('2. Remove stock to watchlist')
            print('3. To clear  watchlist')
            print('4. Enter any key to go back')

            val = int(input())
            if val == 1:
                stock = str(input('Enter Stock to watchlist'))
                stock = stock.upper()
                watchlist2.append(stock)
                f = open("watchlist.txt", "w")
                for ele in watchlist2:
                    f.write(ele + '\n')
                f.close()
            elif val == 2:
                stock = str(input('Enter Stock to remove from watchlist'))
                stock = stock.upper()
                watchlist2.remove(stock)
                f = open("watchlist.txt", "w")
                for ele in watchlist2:
                    f.write(ele + '\n')
                f.close()
            elif val == 3:
                f = open("watchlist.txt", "r+")
                f.truncate(0)
                f.close()
                print('Yours watchlist :', watchlist)
            else:
                break



    elif val == 2:
        print('loading data for intraday..............')
        schedule.every(5).seconds.do(run_intraday)
        while True:
            schedule.run_pending()
            time.sleep(1)

    elif val == 3:
        print('loading data for longterm..............')
        schedule.every(5).seconds.do(run_longterm)
        while True:
            schedule.run_pending()
            time.sleep(1)
