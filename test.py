from prophet import Prophet

# Create a simple dataframe
import pandas as pd
df = pd.DataFrame({
    'ds': pd.date_range(start='2025-01-01', periods=10, freq='D'),
    'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
})

# Create and fit the model
model = Prophet()
model.fit(df)

# Make a future dataframe
future = model.make_future_dataframe(periods=5)
forecast = model.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())