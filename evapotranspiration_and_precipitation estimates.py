import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# ---- SETTINGS ----
input_file = 'Input Data for Water Budget Predictions.xlsm'  # Change to your filename
sheet_name = 'ET_and_Precip'  # Set to None for first sheet, or e.g. 'Sheet1' if you know it
months_to_predict = 400  # Change as needed
output_excel = 'Monthly_ET_and_Precip_Predictions.xlsx'

# ---- READ DATA ----
df = pd.read_excel(input_file, sheet_name=sheet_name)
df = df.rename(columns={
    'Month-Year': 'ds',
    'Monthly Evapotranspiration Estimates (ET) (mm)': 'ET',
    'Monthly Precipitation Estimates (mm)': 'Precip'
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
et_forecast = prophet_forecast(df, 'ET', months_to_predict)
precip_forecast = prophet_forecast(df, 'Precip', months_to_predict)

# ---- MERGE RESULTS ----
# Merge on date, keep all forecast dates (will align future dates automatically)
all_forecasts = pd.merge(et_forecast, precip_forecast, on='ds', how='outer')

# ---- EXPORT TO EXCEL ----
all_forecasts.to_excel(output_excel, index=False)
print(f"Forecasts saved to {output_excel}")

# ---- OPTIONAL: PLOT ----
plt.figure(figsize=(10, 4))
plt.plot(et_forecast['ds'], et_forecast['ET_forecast'], label='ET Forecast')
plt.fill_between(et_forecast['ds'], et_forecast['ET_lower'], et_forecast['ET_upper'], alpha=0.2)
plt.title('Long-Term Evapotranspiration Forecast')
plt.xlabel('Year')
plt.ylabel('ET (mm)')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(precip_forecast['ds'], precip_forecast['Precip_forecast'], color='g', label='Precip Forecast')
plt.fill_between(precip_forecast['ds'], precip_forecast['Precip_lower'], precip_forecast['Precip_upper'], color='g', alpha=0.2)
plt.title('Long-Term Precipitation Forecast')
plt.xlabel('Year')
plt.ylabel('Precipitation (mm)')
plt.legend()
plt.tight_layout()
plt.show()
