import yfinance as yf
import os

def collect_stock_data(ticker, start_date, end_date, save_path = "data/raw/"):
    os.makedirs(save_path, exist_ok= True)
    data = yf.download(ticker, start = start_date, end = end_date)
    file_path = os.path.join(save_path, f"{ticker}.csv")
    data.to_csv(file_path)
    print(f"Data for {ticker} saved to {file_path}")

if __name__ == "__main__":
    collect_stock_data("AAPL", "2020-01-01", "2023-01-01")