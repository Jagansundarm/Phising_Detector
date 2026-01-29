import pickle
import numpy as np
from backend.app.advanced_feature_extractor import AdvancedFeatureExtractor

model = pickle.load(open('backend/models/phishing_model.pkl', 'rb'))
scaler = pickle.load(open('backend/models/scaler.pkl', 'rb'))
fe = AdvancedFeatureExtractor()

# Full Yahoo URL
yahoo_url = "https://search.yahoo.com/search?d=%7b%22dn%22%3a%22yk%22%2c%22subdn%22%3a%22publiccompany%22%2c%22ykid%22%3a%220d14d6b9-779c-4435-a2f1-70077358e09e%22%7d&fr2=p%3ads%2cv%3aomn%2cm%3asa%2cbrws%3achrome%2cpos%3a1%2csa_mk%3a30&mkr=30&fr=mcafee&type=E210US885G0&p=Lovable"

features = fe.extract_features_dict(yahoo_url)
print("KEY FEATURES FOR YAHOO URL:")
print("-" * 40)
for k, v in features.items():
    if isinstance(v, float):
        print(f"  {k}: {v:.2f}")
    else:
        print(f"  {k}: {v}")

f = fe.extract_features(yahoo_url).reshape(1,-1)
p = model.predict_proba(scaler.transform(f))[0][1]
print(f"\nPHISHING PROBABILITY: {p*100:.1f}%")
print(f"PREDICTION: {'PHISHING' if p >= 0.5 else 'LEGITIMATE'}")

# Root cause
print("\nROOT CAUSE:")
if features['url_length'] > 100:
    print(f"  - URL is very long: {int(features['url_length'])} chars")
if features['query_length'] > 50:
    print(f"  - Query string is long: {int(features['query_length'])} chars")  
if features['shannon_entropy'] > 4.0:
    print(f"  - High entropy: {features['shannon_entropy']:.2f}")
if features['num_digits'] > 15:
    print(f"  - Many digits: {int(features['num_digits'])}")
