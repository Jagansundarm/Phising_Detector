"""
Quick test to check model predictions
"""

import sys
sys.path.append('backend')

from app.predictor import PhishingPredictor

predictor = PhishingPredictor()

test_urls = [
    ("https://www.google.com", "legitimate"),
    ("https://www.github.com", "legitimate"),
    ("http://paypal-secure.login-verification.com/signin", "phishing"),
    ("http://secure.bankofamerica.verify.update-account.net", "phishing"),
    ("http://192.168.1.1/login.php", "phishing"),
]

print("=" * 70)
print("MODEL PREDICTION TEST")
print("=" * 70)

for url, expected in test_urls:
    result = predictor.predict(url)
    status = "✅" if result['prediction'] == expected else "❌"
    print(f"\n{status} URL: {url}")
    print(f"   Expected: {expected}")
    print(f"   Predicted: {result['prediction']}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Probability: {result['probability']:.4f}")
    print(f"   Risk Level: {result['risk_level']}")

print("\n" + "=" * 70)
