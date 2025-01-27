import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from fredapi import Fred
import os

save_path = "/Users/boragoksal/PycharmProjects/FinDataAnalysis/data/raw/"
file_path = os.path.join(save_path, "AAPL.csv")

#Read in the Apple stocks data
df_AAPL = pd.read_csv(file_path)

#convert Date to datetime
df_AAPL['Date'] = pd.to_datetime(df_AAPL['Date'])
df_AAPL.set_index('Date', inplace=True)

#Calculating stock returns
df_AAPL['Daily returns'] = df_AAPL['Close'].pct_change()

#Load inflation data
api_key = os.getenv('FRED_API_KEY')
fred = Fred(api_key=api_key)
data_inflation = fred.get_series('CPIAUCSL') # Consumer Price Index for All Urban Consumers

#Regression model
