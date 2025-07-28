import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# ---- SETTINGS ----
input_file = 'Input Data for Water Budget Predictions.xlsm'  # Change to your filename
sheet_name = 'Snowmelt'  # Set to None for first sheet, or e.g. 'Sheet1' if you know it
months_to_predict = 400  # Change as needed
output_excel = 'Monthly_Snowmelt_Predictions.xlsx'

# ---- READ DATA ----
df = pd.read_excel(input_file, sheet_name=sheet_name)
df = df.rename(columns={
    'Month-Year': 'ds',
    'Sum of Volumetric Snowmelt Per Month (m^3/month)': 'Snowmelt',
})

# Ensure datetime format for Prophet
# (Try both %Y-%m and %b-%Y in case user used either format)
try:
    df['ds'] = pd.to_datetime(df['ds'], format='%Y-%m')
except:
    try:
        df['ds'] = pd.to_datetime(df['ds'], format='%b-%Y')
    except:
        df['ds'] = pd.to_datetime(df['ds'])  # fallback: autodetect

# ---- FORECAST FUNCTION ----
def prophet_forecast(df, value_col, months_to_predict):
    data = df[['ds', value_col]].rename(columns={value_col: 'y'})
    model = Prophet(yearly_seasonality=True)
    model.fit(data)
    future = model.make_future_dataframe(periods=months_to_predict, freq='M')
    forecast = model.predict(future)
    output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    output = output.rename(columns={
        'yhat': f'{value_col}_forecast',
        'yhat_lower': f'{value_col}_lower',
        'yhat_upper': f'{value_col}_upper'
    })

    # Set any negative values to zero
    for col in [f'{value_col}_forecast', f'{value_col}_lower']:
        output[col] = output[col].clip(lower=0)
    return output
    return output

# ---- GENERATE FORECASTS ----
snowmelt_forecast = prophet_forecast(df, 'Snowmelt', months_to_predict)


# ---- EXPORT TO EXCEL ----
snowmelt_forecast.to_excel(output_excel, index=False)
print(f"Forecasts saved to {output_excel}")

# ---- OPTIONAL: PLOT ----
plt.figure(figsize=(10, 4))
plt.plot(snowmelt_forecast['ds'], snowmelt_forecast['Snowmelt_forecast'], label='Snowmelt Forecast')
plt.fill_between(snowmelt_forecast['ds'], snowmelt_forecast['Snowmelt_lower'], snowmelt_forecast['Snowmelt_upper'], alpha=0.2)
plt.title('Long-Term Snowmelt Forecast')
plt.xlabel('Date')
plt.ylabel('Snowmelt (m^3)')
plt.legend()
plt.tight_layout()
plt.show()
