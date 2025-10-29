
#  Retail Demand Forecast & Inventory Optimizer

This is an end-to-end analytics tool that moves from prediction (forecasting sales) to prescription (optimizing inventory). It's built in Python using Prophet and Streamlit.

## 🚀 Live Application

**[[Walmart-inventory-optmizer-deployed](https://walmart-inventory-optimizer-fnfe3twwjatvyuasbw4r7y.streamlit.app/)]**

## 💡 The Business Problem

Retail clients constantly struggle to balance the high cost of overstocking with the lost sales from stockouts. This tool provides a data-driven solution by answering two key questions:
1.  **When** should we reorder?
2.  **How much** should we reorder?

## 🛠️ How It Works

1.  **Forecast:** A time-series model (Prophet) forecasts weekly sales, capturing seasonality and the impact of external drivers like temperature and holidays.
2.  **Optimize:** The forecast's uncertainty is used to calculate a full inventory policy (Reorder Point, Safety Stock, EOQ) that is optimized to meet a specific **Service Level**.
3.  **Deploy:** The entire model is deployed as an interactive Streamlit dashboard where a "store manager" can run what-if scenarios to see the exact cost/risk trade-offs of their decisions.
### 📸 Dashboard Screenshots
Here is the tool in action, showing the clear, actionable recommendations:
![Dashboard Screenshot 1](dashboard_main.png)
![Dashboard Screenshot 2](d2.png)

## 🔧 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/diyagijo/walmart-inventory-optimizer.git](https://github.com/diyagijo/walmart-inventory-optimizer.git)
    cd walmart-inventory-optimizer
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

---


    
