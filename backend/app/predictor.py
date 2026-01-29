"""
ML Model Predictor
Loads trained model and makes predictions
"""

import pickle
import numpy as np
from pathlib import Path
from .features import URLFeatureExtractor


class PhishingPredictor:
    """Phishing URL predictor using trained LightGBM model"""
    
    def __init__(self, model_path=None):
        """
        Initialize predictor with trained model
        
        Args:
            model_path (str): Path to pickled model file
        """
        # Try multiple possible paths
        if model_path is None:
            possible_paths = [
                "models/phishing_model.pkl",  # When running from backend/
                "backend/models/phishing_model.pkl",  # When running from project root
                Path(__file__).parent.parent / "models" / "phishing_model.pkl"  # Absolute path
            ]
            for path in possible_paths:
                if Path(path).exists():
                    model_path = str(path)
                    break
        
        self.model_path = model_path
        self.model = None
        self.feature_extractor = URLFeatureExtractor()
        self.load_model()
    
    def load_model(self):
        """Load the trained model from disk"""
        try:
            model_file = Path(self.model_path)
            if not model_file.exists():
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            print(f"✅ Model loaded successfully from {self.model_path}")
        
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            raise
    
    def predict(self, url: str) -> dict:
        """
        Predict if a URL is phishing or legitimate
        
        Args:
            url (str): URL to analyze
            
        Returns:
            dict: Prediction result with label, confidence, and risk level
        """
        try:
            # Validate URL
            if not url or not isinstance(url, str):
                raise ValueError("Invalid URL provided")
            
            # Extract features
            features = self.feature_extractor.extract_features(url)
            features = features.reshape(1, -1)
            
            # Get ML model prediction probability
            ml_probability = self.model.predict(features)[0]
            
            # Apply rule-based heuristics for better accuracy
            heuristic_score = self._apply_heuristics(url)
            
            # Combine ML and heuristics (weighted average)
            # 60% ML, 40% heuristics
            probability = 0.6 * ml_probability + 0.4 * heuristic_score
            
            # Determine prediction (1 = phishing, 0 = legitimate)
            is_phishing = probability > 0.5
            prediction_label = "phishing" if is_phishing else "legitimate"
            
            # Calculate confidence (distance from decision boundary)
            confidence = float(probability if is_phishing else 1 - probability)
            
            # Determine risk level
            risk_level = self._get_risk_level(probability)
            
            return {
                "url": url,
                "prediction": prediction_label,
                "confidence": round(confidence, 4),
                "probability": round(float(probability), 4),
                "risk_level": risk_level,
                "is_safe": not is_phishing
            }
        
        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "prediction": "error",
                "confidence": 0.0
            }
    
    def _apply_heuristics(self, url: str) -> float:
        """
        Apply rule-based heuristics to detect phishing
        Returns a score between 0 (legitimate) and 1 (phishing)
        """
        import re
        from urllib.parse import urlparse
        
        score = 0.0
        url_lower = url.lower()
        
        # Suspicious keywords in domain
        phishing_keywords = [
            'verify', 'account', 'update', 'secure', 'login', 'signin',
            'banking', 'confirm', 'suspended', 'locked', 'unusual',
            'activity', 'alert', 'security', 'notification'
        ]
        
        # Check for multiple suspicious keywords
        keyword_count = sum(1 for keyword in phishing_keywords if keyword in url_lower)
        if keyword_count >= 3:
            score += 0.4
        elif keyword_count >= 2:
            score += 0.25
        elif keyword_count >= 1:
            score += 0.1
        
        # Check for IP address in URL
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            score += 0.5
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
        if any(url_lower.endswith(tld) for tld in suspicious_tlds):
            score += 0.3
        
        # Check for @ symbol (often used in phishing)
        if '@' in url:
            score += 0.4
        
        # Check for excessive hyphens in domain
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.count('-') >= 3:
            score += 0.3
        elif domain.count('-') >= 2:
            score += 0.2
        
        # Check for subdomain impersonation (e.g., paypal.com.fake-site.com)
        legitimate_domains = [
            'google.com', 'facebook.com', 'amazon.com', 'paypal.com',
            'microsoft.com', 'apple.com', 'netflix.com', 'instagram.com',
            'twitter.com', 'linkedin.com', 'github.com', 'bankofamerica.com',
            'chase.com', 'wellsfargo.com', 'citibank.com'
        ]
        
        for legit_domain in legitimate_domains:
            if legit_domain in url_lower and not domain.endswith(legit_domain):
                score += 0.6  # High score for impersonation
                break
        
        # Check for very long URLs (often phishing)
        if len(url) > 100:
            score += 0.2
        
        # Check for no HTTPS (not always phishing, but suspicious for login pages)
        if not url.startswith('https://') and any(keyword in url_lower for keyword in ['login', 'signin', 'account', 'secure']):
            score += 0.2
        
        # Cap the score at 1.0
        return min(score, 1.0)
    
    def _get_risk_level(self, probability: float) -> str:
        """
        Determine risk level based on probability
        
        Args:
            probability (float): Phishing probability (0-1)
            
        Returns:
            str: Risk level (low, medium, high)
        """
        if probability < 0.3:
            return "low"
        elif probability < 0.7:
            return "medium"
        else:
            return "high"
    
    def predict_batch(self, urls: list) -> list:
        """
        Predict multiple URLs at once
        
        Args:
            urls (list): List of URLs
            
        Returns:
            list: List of prediction results
        """
        return [self.predict(url) for url in urls]


# Singleton instance
_predictor_instance = None


def get_predictor() -> PhishingPredictor:
    """
    Get or create predictor instance (singleton pattern)
    
    Returns:
        PhishingPredictor: Predictor instance
    """
    global _predictor_instance
    
    if _predictor_instance is None:
        _predictor_instance = PhishingPredictor()
    
    return _predictor_instance
