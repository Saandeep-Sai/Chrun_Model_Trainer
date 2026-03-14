"""
Customer Churn Prediction API
Flask application for real-time churn predictions
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='monitoring.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load model at startup
MODEL_PATH = 'model.pkl'
model = None

def load_model():
    """Load the trained model pipeline"""
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logging.info("Model loaded successfully")
            print("Model loaded successfully")
        else:
            logging.error(f"Model file not found at {MODEL_PATH}")
            print(f"ERROR: Model file not found at {MODEL_PATH}")
    except Exception as e:
        logging.error(f"Error loading model: {str(e)}")
        print(f"ERROR loading model: {str(e)}")

# Load model when app starts
load_model()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Customer Churn Prediction API',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint
    Expects JSON with customer features
    Returns churn prediction and probability
    """
    try:
        # Check if model is loaded
        if model is None:
            logging.error("Prediction failed: Model not loaded")
            return jsonify({
                'error': 'Model not loaded',
                'message': 'Please ensure model.pkl exists in the app directory'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            logging.warning("Prediction failed: No data provided")
            return jsonify({
                'error': 'No data provided',
                'message': 'Please send customer data in JSON format'
            }), 400
        
        # Extract customer data
        if 'customer' in data:
            customer_data = data['customer']
        else:
            customer_data = data
        
        # Convert to DataFrame
        df = pd.DataFrame([customer_data])
        
        # Handle TotalCharges conversion
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            if df['TotalCharges'].isna().any():
                df['TotalCharges'].fillna(df['MonthlyCharges'], inplace=True)
        
        # Make prediction
        prediction = model.predict(df)[0]
        prediction_proba = model.predict_proba(df)[0]
        
        # Prepare response
        result = {
            'prediction': 'Churn' if prediction == 1 else 'No Churn',
            'churn_probability': float(prediction_proba[1]),
            'no_churn_probability': float(prediction_proba[0]),
            'timestamp': datetime.now().isoformat()
        }
        
        # Log successful prediction
        logging.info(f"Prediction successful - Churn: {result['prediction']}, Probability: {result['churn_probability']:.4f}")
        
        return jsonify(result), 200
        
    except KeyError as e:
        logging.error(f"Prediction failed: Missing feature - {str(e)}")
        return jsonify({
            'error': 'Missing feature',
            'message': f'Required feature missing: {str(e)}'
        }), 400
        
    except Exception as e:
        logging.error(f"Prediction failed: {str(e)}")
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Please use /predict endpoint for predictions'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logging.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    print("="*60)
    print("CUSTOMER CHURN PREDICTION API")
    print("="*60)
    print("Starting Flask server...")
    print("API will be available at: http://127.0.0.1:5000")
    print("Prediction endpoint: http://127.0.0.1:5000/predict")
    print("="*60)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
