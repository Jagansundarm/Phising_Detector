"""
Convert trained model to TensorFlow Lite format for mobile deployment
"""

import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import json
from feature_extractor import URLFeatureExtractor


class ModelConverter:
    """Convert LightGBM model to TensorFlow Lite"""
    
    def __init__(self, model_path="ml_engine/models/phishing_model.pkl"):
        """Load the trained LightGBM model"""
        print(f"📂 Loading model from {model_path}...")
        with open(model_path, 'rb') as f:
            self.lgb_model = pickle.load(f)
        print("   ✅ Model loaded successfully")
        
        self.feature_extractor = URLFeatureExtractor()
        self.num_features = len(self.feature_extractor.feature_names)
    
    def create_keras_model(self, X_sample):
        """
        Create a Keras model that mimics the LightGBM predictions
        Uses knowledge distillation approach
        """
        print("\n🔧 Creating TensorFlow/Keras equivalent model...")
        
        # Create a simple neural network
        model = keras.Sequential([
            keras.layers.Input(shape=(self.num_features,)),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        print("   Model architecture:")
        model.summary()
        
        return model
    
    def train_keras_model(self, X_train, y_train):
        """
        Train Keras model using LightGBM predictions as soft labels
        (Knowledge Distillation)
        """
        print("\n🚀 Training TensorFlow model...")
        
        # Get LightGBM predictions as soft labels
        lgb_predictions = self.lgb_model.predict(X_train)
        
        # Create and train Keras model
        keras_model = self.create_keras_model(X_train)
        
        history = keras_model.fit(
            X_train,
            lgb_predictions,  # Use LightGBM predictions as targets
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )
        
        print("   ✅ Training complete!")
        
        return keras_model
    
    def convert_to_tflite(self, keras_model, output_path="ml_engine/models/phishing_model.tflite"):
        """Convert Keras model to TFLite format"""
        print(f"\n📦 Converting to TensorFlow Lite...")
        
        # Convert the model
        converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
        
        # Optimization (optional, reduces model size)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        
        tflite_model = converter.convert()
        
        # Save the model
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        file_size = len(tflite_model) / 1024  # KB
        print(f"   ✅ TFLite model saved: {output_path}")
        print(f"   📊 Model size: {file_size:.2f} KB")
        
        return output_path
    
    def test_tflite_model(self, tflite_path, test_urls):
        """Test the TFLite model"""
        print(f"\n🧪 Testing TFLite model...")
        
        # Load TFLite model
        interpreter = tf.lite.Interpreter(model_path=tflite_path)
        interpreter.allocate_tensors()
        
        # Get input/output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        print("\nTest Results:")
        print("="*60)
        
        for url in test_urls:
            # Extract features
            features = self.feature_extractor.extract_features(url)
            features = features.reshape(1, -1).astype(np.float32)
            
            # Run inference
            interpreter.set_tensor(input_details[0]['index'], features)
            interpreter.invoke()
            
            # Get prediction
            output = interpreter.get_tensor(output_details[0]['index'])
            probability = output[0][0]
            prediction = 'PHISHING' if probability > 0.5 else 'LEGITIMATE'
            confidence = probability if probability > 0.5 else 1 - probability
            
            print(f"\nURL: {url}")
            print(f"  → Prediction: {prediction}")
            print(f"  → Confidence: {confidence:.2%}")
        
        print("="*60)


def create_sample_training_data():
    """
    Create sample training data for demonstration
    In production, use actual dataset
    """
    from download_dataset import create_dataset
    import pandas as pd
    
    # Create sample dataset
    df = create_dataset()
    
    # Extract features
    extractor = URLFeatureExtractor()
    X = extractor.extract_batch(df['url'].values)
    y = df['label'].values
    
    return X, y


def main():
    """Main conversion pipeline"""
    print("=" * 60)
    print("TFLITE MODEL CONVERSION")
    print("=" * 60 + "\n")
    
    try:
        # Load LightGBM model
        converter = ModelConverter()
        
        # Load or create training data
        print("\n📊 Preparing training data...")
        X_train, y_train = create_sample_training_data()
        print(f"   Training samples: {len(X_train)}")
        
        # Train Keras equivalent
        keras_model = converter.train_keras_model(X_train, y_train)
        
        # Save Keras model
        keras_path = "ml_engine/models/phishing_model_keras.h5"
        keras_model.save(keras_path)
        print(f"\n💾 Keras model saved: {keras_path}")
        
        # Convert to TFLite
        tflite_path = converter.convert_to_tflite(keras_model)
        
        # Test the model
        test_urls = [
            "https://www.google.com",
            "http://paypal-secure.login-verification.com/signin",
            "https://www.github.com",
            "http://secure.bankofamerica.verify.update-account.net"
        ]
        
        converter.test_tflite_model(tflite_path, test_urls)
        
        print("\n" + "="*60)
        print("✅ CONVERSION COMPLETE!")
        print("="*60)
        print(f"\nGenerated files:")
        print(f"  1. Keras model: ml_engine/models/phishing_model_keras.h5")
        print(f"  2. TFLite model: ml_engine/models/phishing_model.tflite")
        print(f"\nThe .tflite file can be used in:")
        print(f"  • Flutter apps (tflite_flutter package)")
        print(f"  • React Native (react-native-tensorflow-lite)")
        print(f"  • Native Android/iOS apps")
        
    except FileNotFoundError:
        print("\n❌ Error: Model not found!")
        print("   Please run 'python ml_engine/train_model.py' first")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
