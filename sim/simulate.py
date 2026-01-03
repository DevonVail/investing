

from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import math
import pickle
import yfinance as yf
from typing import List

STARTDATE = datetime(2025, 1, 1)
ENDDATE = datetime.today()



date_range = [STARTDATE + timedelta(days=x) for x in range((ENDDATE - STARTDATE).days + 1)]

electricity_infrastructure_stocks = {"NYSE":{"EIX":[], "ED":[], "EME":[], "SO":[], "DUK":[], "MTZ":[], "ETR":[], "NEE":[], "PCG":[]},
                                     "NASDAQ":{"EXC":[], "FSLR":[], "AEP":[], "CEG":[]}}

def retrieve_stock_data(stocks_of_interest: dict, start_date: datetime, end_date: datetime, save_data: bool=False):
    for exchange in stocks_of_interest.keys():
        for ticker in stocks_of_interest[exchange].keys():
            
            stocks_of_interest[exchange][ticker] = yf.download(ticker, start=start_date, end=end_date)
            stocks_of_interest[exchange][ticker]['Returns'] = stocks_of_interest[exchange][ticker]['Close'].pct_change()
    return stocks_of_interest

# def filter_stocks_by_avg_daily_return(stocks_of_interest: dict, return_prcnt_thresh: float=0.1):
#     for exchange in stocks_of_interest.keys():
#         for ticker in stocks_of_interest[exchange].keys():
#             exchange_ticker_str = f"{exchange}:{ticker}"
#             stock_cumprod = (1 + stocks_of_interest[exchange][ticker]['Returns']).cumprod()
#             print(f"{exchange_ticker_str} average return: {stock_cumprod}%")
#             if (1+return_prcnt_thresh) <= stock_cumprod:
#                 print(f"Threshold Exceeded\n\n")


def filter_stocks_by_list(stocks_to_be_filtered: dict, list_of_tickers: List[str]):
    filtered_stocks = {}
    empty_exchanges = []
    for exchange in stocks_to_be_filtered.keys():
        filtered_stocks[exchange] = {}
        for ticker in stocks_to_be_filtered[exchange].keys():
            if ticker in list_of_tickers: filtered_stocks[exchange][ticker] = stocks_to_be_filtered[exchange][ticker]
    for exchange in filtered_stocks.keys():
        if len(filtered_stocks[exchange]) == 0: empty_exchanges.append(exchange)
    for empty_exchange in empty_exchanges: filtered_stocks.pop(empty_exchange)
    
    return filtered_stocks



def plot_stock_data(stocks_of_interest: dict):
    plt.figure(figsize=(10, 6))
    for exchange in stocks_of_interest.keys():
        for ticker in stocks_of_interest[exchange].keys():
            exchange_ticker_str = f"{exchange}:{ticker}"
            plt.plot(stocks_of_interest[exchange][ticker]['Close'], label=exchange_ticker_str)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))

    # Enable interactive hover annotations
    cursor = mplcursors.cursor(hover=True)
    #cursor.connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))
    @cursor.connect("add")
    def on_add(sel):
        line = sel.artist
        label = line.get_label()
        x_val, y_val = sel.target
        dt_object = mdates.num2date(x_val)
        formatted_date = dt_object.strftime('%y-%m-%d')
        sel.annotation.set_text(f"{label}\nDate: {formatted_date}\nPrice: {y_val:.2f}")

    plt.title(f"Electricity Infrastructure Stocks YTD")
    plt.xlabel("Date")
    plt.ylabel("Close Value($)")
    plt.legend()
    plt.grid()
    plt.show()


def get_prcnt_return_btwn_two_dates(ticker: str, start_date: datetime, end_date: datetime):
    


filtered_stock_list = ['EME', 'CEG', 'FSLR', 'MTZ'] # Created this by looking at the plot of all the stocks listed above YTD and picking the four that weren't essentially flat
electricity_infrastructure_stocks = retrieve_stock_data(electricity_infrastructure_stocks, STARTDATE, ENDDATE)
filtered_electricity_infrastructure_stocks = filter_stocks_by_list(electricity_infrastructure_stocks, filtered_stock_list)
plot_stock_data(filtered_electricity_infrastructure_stocks)


#print(len(data.index))

#data['Returns'] = data['Close'].pct_change()  # Calculate daily returns

"""
# Step 2: Simulate Portfolio Growth
initial_investment = 10000  # Starting with $10,000
data['Portfolio Value'] = initial_investment * (1 + data['Returns']).cumprod()

# Step 3: Visualize the Simulation
plt.figure(figsize=(10, 6))
plt.plot(data['Portfolio Value'], label="Portfolio Value")

"""