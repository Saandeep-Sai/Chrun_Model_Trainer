# Recommended Project Folder Structure

## Final Production-Ready Structure

```
Final Assignment/
│
├── app/                          # Flask API application
│   ├── __init__.py              # Package initializer (optional)
│   ├── main.py                  # Flask API server
│   └── model.pkl                # Trained model pipeline (generated)
│
├── data/                         # Data directory (optional organization)
│   ├── raw/
│   │   └── gold_churn_data.csv  # Original training data
│   ├── processed/
│   │   └── all_customers.csv    # Customers to score
│   └── output/
│       └── scored_customers.csv # Batch predictions (generated)
│
├── logs/                         # Centralized logs (optional)
│   ├── monitoring.log           # API logs (generated)
│   └── batch_scoring.log        # Batch job logs (generated)
│
├── models/                       # Model versioning (optional)
│   ├── v1.0.0/
│   │   ├── model.pkl
│   │   └── metadata.json
│   └── current -> v1.0.0/       # Symlink to active version
│
├── notebooks/                    # Jupyter notebooks (optional)
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── tests/                        # Unit tests (optional)
│   ├── test_api.py
│   ├── test_model.py
│   └── test_batch_scoring.py
│
├── docs/                         # Documentation (optional)
│   ├── api_documentation.md
│   ├── deployment_guide.md
│   └── troubleshooting.md
│
├── scripts/                      # Utility scripts (optional)
│   ├── deploy.sh
│   ├── backup_model.sh
│   └── monitor_health.py
│
├── config/                       # Configuration files (optional)
│   ├── config.yaml
│   └── logging_config.yaml
│
├── train_model.py               # Model training script
├── batch_score.py               # Batch scoring script
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── maintenance_plan.md          # Maintenance strategy
├── monitoring_strategy.md       # Monitoring guide
│
├── .gitignore                   # Git ignore file
├── .env                         # Environment variables (not in git)
├── Dockerfile                   # Docker configuration (optional)
└── docker-compose.yml           # Docker compose (optional)
```

---

## Current Minimal Structure (As Created)

```
Final Assignment/
│
├── app/
│   ├── main.py                  # Flask API
│   └── model.pkl                # Trained model (after training)
│
├── train_model.py               # Training script
├── batch_score.py               # Batch scoring
├── requirements.txt             # Dependencies
├── README.md                    # Main documentation
├── maintenance_plan.md          # Maintenance guide
├── monitoring_strategy.md       # Monitoring guide
│
├── gold_churn_data.csv         # Training data
├── all_customers.csv           # Customers to score
├── sample_input.json           # Example API input
│
├── scored_customers.csv        # Output (generated)
├── monitoring.log              # API logs (generated)
└── batch_scoring.log           # Batch logs (generated)
```

---

## File Descriptions

### Core Application Files

**train_model.py**
- Purpose: Train and save the churn prediction model
- Input: gold_churn_data.csv
- Output: app/model.pkl
- Run: `python train_model.py`

**app/main.py**
- Purpose: Flask API for real-time predictions
- Input: JSON customer data via POST
- Output: Prediction + probability
- Run: `python app/main.py`

**batch_score.py**
- Purpose: Score multiple customers via API
- Input: all_customers.csv
- Output: scored_customers.csv
- Run: `python batch_score.py`

### Configuration Files

**requirements.txt**
- Purpose: Python package dependencies
- Usage: `pip install -r requirements.txt`
- Contains: Flask, pandas, scikit-learn, etc.

**sample_input.json**
- Purpose: Example API request format
- Usage: Testing and documentation
- Format: JSON with customer features

### Documentation Files

**README.md**
- Purpose: Main project documentation
- Contains: Setup, usage, API docs, troubleshooting
- Audience: Developers and users

**maintenance_plan.md**
- Purpose: Production maintenance strategy
- Contains: Retraining, monitoring, versioning
- Audience: ML engineers and ops team

**monitoring_strategy.md**
- Purpose: Monitoring and alerting guide
- Contains: Metrics, logging, dashboards
- Audience: DevOps and ML engineers

### Data Files

**gold_churn_data.csv**
- Purpose: Historical customer data for training
- Size: ~1000+ records
- Contains: Customer features + churn label

**all_customers.csv**
- Purpose: Current customers to score
- Size: Variable
- Contains: Customer features (no label)

**scored_customers.csv** (generated)
- Purpose: Predictions for all customers
- Contains: Original data + predictions + probabilities
- Usage: Business intelligence, retention campaigns

### Generated Files

**app/model.pkl**
- Purpose: Serialized trained model pipeline
- Size: ~1-5 MB
- Format: Joblib pickle file
- Contains: Preprocessor + trained classifier

**monitoring.log**
- Purpose: API activity and error logs
- Rotation: Daily
- Contains: Timestamps, predictions, errors

**batch_scoring.log**
- Purpose: Batch job execution logs
- Rotation: Weekly
- Contains: Job status, success/failure counts

---

## Deployment Structures

### Development Environment
```
Final Assignment/
├── app/
├── train_model.py
├── batch_score.py
├── requirements.txt
└── [data files]
```

### Production Environment
```
/opt/churn-prediction/
├── app/
│   ├── main.py
│   └── model.pkl
├── config/
│   └── production.yaml
├── logs/
│   ├── monitoring.log
│   └── batch_scoring.log
├── scripts/
│   ├── start_api.sh
│   └── run_batch.sh
└── requirements.txt
```

### Docker Container Structure
```
/app/
├── app/
│   ├── main.py
│   └── model.pkl
├── requirements.txt
└── entrypoint.sh
```

---

## Best Practices

### File Organization

1. **Separate concerns**: Keep training, serving, and scoring separate
2. **Version models**: Use versioned directories for models
3. **Centralize logs**: Keep all logs in one location
4. **Document everything**: README for each major component
5. **Use .gitignore**: Don't commit generated files or data

### Naming Conventions

- **Scripts**: Lowercase with underscores (train_model.py)
- **Modules**: Lowercase with underscores (data_processor.py)
- **Classes**: PascalCase (ChurnPredictor)
- **Functions**: Lowercase with underscores (load_data)
- **Constants**: UPPERCASE (MODEL_PATH)

### Directory Guidelines

- **app/**: Only production API code
- **data/**: All data files (with subdirectories)
- **logs/**: All log files
- **models/**: Versioned model artifacts
- **tests/**: All test files
- **docs/**: All documentation

---

## Git Repository Structure

### .gitignore
```
# Generated files
*.pkl
*.log
scored_customers.csv

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Data (optional - depends on size)
*.csv
data/raw/
data/processed/
```

### Repository Layout
```
churn-prediction/
├── .git/
├── .gitignore
├── README.md
├── requirements.txt
├── app/
├── train_model.py
├── batch_score.py
└── docs/
```

---

## Scalability Considerations

### For Large Teams
```
churn-prediction/
├── src/
│   ├── data/
│   │   ├── loader.py
│   │   └── preprocessor.py
│   ├── models/
│   │   ├── trainer.py
│   │   └── predictor.py
│   ├── api/
│   │   ├── app.py
│   │   └── routes.py
│   └── utils/
│       ├── logger.py
│       └── config.py
├── tests/
├── docs/
└── setup.py
```

### For Microservices
```
churn-prediction/
├── training-service/
│   ├── Dockerfile
│   ├── train_model.py
│   └── requirements.txt
├── prediction-service/
│   ├── Dockerfile
│   ├── app/
│   └── requirements.txt
├── batch-service/
│   ├── Dockerfile
│   ├── batch_score.py
│   └── requirements.txt
└── docker-compose.yml
```

---

## Migration Path

### From Current to Enhanced Structure

**Step 1**: Create directories
```bash
mkdir -p data/{raw,processed,output}
mkdir -p logs
mkdir -p models/v1.0.0
```

**Step 2**: Move files
```bash
mv gold_churn_data.csv data/raw/
mv all_customers.csv data/processed/
mv scored_customers.csv data/output/
mv *.log logs/
mv app/model.pkl models/v1.0.0/
```

**Step 3**: Update paths in code
- Modify train_model.py to use new paths
- Update app/main.py model path
- Adjust batch_score.py file paths

**Step 4**: Create symlink
```bash
ln -s models/v1.0.0/model.pkl app/model.pkl
```

---

## Summary

The current structure is **production-ready** for a single-server deployment. For enhanced scalability and team collaboration, consider the expanded structure with:

- Versioned model directories
- Centralized logging
- Comprehensive testing
- Docker containerization
- CI/CD integration

Choose the structure that matches your deployment complexity and team size.
