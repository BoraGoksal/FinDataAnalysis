import yfinance as yf
from datetime import datetime
import os

def collect_stock_data(tickers, start_date, end_date, save_path = "/Users/boragoksal/PycharmProjects/FinDataAnalysis/data/raw"):
    os.makedirs(save_path, exist_ok= True)

    #Download data for all tickers
    data = yf.download(tickers, start = start_date, end = end_date)

    #save each ticker's data as a seperate CSV file in to data/raw/
    for ticker in tickers:
        data_ticker = data.xs(ticker, level=1, axis=1) #Data for each ticker
        file_path = os.path.join(save_path, f"{ticker}.csv")
        data_ticker.to_csv(file_path)

        print(f"Data for {ticker} saved to {file_path}")

if __name__ == "__main__":

    tickers = ['AAPL', 'GOOGL', 'MSFT', 'NFLX'] #tickers - add more if needed

    start = "2018-01-01"
    end = datetime.now()
    collect_stock_data(tickers, start, end) #collecting data for specified dates
