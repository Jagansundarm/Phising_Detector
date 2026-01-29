"""
Test the retrained model accuracy
"""
import pickle
import numpy as np
from backend.app.advanced_feature_extractor import AdvancedFeatureExtractor

model = pickle.load(open('backend/models/phishing_model.pkl', 'rb'))
scaler = pickle.load(open('backend/models/scaler.pkl', 'rb'))
fe = AdvancedFeatureExtractor()

print(f'Model type: {type(model).__name__}')
print(f'Has predict_proba: {hasattr(model, "predict_proba")}')
print()

test_urls = [
    ('https://www.google.com', 'legitimate'),
    ('https://www.facebook.com', 'legitimate'),
    ('https://www.amazon.com', 'legitimate'),
    ('https://www.paypal.com', 'legitimate'),
    ('https://www.github.com', 'legitimate'),
    ('http://paypal-verify.fake.com', 'phishing'),
    ('http://google-security.tk/signin', 'phishing'),
    ('http://faceboook.com/login', 'phishing'),
    ('http://paypal-secure.login-verification.com/signin', 'phishing'),
    ('http://paypa1.com/verify', 'phishing'),
    ('http://amazon.com-account-verification.net/update', 'phishing'),
]

correct = 0
total = len(test_urls)

print('URL                                      | Expected   | Prediction | Phishing%')
print('-' * 85)

for url, expected in test_urls:
    features = fe.extract_features(url).reshape(1, -1)
    features_scaled = scaler.transform(features)
    proba = model.predict_proba(features_scaled)[0]
    phishing_prob = proba[1]  # Probability of class 1 (phishing)
    pred = 'phishing' if phishing_prob >= 0.5 else 'legitimate'
    status = '✓' if pred == expected else '✗'
    if pred == expected:
        correct += 1
    print(f'{status} {url[:40]:40} | {expected:10} | {pred:10} | {phishing_prob*100:.1f}%')

print(f'\nAccuracy: {correct}/{total} ({correct/total*100:.0f}%)')
