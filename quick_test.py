import pickle
from backend.app.advanced_feature_extractor import AdvancedFeatureExtractor

model = pickle.load(open('backend/models/phishing_model.pkl', 'rb'))
scaler = pickle.load(open('backend/models/scaler.pkl', 'rb'))
fe = AdvancedFeatureExtractor()

yahoo_url = "https://search.yahoo.com/search?d=%7b%22dn%22%3a%22yk%22%2c%22subdn%22%3a%22publiccompany%22%2c%22ykid%22%3a%220d14d6b9-779c-4435-a2f1-70077358e09e%22%7d&fr2=p%3ads%2cv%3aomn%2cm%3asa%2cbrws%3achrome%2cpos%3a1%2csa_mk%3a30&mkr=30&fr=mcafee&type=E210US885G0&p=Lovable"

f = fe.extract_features(yahoo_url).reshape(1,-1)
f_scaled = scaler.transform(f)
p = model.predict_proba(f_scaled)[0]
print(f"Yahoo URL Phishing Prob: {p[1]*100:.1f}%")
print(f"Prediction: {'PHISHING' if p[1] >= 0.5 else 'LEGITIMATE'}")
