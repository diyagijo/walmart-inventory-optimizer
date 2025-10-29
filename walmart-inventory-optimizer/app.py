# app.py
import streamlit as st
import plotly.graph_objects as go
from prophet.plot import plot_components_plotly

# --- THIS IS THE FIX ---
# This tells Python to look in the current folder for the 'modules' directory
import sys
import os
sys.path.append(os.path.dirname(__file__))
# --- END OF FIX ---

# Import your modules
from modules import data_loader, forecasting, optimization
import config

# --- Page Configuration ---
st.set_page_config(
    page_title="Retail Inventory Optimizer",
    page_icon="🛒",
    layout="wide"
)

# --- Custom CSS for "Sleek" Look ---
CSS_STYLE = """
<style>
/* --- Main App Styling --- */
div[data-testid="stAppViewContainer"] {
    background-color: #1a1a1a; /* Darker background for the app */
}

/* --- Sidebar Styling --- */
div[data-testid="stSidebar"] {
    background-color: #1E1E1E; /* Slightly different sidebar color */
    border-right: 1px solid #333;
}
div[data-testid="stSidebar"] h1, 
div[data-testid="stSidebar"] h2, 
div[data-testid="stSidebar"] h3 {
    color: #FAFAFA;
}
div[data-testid="stSidebar"] .stSelectbox,
div[data-testid="stSidebar"] .stSlider,
div[data-testid="stSidebar"] .stNumberInput {
    padding-bottom: 10px;
}

/* --- "Run Analysis" Button Styling --- */
button[data-testid="stButton"] > div {
    font-weight: bold;
    border: 2px solid #FF4B4B; /* Red border */
    border-radius: 50px; /* Pill shape */
    padding: 10px 20px;
    background-color: transparent;
    transition: all 0.3s ease;
}
button[data-testid="stButton"]:hover > div {
    background-color: #FF4B4B; /* Red fill on hover */
    color: white;
}
button[data-act-class="st-emotion-cache-n5mc6e"] {
    background-color: #FF4B4B;
}

/* --- Metric "Card" Styling --- */
div[data-testid="stMetric"] {
    background-color: #262730;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
div[data-testid="stMetric"] > div {
    padding-left: 10px; /* Adjust internal padding */
}

/* --- Tab Styling --- */
div[data-testid="stTabs"] {
    border-bottom: 2px solid #333;
}
button[data-baseweb="tab"] {
    font-size: 1.1rem;
    padding: 15px;
}

/* --- Chart "Card" Styling --- */
div[data-testid="stPlotlyChart"] {
    background-color: #262730;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

</style>
"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)


# --- Data Loading ---
df, store_list, dept_list = data_loader.load_data()
if df is None:
    st.stop()

# --- Sidebar (Inputs) ---
st.sidebar.title("Configuration")

st.sidebar.header("1. Select Item")
selected_store = st.sidebar.selectbox("Store", store_list, index=store_list.index(config.DEFAULT_STORE))
selected_dept = st.sidebar.selectbox("Department", dept_list, index=dept_list.index(config.DEFAULT_DEPT))

st.sidebar.header("2. Set Business Parameters")
L = st.sidebar.slider("Lead Time (Weeks)", 1, 12, config.DEFAULT_LEAD_TIME_WEEKS)
SL_pct = st.sidebar.slider("Service Level (%)", 80.0, 99.9, config.DEFAULT_SERVICE_LEVEL_PCT, 0.1)
C = st.sidebar.number_input("Item Cost ($)", 0.01, 10000.0, config.DEFAULT_ITEM_COST, 0.01)
H_pct = st.sidebar.slider("Annual Holding Cost (% of Item Cost)", 1.0, 50.0, config.DEFAULT_HOLDING_COST_PCT, 0.5)
S = st.sidebar.number_input("Ordering Cost ($)", 0.0, 1000.0, config.DEFAULT_ORDERING_COST, 1.0)

# --- Main Application ---
st.title(f"🛒 Retail Demand Forecast & Inventory Optimizer")
st.header(f"Store {selected_store} | Department {selected_dept}")

# Run analysis when button is pressed
if st.sidebar.button("Run Analysis", type="primary"):
    
    with st.spinner("Running analysis... This may take a moment."):
        
        # 1. Filter data
        df_filtered = data_loader.filter_data(df, selected_store, selected_dept)
        
        if df_filtered.empty:
            st.error("No data found for this Store/Department combination.")
        else:
            # 2. Run Forecast
            model, forecast, hist_df = forecasting.run_prophet_forecast(df_filtered)
            
            # 3. Run Optimization
            policy = optimization.calculate_inventory_policy(forecast, hist_df, L, SL_pct, C, H_pct, S)
            
            # --- Display Results ---
            
            # Use tabs for a cleaner layout
            tab1, tab2 = st.tabs(["📈 Policy & Forecast", "⚙️ Model Components"])
            
            with tab1:
                st.subheader("Recommended Inventory Policy")
                
                # Key Metrics in columns
                col1, col2, col3 = st.columns(3)
                col1.metric("Reorder Point (ROP)", f"{policy['reorder_point']} Units",
                             help="When inventory drops to this level, place a new order.")
                col2.metric("Order Quantity (EOQ)", f"{policy['order_quantity']} Units",
                             help="The optimal amount to order to minimize costs.")
                col3.metric("Safety Stock", f"{policy['safety_stock']} Units",
                             help="Buffer stock to prevent stockouts during lead time.")

                # Use st.caption for the policy explanation text
                st.caption(f"This policy is designed to achieve a **{SL_pct}% service level**, protecting against stockouts during the **{L}-week** lead time. "
                         f"It assumes an item cost of **${C}**, a holding cost of **{H_pct}%** (or **${policy['annual_holding_cost']}** per unit/year), "
                         f"and an ordering cost of **${S}**.")

                # 1. Forecast Plot
                st.subheader("Weekly Sales Forecast (Next 52 Weeks)")
                fig_forecast = go.Figure()
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'], y=forecast['yhat'], name='Forecast (yhat)',
                    line=dict(color='#007AFF') # Brighter blue
                ))
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'], y=forecast['yhat_upper'], name='Upper Uncertainty',
                    line=dict(color='gray', dash='dash'), fill=None
                ))
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'], y=forecast['yhat_lower'], name='Lower Uncertainty',
                    line=dict(color='gray', dash='dash'), fill='tonexty',
                    fillcolor='rgba(150, 150, 150, 0.2)' # Lighter fill
                ))
                fig_forecast.add_trace(go.Scatter(
                    x=hist_df['ds'], y=hist_df['y'], name='Historical Sales',
                    mode='markers', marker=dict(color='white', size=5, opacity=0.5) # White markers
                ))
                fig_forecast.update_layout(
                    title=f"Sales Forecast for Store {selected_store} / Dept {selected_dept}",
                    xaxis_title="Date", yaxis_title="Weekly Sales ($)",
                    showlegend=True,
                    template="plotly_dark", # Use plotly's dark template
                    paper_bgcolor='rgba(0,0,0,0)', # Transparent background
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_forecast, use_container_width=True)

            with tab2:
                # 2. Model Components
                st.subheader("Forecast Components")
                st.write("These charts show the model's understanding of yearly trends and the impact of factors like temperature.")
                
                fig_components = plot_components_plotly(model, forecast)
                fig_components.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_components, use_container_width=True)

else:
    st.info("Select your item and parameters in the sidebar, then click 'Run Analysis'.")
