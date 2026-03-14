"""
Customer Churn Model Training Script
Trains a classification model and saves it as a serialized pipeline
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import joblib
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data(filepath='gold_churn_data.csv'):
    """Load and prepare the churn dataset"""
    print("Loading data...")
    df = pd.read_csv(filepath)
    
    # Drop unnecessary columns
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
    
    # Handle TotalCharges - convert to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['MonthlyCharges'], inplace=True)
    
    print(f"Dataset shape: {df.shape}")
    return df

def preprocess_features(df):
    """Separate features and target, identify column types"""
    # Target variable
    y = df['Churn'].map({'Yes': 1, 'No': 0})
    X = df.drop('Churn', axis=1)
    
    # Identify numeric and categorical columns
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    
    print(f"Numeric features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)}")
    
    return X, y, numeric_features, categorical_features

def build_pipeline(numeric_features, categorical_features):
    """Build sklearn pipeline with preprocessing and model"""
    
    # Preprocessing for numeric and categorical data
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Create pipeline with preprocessor and classifier
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    return pipeline

def train_and_save_model(X, y, pipeline, model_path='app/model.pkl'):
    """Train the model and save it"""
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    print("\nTraining model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate on test set
    train_score = pipeline.score(X_train, y_train)
    test_score = pipeline.score(X_test, y_test)
    
    print(f"\nModel Performance:")
    print(f"Training Accuracy: {train_score:.4f}")
    print(f"Test Accuracy: {test_score:.4f}")
    
    # Save the trained pipeline
    print(f"\nSaving model to {model_path}...")
    joblib.dump(pipeline, model_path)
    print("Model saved successfully!")
    
    return pipeline, test_score

def main():
    """Main training workflow"""
    print("="*60)
    print("CUSTOMER CHURN MODEL TRAINING")
    print("="*60)
    
    # Load data
    df = load_and_prepare_data()
    
    # Preprocess
    X, y, numeric_features, categorical_features = preprocess_features(df)
    
    # Build pipeline
    pipeline = build_pipeline(numeric_features, categorical_features)
    
    # Train and save
    trained_pipeline, accuracy = train_and_save_model(X, y, pipeline)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"Final Model Accuracy: {accuracy:.4f}")
    print("Model ready for deployment!")

if __name__ == "__main__":
    main()
