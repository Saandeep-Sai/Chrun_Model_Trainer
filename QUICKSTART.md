# Quick Start Guide

## Get Started in 5 Minutes

This guide will get your churn prediction system running quickly.

---

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check pip
pip --version
```

---

## Step-by-Step Setup

### 1. Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

**Expected output**: Successfully installed Flask, pandas, scikit-learn...

---

### 2. Train the Model (30 seconds)

```bash
python train_model.py
```

**Expected output**:
```
============================================================
CUSTOMER CHURN MODEL TRAINING
============================================================
Loading data...
Dataset shape: (1043, 24)
Numeric features: 5
Categorical features: 18

Splitting data...
Training set size: 834
Test set size: 209

Training model...

Model Performance:
Training Accuracy: 0.8513
Test Accuracy: 0.8134

Saving model to app/model.pkl...
Model saved successfully!

============================================================
TRAINING COMPLETE
============================================================
```

**✓ Success**: You should now have `app/model.pkl` file

---

### 3. Start the API (10 seconds)

```bash
python app/main.py
```

**Expected output**:
```
============================================================
CUSTOMER CHURN PREDICTION API
============================================================
Model loaded successfully
Starting Flask server...
API will be available at: http://127.0.0.1:5000
============================================================
 * Running on http://0.0.0.0:5000
```

**✓ Success**: API is now running

**⚠️ Keep this terminal open!**

---

### 4. Test the API (30 seconds)

Open a **new terminal** and run:

#### Option A: Using curl (Linux/Mac/Windows Git Bash)
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d @sample_input.json
```

#### Option B: Using Python
```python
import requests
import json

with open('sample_input.json', 'r') as f:
    data = json.load(f)

response = requests.post('http://127.0.0.1:5000/predict', json=data)
print(response.json())
```

#### Option C: Using PowerShell (Windows)
```powershell
$body = Get-Content sample_input.json -Raw
Invoke-RestMethod -Uri http://127.0.0.1:5000/predict -Method Post -Body $body -ContentType "application/json"
```

**Expected response**:
```json
{
  "prediction": "No Churn",
  "churn_probability": 0.2345,
  "no_churn_probability": 0.7655,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**✓ Success**: API is working correctly!

---

### 5. Run Batch Scoring (2 minutes)

In the **new terminal** (keep API running in first terminal):

```bash
python batch_score.py
```

**Expected output**:
```
============================================================
BATCH CUSTOMER SCORING
============================================================
Start Time: 2024-01-15 10:30:45
============================================================
✓ API is running and healthy
Loading customers from all_customers.csv...
Loaded 53 customers

Starting batch scoring for 53 customers...
============================================================
Processed 10/53 customers...
Processed 20/53 customers...
Processed 30/53 customers...
Processed 40/53 customers...
Processed 50/53 customers...
============================================================

Batch scoring complete!
Total customers: 53
Successful predictions: 53
Failed predictions: 0
Time elapsed: 5.23 seconds
Average time per customer: 0.099 seconds

Saving results to scored_customers.csv...
✓ Results saved successfully!
  File: scored_customers.csv
  Rows: 53

Prediction Summary:
No Churn    38
Churn       15

Average Churn Probability: 0.3421
High Risk Customers (>70% churn prob): 8

============================================================
BATCH SCORING COMPLETED SUCCESSFULLY
============================================================
```

**✓ Success**: Check `scored_customers.csv` for results!

---

## Verify Everything Works

### Check Generated Files

```bash
# Windows
dir app\model.pkl
dir scored_customers.csv
dir monitoring.log

# Linux/Mac
ls -lh app/model.pkl
ls -lh scored_customers.csv
ls -lh monitoring.log
```

You should see:
- ✓ `app/model.pkl` (~1-5 MB)
- ✓ `scored_customers.csv` (with predictions)
- ✓ `monitoring.log` (with API logs)
- ✓ `batch_scoring.log` (with batch logs)

---

## Common Issues & Quick Fixes

### Issue 1: "Model file not found"

**Problem**: Forgot to train model

**Fix**:
```bash
python train_model.py
```

---

### Issue 2: "Port 5000 already in use"

**Problem**: Another application using port 5000

**Fix**: Kill the process or change port in `app/main.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=False)  # Change to 5001
```

---

### Issue 3: "API is not reachable"

**Problem**: API not running

**Fix**: Start API in separate terminal:
```bash
python app/main.py
```

---

### Issue 4: "Module not found"

**Problem**: Dependencies not installed

**Fix**:
```bash
pip install -r requirements.txt
```

---

### Issue 5: "Permission denied"

**Problem**: File permissions (Linux/Mac)

**Fix**:
```bash
chmod +x train_model.py
chmod +x batch_score.py
```

---

## What to Do Next

### 1. Explore the Results

Open `scored_customers.csv` in Excel or any spreadsheet application:
- See predictions for each customer
- Identify high-risk customers (churn_probability > 0.7)
- Analyze patterns

### 2. Check the Logs

```bash
# View API logs
cat monitoring.log

# View batch logs
cat batch_scoring.log
```

### 3. Make Custom Predictions

Create your own JSON file:

```json
{
  "customer": {
    "gender": "Male",
    "SeniorCitizen": 1,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 6,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.50,
    "TotalCharges": 573.00,
    "tenure_years": 0.5,
    "spend_per_month": 95.50
  }
}
```

Save as `my_customer.json` and test:
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d @my_customer.json
```

### 4. Read the Documentation

- **README.md**: Complete documentation
- **maintenance_plan.md**: Production maintenance
- **monitoring_strategy.md**: Monitoring guide
- **PROJECT_STRUCTURE.md**: File organization

---

## Stopping the System

### Stop the API

In the terminal running the API, press:
```
Ctrl + C
```

### Clean Up (Optional)

To remove generated files:
```bash
# Windows
del app\model.pkl
del scored_customers.csv
del *.log

# Linux/Mac
rm app/model.pkl
rm scored_customers.csv
rm *.log
```

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Test with real data
- [ ] Set up monitoring alerts
- [ ] Configure log rotation
- [ ] Add authentication to API
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up automated backups
- [ ] Document deployment process
- [ ] Create rollback plan
- [ ] Schedule regular retraining
- [ ] Set up health checks

---

## Getting Help

### Check Logs First
```bash
# API errors
tail -n 50 monitoring.log

# Batch errors
tail -n 50 batch_scoring.log
```

### Common Log Messages

**"Model loaded successfully"** ✓ Good  
**"Prediction successful"** ✓ Good  
**"Model file not found"** ✗ Run train_model.py  
**"Prediction failed: Missing feature"** ✗ Check input data  
**"API error: 500"** ✗ Check API logs  

### Resources

- **README.md**: Full documentation
- **Troubleshooting section**: Common issues
- **API Documentation**: Endpoint details
- **Monitoring logs**: Error details

---

## Success Criteria

You've successfully set up the system if:

✓ Model trains without errors  
✓ API starts and responds to health checks  
✓ Single predictions work via API  
✓ Batch scoring completes successfully  
✓ Output files are generated  
✓ Logs show no critical errors  

---

## Next Steps

1. **Customize**: Modify for your specific use case
2. **Integrate**: Connect to your business systems
3. **Monitor**: Set up dashboards and alerts
4. **Optimize**: Improve performance as needed
5. **Scale**: Deploy to production infrastructure

---

**Congratulations! Your churn prediction system is ready to use! 🎉**

For detailed information, see **README.md**
