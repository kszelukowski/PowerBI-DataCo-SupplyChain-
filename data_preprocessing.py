import pandas as pd
import os

def clean_supply_chain_data(file_name):
    # Determine the directory where the script is located
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, file_name)
    
    print(f"Loading file: {full_path}")
    
    # Load data with ISO-8859-1 encoding for compatibility
    df = pd.read_csv(full_path, encoding='ISO-8859-1')

    # STEP 1: Column Name Normalization
    # Converts names like "Days for shipment (scheduled)" to "days_for_shipment_scheduled"
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace('(', '')
                  .str.replace(')', '')
                  .str.replace('-', '_'))
    
    print("Column names standardized successfully.")

    # STEP 2: Feature Engineering
    # Updated to match your specific headers: 'days_for_shipping_real' and 'days_for_shipment_scheduled'
    real_col = 'days_for_shipping_real'
    sched_col = 'days_for_shipment_scheduled'
    
    if real_col in df.columns and sched_col in df.columns:
        # Create Boolean flag for Power BI filters
        df['is_late'] = df['days_for_shipping_real'] > df[sched_col]
        
        # Calculate numerical delay for KPI averages
        df['delivery_delay_days'] = df['days_for_shipping_real'] - df[sched_col]
        print("Logistics KPIs (is_late, delivery_delay_days) created.")
    else:
        print(f"WARNING: Could not find '{real_col}' or '{sched_col}'.")
        print("Available columns:", df.columns.tolist())

    # STEP 3: Security & Anonymization
    # Dropping sensitive PII (Personally Identifiable Information)
    cols_to_drop = ['customer_fname', 'customer_lname', 'customer_email', 'product_description']
    df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True)
    
    return df, base_path

if __name__ == "__main__":
    try:
        processed_data, folder = clean_supply_chain_data('DataCoSupplyChainDataset.csv')
        
        output_file = os.path.join(folder, 'Cleaned_Logistics_Data.csv')
        processed_data.to_csv(output_file, index=False)
        
        print(f"SUCCESS! Cleaned file saved: {output_file}")
        
    except Exception as e:
        print(f"ERROR: {e}")