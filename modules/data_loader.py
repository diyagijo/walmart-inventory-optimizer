# modules/data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(data_path="data/"):
    """
    Loads and merges all required dataframes from the specified path.
    This function is cached by Streamlit for performance.
    """
    try:
        train = pd.read_csv(f"{data_path}train.csv")
        features = pd.read_csv(f"{data_path}features.csv")
        stores = pd.read_csv(f"{data_path}stores.csv")
    except FileNotFoundError:
        st.error(f"Error: Data files not found in '{data_path}' folder.")
        st.error("Please download train.csv, features.csv, and stores.csv from Kaggle.")
        return None, None, None

    # Merge dataframes
    features = pd.merge(features, stores, on='Store', how='left')
    df = pd.merge(train, features, on=['Store', 'Date', 'IsHoliday'], how='left')
    
    # Convert 'Date' to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Get lists of available stores and departments
    store_list = sorted(df['Store'].unique())
    dept_list = sorted(df['Dept'].unique())

    return df, store_list, dept_list

def filter_data(df, store_id, dept_id):
    """
    Filters the main dataframe for a specific store and department.
    """
    df_filtered = df[(df['Store'] == store_id) & (df['Dept'] == dept_id)].copy()
    return df_filtered