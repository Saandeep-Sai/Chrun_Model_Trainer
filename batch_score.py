"""
Batch Scoring Script
Processes all customers and generates predictions via API
"""

import pandas as pd
import requests
import json
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    filename='batch_scoring.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# API Configuration
API_URL = 'http://127.0.0.1:5000/predict'
INPUT_FILE = 'all_customers.csv'
OUTPUT_FILE = 'scored_customers.csv'

def load_customers(filepath):
    """Load customer data from CSV"""
    print(f"Loading customers from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Drop index column if exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    
    print(f"Loaded {len(df)} customers")
    return df

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get('http://127.0.0.1:5000/health', timeout=5)
        if response.status_code == 200:
            print("✓ API is running and healthy")
            return True
        else:
            print("✗ API returned non-200 status")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ API is not reachable: {str(e)}")
        print("\nPlease start the API first:")
        print("  python app/main.py")
        return False

def predict_single_customer(customer_data, customer_id):
    """Send single customer to API for prediction"""
    try:
        # Prepare payload
        payload = {'customer': customer_data.to_dict()}
        
        # Make API request
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'prediction': result['prediction'],
                'churn_probability': result['churn_probability']
            }
        else:
            logging.error(f"API error for customer {customer_id}: {response.status_code}")
            return {
                'success': False,
                'prediction': 'Error',
                'churn_probability': None
            }
            
    except requests.exceptions.Timeout:
        logging.error(f"Timeout for customer {customer_id}")
        return {
            'success': False,
            'prediction': 'Timeout',
            'churn_probability': None
        }
    except Exception as e:
        logging.error(f"Error for customer {customer_id}: {str(e)}")
        return {
            'success': False,
            'prediction': 'Error',
            'churn_probability': None
        }

def batch_score(df):
    """Score all customers in batch"""
    print(f"\nStarting batch scoring for {len(df)} customers...")
    print("="*60)
    
    results = []
    successful = 0
    failed = 0
    
    start_time = time.time()
    
    for idx, row in df.iterrows():
        # Get customer ID if available
        customer_id = row.get('customerID', f'Customer_{idx}')
        
        # Remove customerID from features if present
        features = row.drop('customerID') if 'customerID' in row.index else row
        
        # Get prediction
        result = predict_single_customer(features, customer_id)
        
        if result['success']:
            successful += 1
        else:
            failed += 1
        
        # Store result
        results.append({
            'customerID': customer_id,
            'prediction': result['prediction'],
            'churn_probability': result['churn_probability']
        })
        
        # Progress update every 10 customers
        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{len(df)} customers...")
    
    elapsed_time = time.time() - start_time
    
    print("="*60)
    print(f"\nBatch scoring complete!")
    print(f"Total customers: {len(df)}")
    print(f"Successful predictions: {successful}")
    print(f"Failed predictions: {failed}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Average time per customer: {elapsed_time/len(df):.3f} seconds")
    
    # Log summary
    logging.info(f"Batch scoring completed - Total: {len(df)}, Success: {successful}, Failed: {failed}")
    
    return pd.DataFrame(results)

def save_results(df_original, df_predictions, output_file):
    """Combine original data with predictions and save"""
    print(f"\nSaving results to {output_file}...")
    
    # Merge original data with predictions
    df_scored = df_original.copy()
    df_scored['predicted_churn'] = df_predictions['prediction'].values
    df_scored['churn_probability'] = df_predictions['churn_probability'].values
    
    # Save to CSV
    df_scored.to_csv(output_file, index=False)
    
    print(f"✓ Results saved successfully!")
    print(f"  File: {output_file}")
    print(f"  Rows: {len(df_scored)}")
    
    # Show summary statistics
    print("\nPrediction Summary:")
    print(df_scored['predicted_churn'].value_counts())
    
    if df_scored['churn_probability'].notna().any():
        print(f"\nAverage Churn Probability: {df_scored['churn_probability'].mean():.4f}")
        print(f"High Risk Customers (>70% churn prob): {(df_scored['churn_probability'] > 0.7).sum()}")

def main():
    """Main batch scoring workflow"""
    print("="*60)
    print("BATCH CUSTOMER SCORING")
    print("="*60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Check API health
    if not check_api_health():
        print("\nExiting: API is not available")
        return
    
    try:
        # Load customers
        df_customers = load_customers(INPUT_FILE)
        
        # Perform batch scoring
        df_predictions = batch_score(df_customers)
        
        # Save results
        save_results(df_customers, df_predictions, OUTPUT_FILE)
        
        print("\n" + "="*60)
        print("BATCH SCORING COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except FileNotFoundError:
        print(f"\nError: Input file '{INPUT_FILE}' not found")
        logging.error(f"Input file not found: {INPUT_FILE}")
    except Exception as e:
        print(f"\nError during batch scoring: {str(e)}")
        logging.error(f"Batch scoring failed: {str(e)}")

if __name__ == "__main__":
    main()
