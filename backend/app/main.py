"""
Enhanced Backend API with Research-Aligned Features
Provides prediction with feature explanation and model metadata
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional
import pickle
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from .advanced_feature_extractor import AdvancedFeatureExtractor


app = FastAPI(
    title="Phishing URL Detection API",
    description="Research-aligned early detection of phishing URLs in parked domains",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLRequest(BaseModel):
    url: str


class PredictionResponse(BaseModel):
    url: str
    prediction: str
    confidence: float
    probability: float
    risk_level: str
    is_safe: bool
    timestamp: str


class ExplanationResponse(BaseModel):
    url: str
    prediction: str
    confidence: float
    features: Dict[str, float]
    top_indicators: List[Dict[str, str]]  # Changed from 'any' to 'str'
    explanation: str


class ModelInfoResponse(BaseModel):
    model_type: str
    best_model: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    training_date: str
    features_count: int
    feature_names: List[str]


class EnhancedPredictor:
    """Enhanced predictor with feature explanation"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_extractor = AdvancedFeatureExtractor()
        self.model_info = {}
        self.load_model()
    
    def load_model(self):
        """Load trained model and metadata"""
        try:
            # Load model
            model_path = Path("models/phishing_model.pkl")
            if not model_path.exists():
                model_path = Path("backend/models/phishing_model.pkl")
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load scaler
            scaler_path = model_path.parent / "scaler.pkl"
            if scaler_path.exists():
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
            
            # Load model info
            info_path = model_path.parent / "model_comparison.json"
            if info_path.exists():
                with open(info_path, 'r') as f:
                    self.model_info = json.load(f)
            
            print(f"✅ Model loaded successfully from {model_path}")
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            raise
    
    def predict(self, url: str) -> Dict:
        """Predict with basic response"""
        try:
            # Extract features
            features = self.feature_extractor.extract_features(url)
            features = features.reshape(1, -1)
            
            
            # Scale if scaler available
            if self.scaler:
                features = self.scaler.transform(features)
            
            # Get prediction - handle both sklearn and LightGBM models
            if hasattr(self.model, 'predict_proba'):
                # Sklearn models (LogisticRegression, RandomForest, LGBMClassifier)
                prediction = self.model.predict(features)[0]
                probability = self.model.predict_proba(features)[0][1]  # Probability of phishing (class 1)
            else:
                # LightGBM Booster - returns probability of legitimate (class 0)
                # Higher value = more legitimate, Lower value = more phishing
                raw_score = float(self.model.predict(features)[0])
                
                # The model outputs probability of being LEGITIMATE
                # So probability of phishing = 1 - raw_score  
                # BUT if raw_score > 0.5, it's legitimate
                probability = 1.0 - raw_score  # Probability of phishing
                prediction = 1 if probability >= 0.5 else 0
            
            # Determine labels
            is_phishing = prediction == 1
            prediction_label = "phishing" if is_phishing else "legitimate"
            confidence = float(probability if is_phishing else 1 - probability)
            
            # Calculate risk level based on phishing probability
            if probability < 0.3:
                risk_level = "low"
            elif probability < 0.7:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            return {
                "url": url,
                "prediction": prediction_label,
                "confidence": round(confidence, 4),
                "probability": round(float(probability), 4),
                "risk_level": risk_level,
                "is_safe": not is_phishing,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                "url": url,
                "prediction": "error",
                "confidence": 0.0,
                "probability": 0.0,
                "risk_level": "unknown",
                "is_safe": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def explain(self, url: str) -> Dict:
        """Predict with detailed feature explanation"""
        try:
            # Get basic prediction
            prediction_result = self.predict(url)
            
            # Extract features as dict
            features_dict = self.feature_extractor.extract_features_dict(url)
            
            # Get feature importance (if available)
            top_indicators = self._get_top_indicators(features_dict, prediction_result['prediction'])
            
            # Generate explanation
            explanation = self._generate_explanation(features_dict, prediction_result)
            
            return {
                "url": url,
                "prediction": prediction_result['prediction'],
                "confidence": prediction_result['confidence'],
                "features": features_dict,
                "top_indicators": top_indicators,
                "explanation": explanation
            }
        
        except Exception as e:
            return {
                "url": url,
                "prediction": "error",
                "confidence": 0.0,
                "features": {},
                "top_indicators": [],
                "explanation": f"Error: {str(e)}"
            }
    
    def _get_top_indicators(self, features: Dict, prediction: str) -> List[Dict]:
        """Get top suspicious/safe indicators"""
        indicators = []
        
        if prediction == "phishing":
            # Phishing indicators
            if features.get('has_ip_address', 0) == 1:
                indicators.append({
                    "feature": "IP Address in URL",
                    "value": "Present",
                    "severity": "high",
                    "description": "URLs with IP addresses are often used in phishing attacks"
                })
            
            if features.get('suspicious_keyword_count', 0) >= 2:
                indicators.append({
                    "feature": "Suspicious Keywords",
                    "value": int(features['suspicious_keyword_count']),
                    "severity": "high",
                    "description": "Multiple suspicious keywords detected (login, verify, secure, etc.)"
                })
            
            if features.get('uses_https', 0) == 0:
                indicators.append({
                    "feature": "No HTTPS",
                    "value": "HTTP only",
                    "severity": "medium",
                    "description": "Legitimate sites typically use HTTPS for security"
                })
            
            if features.get('url_length', 0) > 75:
                indicators.append({
                    "feature": "Long URL",
                    "value": int(features['url_length']),
                    "severity": "medium",
                    "description": "Unusually long URLs are common in phishing attempts"
                })
            
            if features.get('shannon_entropy', 0) > 4.5:
                indicators.append({
                    "feature": "High Entropy",
                    "value": round(features['shannon_entropy'], 2),
                    "severity": "medium",
                    "description": "Random-looking URL structure suggests obfuscation"
                })
        
        else:
            # Legitimate indicators
            if features.get('uses_https', 0) == 1:
                indicators.append({
                    "feature": "HTTPS Enabled",
                    "value": "Secure",
                    "severity": "positive",
                    "description": "Site uses secure HTTPS protocol"
                })
            
            if features.get('tld_category', 0) == 0:
                indicators.append({
                    "feature": "Trusted TLD",
                    "value": "Verified",
                    "severity": "positive",
                    "description": "Uses trusted top-level domain (.com, .org, .net)"
                })
            
            if features.get('suspicious_keyword_count', 0) == 0:
                indicators.append({
                    "feature": "No Suspicious Keywords",
                    "value": "Clean",
                    "severity": "positive",
                    "description": "URL does not contain common phishing keywords"
                })
        
        return indicators[:5]  # Return top 5
    
    def _generate_explanation(self, features: Dict, prediction_result: Dict) -> str:
        """Generate human-readable explanation"""
        prediction = prediction_result['prediction']
        confidence = prediction_result['confidence']
        
        if prediction == "phishing":
            explanation = f"This URL is classified as PHISHING with {confidence*100:.1f}% confidence. "
            explanation += "Suspicious indicators include: "
            
            reasons = []
            if features.get('has_ip_address', 0) == 1:
                reasons.append("IP address in URL")
            if features.get('suspicious_keyword_count', 0) >= 2:
                reasons.append(f"{int(features['suspicious_keyword_count'])} suspicious keywords")
            if features.get('uses_https', 0) == 0:
                reasons.append("no HTTPS encryption")
            if features.get('num_hyphens', 0) >= 3:
                reasons.append("excessive hyphens")
            
            explanation += ", ".join(reasons) + "."
        
        else:
            explanation = f"This URL appears LEGITIMATE with {confidence*100:.1f}% confidence. "
            explanation += "Positive indicators include: "
            
            reasons = []
            if features.get('uses_https', 0) == 1:
                reasons.append("HTTPS encryption")
            if features.get('tld_category', 0) == 0:
                reasons.append("trusted domain")
            if features.get('suspicious_keyword_count', 0) == 0:
                reasons.append("no suspicious keywords")
            
            explanation += ", ".join(reasons) + "."
        
        return explanation


# Initialize predictor
predictor = EnhancedPredictor()


@app.get("/")
async def root():
    """API information"""
    return {
        "name": "Phishing URL Detection API",
        "version": "2.0.0",
        "description": "Research-aligned early detection of phishing URLs",
        "endpoints": {
            "/predict": "POST - Predict if URL is phishing",
            "/explain": "POST - Get detailed feature explanation",
            "/model-info": "GET - Get model metadata",
            "/health": "GET - API health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is operational",
        "version": "2.0.0",
        "model_loaded": predictor.model is not None
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_url(request: URLRequest):
    """
    Predict if URL is phishing or legitimate
    
    Returns:
    - prediction: "phishing" or "legitimate"
    - confidence: 0.0 to 1.0
    - risk_level: "low", "medium", or "high"
    """
    result = predictor.predict(request.url)
    
    if result.get('prediction') == 'error':
        raise HTTPException(status_code=500, detail=result.get('error', 'Prediction failed'))
    
    return result


@app.post("/explain", response_model=ExplanationResponse)
async def explain_prediction(request: URLRequest):
    """
    Get detailed explanation of prediction with feature breakdown
    
    Returns:
    - All features extracted
    - Top suspicious/safe indicators
    - Human-readable explanation
    """
    result = predictor.explain(request.url)
    
    if result.get('prediction') == 'error':
        raise HTTPException(status_code=500, detail=result.get('explanation', 'Explanation failed'))
    
    return result


@app.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get model metadata and performance metrics"""
    if not predictor.model_info:
        return {
            "model_type": "LightGBM",
            "best_model": "Unknown",
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "roc_auc": 0.0,
            "training_date": "Unknown",
            "features_count": 20,
            "feature_names": predictor.feature_extractor.get_feature_names()
        }
    
    best_model = predictor.model_info.get('best_model', 'Unknown')
    results = predictor.model_info.get('results', {}).get(best_model, {})
    
    return {
        "model_type": "Ensemble Classifier",
        "best_model": best_model,
        "accuracy": results.get('accuracy', 0.0),
        "precision": results.get('precision', 0.0),
        "recall": results.get('recall', 0.0),
        "f1_score": results.get('f1_score', 0.0),
        "roc_auc": results.get('roc_auc', 0.0),
        "training_date": predictor.model_info.get('training_date', 'Unknown'),
        "features_count": 20,
        "feature_names": predictor.feature_extractor.get_feature_names()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
