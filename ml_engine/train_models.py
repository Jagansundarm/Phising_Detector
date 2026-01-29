"""
Multi-Model Training Pipeline for Phishing Detection
Trains and compares multiple ML models following research methodology

Models:
1. Logistic Regression (baseline)
2. Random Forest
3. LightGBM
4. XGBoost (optional)

Evaluation Metrics:
- Precision, Recall, F1-score
- ROC-AUC
- Confusion Matrix
- Feature Importance
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path
from datetime import datetime

# ML libraries
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
import lightgbm as lgb
import xgboost as xgb

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Feature extraction
from advanced_feature_extractor import AdvancedFeatureExtractor


class MultiModelTrainer:
    """Train and compare multiple ML models"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.feature_extractor = AdvancedFeatureExtractor()
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        self.best_model = None
        self.best_model_name = None
        
    def load_and_prepare_data(self, data_path='ml_engine/data/phishing_dataset.csv'):
        """Load dataset and extract features"""
        print("=" * 80)
        print("LOADING AND PREPARING DATA")
        print("=" * 80)
        
        # Load dataset
        df = pd.read_csv(data_path)
        print(f"✅ Loaded {len(df)} URLs")
        print(f"   Phishing: {sum(df['label'] == 1)}")
        print(f"   Legitimate: {sum(df['label'] == 0)}")
        
        # Extract features
        print("\n🔄 Extracting advanced features...")
        features_list = []
        
        for idx, url in enumerate(df['url']):
            if idx % 50 == 0:
                print(f"   Processed {idx}/{len(df)} URLs...")
            features = self.feature_extractor.extract_features(url)
            features_list.append(features)
        
        X = np.array(features_list)
        y = df['label'].values
        
        print(f"✅ Feature extraction complete")
        print(f"   Feature shape: {X.shape}")
        print(f"   Feature names: {len(self.feature_extractor.get_feature_names())}")
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2, val_size=0.1):
        """Split data into train, validation, and test sets"""
        print("\n" + "=" * 80)
        print("SPLITTING DATA")
        print("=" * 80)
        
        # First split: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        # Second split: train vs val
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=self.random_state, stratify=y_temp
        )
        
        print(f"✅ Train set: {len(X_train)} samples")
        print(f"✅ Validation set: {len(X_val)} samples")
        print(f"✅ Test set: {len(X_test)} samples")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test
    
    def train_models(self, X_train, y_train):
        """Train all models"""
        print("\n" + "=" * 80)
        print("TRAINING MODELS")
        print("=" * 80)
        
        # Define models
        self.models = {
            'Logistic Regression': LogisticRegression(
                random_state=self.random_state,
                max_iter=1000,
                class_weight='balanced'
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                random_state=self.random_state,
                class_weight='balanced',
                max_depth=10,
                min_samples_split=5
            ),
            'LightGBM': lgb.LGBMClassifier(
                n_estimators=100,
                random_state=self.random_state,
                class_weight='balanced',
                max_depth=7,
                learning_rate=0.1
            ),
            'XGBoost': xgb.XGBClassifier(
                n_estimators=100,
                random_state=self.random_state,
                max_depth=7,
                learning_rate=0.1,
                scale_pos_weight=1,
                eval_metric='logloss'
            )
        }
        
        # Train each model
        for name, model in self.models.items():
            print(f"\n🔄 Training {name}...")
            model.fit(X_train, y_train)
            print(f"✅ {name} trained successfully")
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all models"""
        print("\n" + "=" * 80)
        print("EVALUATING MODELS")
        print("=" * 80)
        
        for name, model in self.models.items():
            print(f"\n📊 Evaluating {name}...")
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred),
                'recall': recall_score(y_test, y_pred),
                'f1_score': f1_score(y_test, y_pred),
                'roc_auc': roc_auc_score(y_test, y_pred_proba),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
            }
            
            self.results[name] = metrics
            
            # Print results
            print(f"   Accuracy:  {metrics['accuracy']:.4f}")
            print(f"   Precision: {metrics['precision']:.4f}")
            print(f"   Recall:    {metrics['recall']:.4f}")
            print(f"   F1-Score:  {metrics['f1_score']:.4f}")
            print(f"   ROC-AUC:   {metrics['roc_auc']:.4f}")
    
    def select_best_model(self):
        """Select best model based on F1-score"""
        print("\n" + "=" * 80)
        print("SELECTING BEST MODEL")
        print("=" * 80)
        
        best_f1 = 0
        best_name = None
        
        for name, metrics in self.results.items():
            if metrics['f1_score'] > best_f1:
                best_f1 = metrics['f1_score']
                best_name = name
        
        self.best_model_name = best_name
        self.best_model = self.models[best_name]
        
        print(f"🏆 Best Model: {best_name}")
        print(f"   F1-Score: {best_f1:.4f}")
        
        return best_name, self.best_model
    
    def save_models(self, output_dir='ml_engine/models'):
        """Save all models and results"""
        print("\n" + "=" * 80)
        print("SAVING MODELS")
        print("=" * 80)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save best model
        model_path = output_path / 'phishing_model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        print(f"✅ Saved best model: {model_path}")
        
        # Save scaler
        scaler_path = output_path / 'scaler.pkl'
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"✅ Saved scaler: {scaler_path}")
        
        # Save feature names
        feature_names_path = output_path / 'feature_names.json'
        with open(feature_names_path, 'w') as f:
            json.dump(self.feature_extractor.get_feature_names(), f, indent=2)
        print(f"✅ Saved feature names: {feature_names_path}")
        
        # Save results
        results_path = output_path / 'model_comparison.json'
        with open(results_path, 'w') as f:
            json.dump({
                'best_model': self.best_model_name,
                'results': self.results,
                'training_date': datetime.now().isoformat()
            }, f, indent=2)
        print(f"✅ Saved results: {results_path}")
    
    def plot_comparison(self, output_dir='ml_engine/models'):
        """Create comparison visualizations"""
        print("\n" + "=" * 80)
        print("CREATING VISUALIZATIONS")
        print("=" * 80)
        
        output_path = Path(output_dir)
        
        # 1. Metrics comparison bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        metrics_to_plot = ['precision', 'recall', 'f1_score', 'roc_auc']
        x = np.arange(len(self.results))
        width = 0.2
        
        for i, metric in enumerate(metrics_to_plot):
            values = [self.results[model][metric] for model in self.results.keys()]
            ax.bar(x + i * width, values, width, label=metric.replace('_', ' ').title())
        
        ax.set_xlabel('Models')
        ax.set_ylabel('Score')
        ax.set_title('Model Performance Comparison')
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(self.results.keys(), rotation=15, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / 'model_comparison.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved comparison chart")
        plt.close()
        
        # 2. Confusion matrices
        fig, axes = plt.subplots(1, len(self.results), figsize=(15, 4))
        
        for idx, (name, metrics) in enumerate(self.results.items()):
            cm = np.array(metrics['confusion_matrix'])
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
            axes[idx].set_title(f'{name}\nF1: {metrics["f1_score"]:.3f}')
            axes[idx].set_ylabel('True Label')
            axes[idx].set_xlabel('Predicted Label')
        
        plt.tight_layout()
        plt.savefig(output_path / 'confusion_matrices.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved confusion matrices")
        plt.close()


def main():
    """Main training pipeline"""
    print("\n" + "=" * 80)
    print("RESEARCH-ALIGNED PHISHING DETECTION - MULTI-MODEL TRAINING")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize trainer
    trainer = MultiModelTrainer(random_state=42)
    
    # Load and prepare data
    X, y = trainer.load_and_prepare_data()
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.split_data(X, y)
    
    # Train models
    trainer.train_models(X_train, y_train)
    
    # Evaluate models
    trainer.evaluate_models(X_test, y_test)
    
    # Select best model
    trainer.select_best_model()
    
    # Save models
    trainer.save_models()
    
    # Create visualizations
    trainer.plot_comparison()
    
    print("\n" + "=" * 80)
    print("✅ TRAINING COMPLETE")
    print("=" * 80)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nNext steps:")
    print("1. Review model_comparison.json for detailed metrics")
    print("2. Check confusion_matrices.png for error analysis")
    print("3. Proceed to backend deployment")


if __name__ == "__main__":
    main()
