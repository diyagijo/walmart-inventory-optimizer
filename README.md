# walmart-inventory-optimizer
# Retail Demand Forecasting & Inventory Optimization

This project builds an end-to-end tool to forecast retail sales and calculate an optimal inventory policy (Reorder Point & Economic Order Quantity).

The tool uses the Kaggle "Walmart Store Sales Forecasting" dataset.

## Project Structure

-   `/data/`: Contains the raw Kaggle CSV files.
-   `/modules/`: Contains the core Python logic:
    -   `data_loader.py`: Loads and merges data.
    -   `forecasting.py`: Runs the Prophet forecast.
    -   `optimization.py`: Calculates the inventory policy.
-   `app.py`: The main Streamlit application file.
-   `config.py`: Default configuration and business inputs.
-   `requirements.txt`: Required Python packages.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd walmart_inventory_project
    ```

2.  **Download the data:**
    Download `train.csv`, `features.csv`, and `stores.csv` from the [Kaggle Walmart competition](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting) and place them in the `/data/` folder.

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```


    
