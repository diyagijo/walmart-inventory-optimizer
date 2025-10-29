# modules/forecasting.py
import pandas as pd
from prophet import Prophet
import numpy as np

def run_prophet_forecast(df_store_dept):
    """
    Runs a Prophet forecast for a given store-department dataframe.
    """
    # 1. Prepare data for Prophet
    df_prophet = df_store_dept.rename(columns={'Date': 'ds', 'Weekly_Sales': 'y'})
    
    # Select regressors
    regressors = ['Temperature', 'Fuel_Price', 'IsHoliday', 'Size', 'Type']
    df_prophet['IsHoliday'] = df_prophet['IsHoliday'].astype(int)
    
    # Handle 'Type' regressor (needs to be numeric)
    # Convert store 'Type' (A, B, C) into one-hot encoding
    df_prophet = pd.get_dummies(df_prophet, columns=['Type'], drop_first=True)
    
    # Update regressor list with new dummy columns
    regressor_list = ['Temperature', 'Fuel_Price', 'IsHoliday', 'Size']
    if 'Type_B' in df_prophet.columns:
        regressor_list.append('Type_B')
    if 'Type_C' in df_prophet.columns:
        regressor_list.append('Type_C')
        
    # Impute missing values (simple forward fill)
    df_prophet[regressor_list] = df_prophet[regressor_list].fillna(method='ffill').fillna(method='bfill')
    
    # Handle negative sales (set to 0)
    df_prophet.loc[df_prophet['y'] < 0, 'y'] = 0

    # 2. Build and Train Model
    m = Prophet(seasonality_mode='multiplicative', 
                yearly_seasonality=True, 
                weekly_seasonality=False, # Data is already weekly
                daily_seasonality=False)
    
    for reg in regressor_list:
        m.add_regressor(reg)
    
    m.fit(df_prophet[['ds', 'y'] + regressor_list])

    # 3. Create Future Forecast
    future = m.make_future_dataframe(periods=52, freq='W') # 52 weeks
    
    # 4. Populate Future Regressors
    # We need to provide future values for all regressors.
    # Assumption: Use the most recent known value (forward fill)
    
    # Create a dataframe that includes future dates
    future_regressors = df_prophet[['ds'] + regressor_list].merge(future, on='ds', how='right')
    # Forward fill the regressor values into the future
    future_regressors[regressor_list] = future_regressors[regressor_list].fillna(method='ffill')
    
    # 5. Get Prediction
    forecast = m.predict(future_regressors)
    
    # Set negative forecasts to 0
    forecast['yhat'] = np.maximum(0, forecast['yhat'])
    forecast['yhat_lower'] = np.maximum(0, forecast['yhat_lower'])
    forecast['yhat_upper'] = np.maximum(0, forecast['yhat_upper'])
    
    return m, forecast, df_prophet