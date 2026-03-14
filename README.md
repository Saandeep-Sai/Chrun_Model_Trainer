# Customer Churn Prediction - Production Deployment

## Project Overview

This project demonstrates a complete machine learning deployment pipeline for customer churn prediction. It includes model training, real-time API serving, batch scoring, and production monitoring capabilities.

## System Architecture

```
┌─────────────────┐
│  Training Data  │
│ (gold_churn_    │
│   data.csv)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  train_model.py │  ← Train & save model
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   model.pkl     │  ← Serialized pipeline
└────────┬────────┘
         │
         ├──────────────────┐
         ▼                  ▼
┌─────────────────┐  ┌──────────────────┐
│   Flask API     │  │  Batch Scoring   │
│  (app/main.py)  │  │ (batch_score.py) │
└────────┬────────┘  └────────┬─────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌──────────────────┐
│  Real-time      │  │  scored_         │
│  Predictions    │  │  customers.csv   │
└─────────────────┘  └──────────────────┘
```

## Features

✅ **Model Training**: Automated pipeline with preprocessing  
✅ **REST API**: Flask-based prediction service  
✅ **Batch Processing**: Score multiple customers efficiently  
✅ **Logging**: Comprehensive monitoring and error tracking  
✅ **Error Handling**: Robust failure management  
✅ **Production Ready**: Follows ML engineering best practices  

## Project Structure

```
Final Assignment/
│
├── app/
│   ├── main.py              # Flask API application
│   └── model.pkl            # Trained model (generated)
│
├── train_model.py           # Model training script
├── batch_score.py           # Batch scoring script
├── requirements.txt         # Python dependencies
├── maintenance_plan.md      # Production maintenance guide
├── README.md               # This file
│
├── gold_churn_data.csv     # Training dataset
├── all_customers.csv       # Customers to score
├── sample_input.json       # Example API input
│
├── scored_customers.csv    # Batch scoring output (generated)
├── monitoring.log          # API logs (generated)
└── batch_scoring.log       # Batch job logs (generated)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Verify installation**:
```bash
python -c "import flask, pandas, sklearn; print('All packages installed!')"
```

## Usage

### Step 1: Train the Model

Train the churn prediction model using historical data:

```bash
python train_model.py
```

**Expected Output**:
- Console output showing training progress
- `app/model.pkl` file created
- Training and test accuracy displayed

**Typical Runtime**: 10-30 seconds

### Step 2: Start the API

Launch the Flask prediction service:

```bash
python app/main.py
```

**Expected Output**:
```
============================================================
CUSTOMER CHURN PREDICTION API
============================================================
Model loaded successfully
Starting Flask server...
API will be available at: http://127.0.0.1:5000
============================================================
```

**Keep this terminal running** - the API must be active for predictions.

### Step 3: Test the API (Optional)

In a new terminal, test with sample data:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d @sample_input.json
```

**Expected Response**:
```json
{
  "prediction": "No Churn",
  "churn_probability": 0.2345,
  "no_churn_probability": 0.7655,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Step 4: Run Batch Scoring

Score all customers in the dataset:

```bash
python batch_score.py
```

**Expected Output**:
- Progress updates every 10 customers
- Summary statistics
- `scored_customers.csv` file created

**Typical Runtime**: 1-5 minutes depending on dataset size

## API Documentation

### Endpoints

#### `GET /`
Health check endpoint

**Response**:
```json
{
  "status": "running",
  "service": "Customer Churn Prediction API",
  "model_loaded": true
}
```

#### `POST /predict`
Make churn prediction for a customer

**Request Body**:
```json
{
  "customer": {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 844.20,
    "tenure_years": 1.0,
    "spend_per_month": 70.35
  }
}
```

**Response**:
```json
{
  "prediction": "Churn",
  "churn_probability": 0.7823,
  "no_churn_probability": 0.2177,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

#### `GET /health`
Detailed health status

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## Monitoring

### Log Files

**monitoring.log**: API activity and errors
```
2024-01-15 10:30:45 - INFO - Model loaded successfully
2024-01-15 10:31:12 - INFO - Prediction successful - Churn: No Churn, Probability: 0.2345
2024-01-15 10:32:03 - ERROR - Prediction failed: Missing feature 'tenure'
```

**batch_scoring.log**: Batch job execution
```
2024-01-15 11:00:00 - INFO - Batch scoring started
2024-01-15 11:05:23 - INFO - Batch scoring completed - Total: 100, Success: 98, Failed: 2
```

### Monitoring Metrics

Track these key metrics:
- **API Uptime**: Should be >99%
- **Response Time**: Should be <500ms
- **Error Rate**: Should be <1%
- **Prediction Accuracy**: Should be >80%

## Output Files

### scored_customers.csv

Contains all customer data plus predictions:

| Column | Description |
|--------|-------------|
| customerID | Unique customer identifier |
| [original features] | All input features |
| predicted_churn | "Churn" or "No Churn" |
| churn_probability | Probability of churn (0-1) |

**Use Cases**:
- Identify high-risk customers (churn_probability > 0.7)
- Target retention campaigns
- Analyze churn patterns
- Business intelligence reporting

## Troubleshooting

### Issue: Model file not found

**Error**: `Model file not found at model.pkl`

**Solution**:
```bash
python train_model.py
```

### Issue: API not reachable

**Error**: `API is not reachable`

**Solution**:
1. Ensure API is running: `python app/main.py`
2. Check port 5000 is not in use
3. Verify firewall settings

### Issue: Missing dependencies

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Batch scoring fails

**Error**: `Input file 'all_customers.csv' not found`

**Solution**:
- Ensure `all_customers.csv` exists in project root
- Check file path and permissions

## Maintenance

Refer to `maintenance_plan.md` for:
- Model retraining schedule
- Drift monitoring procedures
- Version control strategy
- Failure handling protocols
- Documentation standards

## Performance Optimization

### For Large Datasets

1. **Batch API Requests**: Modify batch_score.py to send multiple customers per request
2. **Parallel Processing**: Use multiprocessing for batch scoring
3. **Caching**: Implement Redis for frequent predictions
4. **Load Balancing**: Deploy multiple API instances

### For Production

1. **Use Gunicorn**: Replace Flask dev server
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
   ```

2. **Add Authentication**: Implement API keys or OAuth

3. **Rate Limiting**: Prevent API abuse

4. **Containerization**: Use Docker for deployment

## Model Information

**Algorithm**: Random Forest Classifier  
**Features**: 23 (numeric and categorical)  
**Target**: Binary classification (Churn/No Churn)  
**Preprocessing**: StandardScaler + OneHotEncoder  
**Expected Accuracy**: ~80-85%  

## Business Value

This system enables:
- **Proactive Retention**: Identify at-risk customers before they churn
- **Targeted Campaigns**: Focus resources on high-risk segments
- **Cost Savings**: Reduce customer acquisition costs
- **Revenue Protection**: Retain valuable customers
- **Data-Driven Decisions**: Replace intuition with predictions

## Future Enhancements

- [ ] Add model explainability (SHAP values)
- [ ] Implement A/B testing framework
- [ ] Create monitoring dashboard
- [ ] Add automated retraining pipeline
- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Implement feature store
- [ ] Add model versioning API
- [ ] Create customer segmentation

## Contributing

For improvements or bug fixes:
1. Document the issue
2. Test changes thoroughly
3. Update relevant documentation
4. Follow code style guidelines

## License

Internal use only - Company Confidential

## Support

For issues or questions:
- Check troubleshooting section
- Review logs (monitoring.log, batch_scoring.log)
- Contact ML Engineering team

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Author**: ML Engineering Team
