# Weather Data Analysis and Temperature Prediction using Linear Regression

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Step 1: Load the dataset with correct date column
df = pd.read_csv('weatherHistory.csv', parse_dates=['Formatted Date'])

# Step 2: Set the datetime column as index
df.set_index('Formatted Date', inplace=True)

# Step 3: Use only Temperature (C) column and drop missing values
df = df[['Temperature (C)']]
df.dropna(inplace=True)

# Step 4: Visualize historical average temperature
plt.figure(figsize=(15, 5))
plt.plot(df.index, df['Temperature (C)'], label='Historical Temperature')
plt.title('Temperature Over Time')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.legend()
plt.show()

# Step 5: Prepare data for regression
df['DateOrdinal'] = df.index.map(lambda x: x.toordinal())
X = df['DateOrdinal'].values.reshape(-1, 1)
y = df['Temperature (C)'].values

# Step 6: Train Linear Regression Model
model = LinearRegression()
model.fit(X, y)

# Step 7: Predict future temperatures for 1 year
future_dates = pd.date_range(start=df.index[-1], periods=365)
future_ordinal = future_dates.map(lambda x: x.toordinal()).values.reshape(-1, 1)
future_preds = model.predict(future_ordinal)

# Step 8: Plot historical and future predictions
plt.figure(figsize=(15, 5))
plt.plot(df.index, y, label='Historical')
plt.plot(future_dates, future_preds, label='Predicted', linestyle='--', color='orange')
plt.title('Temperature Trend Prediction')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.show()

# Step 9: Evaluate the model
predicted_y = model.predict(X)
mae = mean_absolute_error(y, predicted_y)
rmse = np.sqrt(mean_squared_error(y, predicted_y))

print("Model Evaluation:")
print(f"MAE (Mean Absolute Error): {mae:.2f}")
print(f"RMSE (Root Mean Squared Error): {rmse:.2f}")
