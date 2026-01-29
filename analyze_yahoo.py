"""
Analyze why Yahoo search URL is being flagged as phishing
"""
import pickle
import numpy as np
from backend.app.advanced_feature_extractor import AdvancedFeatureExtractor

model = pickle.load(open('backend/models/phishing_model.pkl', 'rb'))
scaler = pickle.load(open('backend/models/scaler.pkl', 'rb'))
fe = AdvancedFeatureExtractor()

# The problematic URL
yahoo_url = "https://search.yahoo.com/search?d=%7b%22dn%22%3a%22yk%22%2c%22subdn%22%3a%22publiccompany%22%2c%22ykid%22%3a%220d14d6b9-779c-4435-a2f1-70077358e09e%22%7d&fr2=p%3ads%2cv%3aomn%2cm%3asa%2cbrws%3achrome%2cpos%3a1%2csa_mk%3a30&mkr=30&fr=mcafee&type=E210US885G0&p=Lovable"

print("="*80)
print("ANALYZING YAHOO SEARCH URL")
print("="*80)
print(f"\nURL: {yahoo_url[:80]}...")
print(f"URL Length: {len(yahoo_url)} characters")

# Extract features
features = fe.extract_features(yahoo_url)
features_dict = fe.extract_features_dict(yahoo_url)

print("\n" + "="*80)
print("FEATURE BREAKDOWN")
print("="*80)

feature_names = fe.get_feature_names()
for name, value in zip(feature_names, features):
    flag = ""
    # Highlight suspicious features
    if name == 'url_length' and value > 75:
        flag = " ⚠️ LONG URL"
    elif name == 'suspicious_keyword_count' and value >= 2:
        flag = " ⚠️ SUSPICIOUS KEYWORDS"
    elif name == 'uses_https' and value == 0:
        flag = " ⚠️ NO HTTPS"
    elif name == 'shannon_entropy' and value > 4.5:
        flag = " ⚠️ HIGH ENTROPY"
    elif name == 'query_length' and value > 100:
        flag = " ⚠️ LONG QUERY"
    elif name == 'num_digits' and value > 10:
        flag = " ⚠️ MANY DIGITS"
    
    print(f"  {name:30} = {value:10.2f}{flag}")

# Scale and predict
features_scaled = scaler.transform(features.reshape(1, -1))
proba = model.predict_proba(features_scaled)[0]
phishing_prob = proba[1]
prediction = 'PHISHING' if phishing_prob >= 0.5 else 'LEGITIMATE'

print("\n" + "="*80)
print("PREDICTION RESULT")
print("="*80)
print(f"  Prediction: {prediction}")
print(f"  Phishing Probability: {phishing_prob*100:.2f}%")
print(f"  Legitimate Probability: {proba[0]*100:.2f}%")

print("\n" + "="*80)
print("ROOT CAUSE ANALYSIS")
print("="*80)

# Identify why it's being flagged
reasons = []
if features_dict['url_length'] > 75:
    reasons.append(f"URL is very long ({int(features_dict['url_length'])} chars)")
if features_dict['shannon_entropy'] > 4.0:
    reasons.append(f"High entropy ({features_dict['shannon_entropy']:.2f}) - URL looks random")
if features_dict['query_length'] > 100:
    reasons.append(f"Very long query string ({int(features_dict['query_length'])} chars)")
if features_dict['num_digits'] > 10:
    reasons.append(f"Many digits in URL ({int(features_dict['num_digits'])})")
if features_dict['special_char_ratio'] > 0.2:
    reasons.append(f"High special character ratio ({features_dict['special_char_ratio']:.2f})")

print("Potential false positive triggers:")
for r in reasons:
    print(f"  - {r}")

# Compare with known legitimate URLs
print("\n" + "="*80)
print("COMPARISON WITH OTHER URLS")
print("="*80)

test_urls = [
    ("https://www.google.com", "Known Legitimate"),
    ("https://www.yahoo.com", "Known Legitimate"),
    ("https://search.yahoo.com/search?p=test", "Yahoo Search (simple)"),
    (yahoo_url, "Yahoo Search (complex)"),
    ("http://paypal-verify.fake.com", "Known Phishing"),
]

for url, desc in test_urls:
    f = fe.extract_features(url).reshape(1, -1)
    f_scaled = scaler.transform(f)
    p = model.predict_proba(f_scaled)[0][1]
    result = "PHISHING" if p >= 0.5 else "LEGITIMATE"
    print(f"  {result:10} ({p*100:5.1f}%) - {desc}")
