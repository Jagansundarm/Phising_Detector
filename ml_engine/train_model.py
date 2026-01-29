"""
Machine Learning Model Training Script
Trains LightGBM classifier for phishing detection
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix,
    classification_report
)
import lightgbm as lgb
from feature_extractor import URLFeatureExtractor
import matplotlib.pyplot as plt
import seaborn as sns


class PhishingDetectionModel:
    """Phishing URL Detection Model Trainer"""
    
    def __init__(self):
        self.feature_extractor = URLFeatureExtractor()
        self.model = None
        self.metrics = {}
        
    def load_data(self, csv_path="ml_engine/data/phishing_dataset.csv"):
        """Load dataset from CSV"""
        print(f"📂 Loading dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
        print(f"   Loaded {len(df)} samples")
        return df
    
    def prepare_features(self, df):
        """Extract features from URLs"""
        print("🔧 Extracting features from URLs...")
        
        urls = df['url'].values
        labels = df['label'].values
        
        # Extract features
        X = self.feature_extractor.extract_batch(urls)
        y = labels
        
        print(f"   Feature matrix shape: {X.shape}")
        print(f"   Features: {len(self.feature_extractor.feature_names)}")
        
        return X, y
    
    def train(self, X, y, test_size=0.2, random_state=42):
        """Train LightGBM model"""
        print("\n🚀 Training LightGBM model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"   Training samples: {len(X_train)}")
        print(f"   Testing samples: {len(X_test)}")
        
        # Create LightGBM datasets
        train_data = lgb.Dataset(X_train, label=y_train)
        test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
        
        # Model parameters
        params = {
            'objective': 'binary',
            'metric': 'binary_logloss',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': 0
        }
        
        # Train
        print("   Training in progress...")
        self.model = lgb.train(
            params,
            train_data,
            num_boost_round=100,
            valid_sets=[test_data],
            callbacks=[lgb.early_stopping(stopping_rounds=10)]
        )
        
        print("   ✅ Training complete!")
        
        # Evaluate
        self.evaluate(X_test, y_test)
        
        return X_train, X_test, y_train, y_test
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        print("\n📊 Evaluating model performance...")
        
        # Predictions
        y_pred_proba = self.model.predict(X_test)
        y_pred = (y_pred_proba > 0.5).astype(int)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        self.metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        
        print(f"\n{'='*50}")
        print(f"   PERFORMANCE METRICS")
        print(f"{'='*50}")
        print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
        print(f"   F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
        print(f"{'='*50}\n")
        
        # Classification report
        print("Detailed Classification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Legitimate', 'Phishing']))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\nConfusion Matrix:")
        print(f"                 Predicted")
        print(f"              Legit  Phishing")
        print(f"Actual Legit    {cm[0][0]:4d}    {cm[0][1]:4d}")
        print(f"       Phishing {cm[1][0]:4d}    {cm[1][1]:4d}\n")
        
        return self.metrics
    
    def save_model(self, output_dir="ml_engine/models"):
        """Save trained model and metadata"""
        print(f"💾 Saving model to {output_dir}...")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Save LightGBM model
        model_path = f"{output_dir}/phishing_model.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"   ✅ Model saved: {model_path}")
        
        # Save feature names
        features_path = f"{output_dir}/feature_names.json"
        with open(features_path, 'w') as f:
            json.dump(self.feature_extractor.feature_names, f, indent=2)
        print(f"   ✅ Features saved: {features_path}")
        
        # Save metrics
        metrics_path = f"{output_dir}/metrics.json"
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"   ✅ Metrics saved: {metrics_path}")
        
        print("\n✅ All files saved successfully!")
    
    def predict(self, url):
        """Predict single URL"""
        features = self.feature_extractor.extract_features(url)
        features = features.reshape(1, -1)
        
        probability = self.model.predict(features)[0]
        prediction = 1 if probability > 0.5 else 0
        
        return {
            'prediction': 'phishing' if prediction == 1 else 'legitimate',
            'confidence': float(probability if prediction == 1 else 1 - probability),
            'label': int(prediction)
        }


def main():
    """Main training pipeline"""
    print("=" * 60)
    print("PHISHING DETECTION MODEL TRAINING")
    print("=" * 60 + "\n")
    
    # Initialize
    trainer = PhishingDetectionModel()
    
    # Load data
    df = trainer.load_data()
    
    # Prepare features
    X, y = trainer.prepare_features(df)
    
    # Train model
    X_train, X_test, y_train, y_test = trainer.train(X, y)
    
    # Save model
    trainer.save_model()
    
    # Test predictions
    print("\n" + "="*60)
    print("TESTING PREDICTIONS")
    print("="*60 + "\n")
    
    test_urls = [
        "https://www.google.com",
        "http://secure.bankofamerica.verify.update-account.net",
        "https://www.github.com",
        "http://paypal-secure.login-verification.com/signin"
    ]
    
    for url in test_urls:
        result = trainer.predict(url)
        print(f"URL: {url}")
        print(f"  → Prediction: {result['prediction'].upper()}")
        print(f"  → Confidence: {result['confidence']:.2%}\n")
    
    print("="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Check ml_engine/models/ for saved files")
    print("  2. Run 'python ml_engine/convert_to_tflite.py' for mobile")
    print("  3. Proceed to backend development")


if __name__ == "__main__":
    main()
