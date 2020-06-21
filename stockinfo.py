import datetime as dt
from datetime import date
import pandas_datareader.data as web
from fuzzywuzzy import process
import requests
import matplotlib.pyplot as plt
import yfinance as yf

today = date.today()
tdy = (today.strftime('%Y,%m,%d')).split(',')
start = dt.datetime(2000,1,1)
end = dt.datetime(int(tdy[0]),int(tdy[1]),int(tdy[2]))

def amount_of_stocks()->[list]:
    companystocks = []
    n = int(input("How many stocks do you want to check: "))
    for i in range(0, n):
        print("Enter Company", i+1, ":")
        item = input()
        companystocks.append(item)

    tickers = []
    for i in range(len(companystocks)):

        r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
        stockList = r.json()
        info = process.extractOne(companystocks[i], stockList)[0]
        ticker = info['symbol']
        tickers.append(ticker)
        companyname = info['name']

        df = web.DataReader(ticker, 'yahoo' , start , end)

        latest_data = ((df['Adj Close'].tail(1).to_string(index=False)).split('\n'))[1]
        latest_data = round(float(latest_data),2)

        print(companyname + " (" + ticker + ")" + ": " + str(latest_data)+"\n")

    return tickers


def graph (tickers:[list]):
    data = yf.download(tickers, '2019-1-1')['Adj Close']
    ((data.pct_change() + 1).cumprod()).plot(figsize=(10, 7))

    plt.legend()
    plt.title("Side-By-Side Returns", fontsize=16)
    plt.ylabel('Cumulative Returns', fontsize=14)
    plt.xlabel('Year', fontsize=14)

    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    plt.show()
    print(data.tail())

if __name__ == "__main__":
    graph(amount_of_stocks())