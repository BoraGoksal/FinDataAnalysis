import pandas as pd
from datetime import datetime
from fredapi import Fred
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

save_path = "/Users/boragoksal/PycharmProjects/FinDataAnalysis/data/raw/"
file_path = os.path.join(save_path, "AAPL.csv")

# Read in the Apple stock data
df_AAPL = pd.read_csv(file_path)

# Convert Date to datetime
df_AAPL['Date'] = pd.to_datetime(df_AAPL['Date'])
df_AAPL.set_index('Date', inplace=True)

# Remove timezone information from the AAPL stock data index
df_AAPL.index = df_AAPL.index.tz_localize(None)

# Calculating stock returns
df_AAPL['Daily returns'] = df_AAPL['Close'].pct_change()

# Load inflation and GDP data
api_key = os.getenv('FRED_API_KEY')
fred = Fred(api_key=api_key)
data_inflation = fred.get_series('CPIAUCSL')  # Consumer Price Index for All Urban Consumers
data_gdp = fred.get_series('GDP')

# Convert FRED data to DataFrame and set index to datetime
df_inflation = data_inflation.to_frame(name='Inflation')
df_inflation.index = pd.to_datetime(df_inflation.index)

df_gdp = data_gdp.to_frame(name='GDP')
df_gdp.index = pd.to_datetime(df_gdp.index)

# Trim inflation and GDP data to match the AAPL date range
start_date = df_AAPL.index.min()  # Start date of AAPL data
end_date = df_AAPL.index.max()   # End date of AAPL data

df_inflation = df_inflation[(df_inflation.index >= start_date) & (df_inflation.index <= end_date)]
df_gdp = df_gdp[(df_gdp.index >= start_date) & (df_gdp.index <= end_date)]

# Fill missing data with forward and backward fill
for df in [df_inflation, df_gdp]:
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    df.index = df.index.tz_localize(None)

# Merging the data into a single DataFrame
df = df_AAPL[['Close', 'Daily returns']].copy()
df_inflation.columns = ['Inflation']
df_gdp.columns = ['GDP']

# Join the data
df = df.join([df_inflation, df_gdp], how='inner')
df.dropna(inplace=True)

print(df.head())

#Regression model
X = df[['Inflation', 'GDP']]
y = df['Daily returns']

X_train,X_test,y_train,y_test = train_test_split(X,y, test_size= 0.2, random_state=39)

model = LinearRegression()
model.fit(X_train,y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display results
print("Model Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print("Mean Squared Error:", mse)
print("R-squared:", r2)

