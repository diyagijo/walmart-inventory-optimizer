# modules/optimization.py
from scipy.stats import norm
import numpy as np

def calculate_inventory_policy(forecast, historical_df, L, SL_pct, C, H_pct, S):
    """
    Calculates the optimal inventory policy (ROP, EOQ, SS).
    """
    # 1. Get Inputs from Forecast & History
    # Use forecast 'yhat' for future demand, but historical 'y' for volatility
    avg_weekly_demand = forecast['yhat'].mean()
    std_weekly_demand = historical_df['y'].std()
    
    # 2. Convert Inputs
    SL = SL_pct / 100.0
    Z = norm.ppf(SL)  # Z-score for Service Level
    H = C * (H_pct / 100.0) # Annual Holding Cost ($)
    D = avg_weekly_demand * 52 # Annual Demand

    # 3. Calculate Inventory Policy
    
    # Standard deviation of demand *during lead time*
    std_dev_lead_time = std_weekly_demand * np.sqrt(L)
    
    # Safety Stock (SS)
    SS = Z * std_dev_lead_time
    
    # Reorder Point (ROP)
    # (Avg. demand during lead time) + (Safety buffer)
    ROP = (avg_weekly_demand * L) + SS
    
    # Economic Order Quantity (EOQ)
    if H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
    else:
        EOQ = np.inf # Avoid division by zero if holding cost is 0
        
    # Compile results into a dictionary
    policy = {
        'avg_weekly_demand': int(avg_weekly_demand),
        'std_weekly_demand': int(std_weekly_demand),
        'safety_stock': int(SS),
        'reorder_point': int(ROP),
        'order_quantity': int(EOQ),
        'z_score': round(Z, 2),
        'annual_holding_cost': round(H, 2)
    }
    
    return policy