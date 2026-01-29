import pickle
from backend.app.advanced_feature_extractor import AdvancedFeatureExtractor

model = pickle.load(open('backend/models/phishing_model.pkl', 'rb'))
scaler = pickle.load(open('backend/models/scaler.pkl', 'rb'))
fe = AdvancedFeatureExtractor()

tests = [
    # Legitimate URLs
    ("https://www.google.com", "legitimate"),
    ("https://www.facebook.com", "legitimate"),
    ("https://www.amazon.com", "legitimate"),
    ("https://www.yahoo.com", "legitimate"),
    ("https://search.yahoo.com/search?d=%7b%22dn%22%3a%22yk%22%2c%22subdn%22%3a%22publiccompany%22%2c%22ykid%22%3a%220d14d6b9-779c-4435-a2f1-70077358e09e%22%7d&fr2=p%3ads%2cv%3aomn%2cm%3asa%2cbrws%3achrome%2cpos%3a1%2csa_mk%3a30&mkr=30&fr=mcafee&type=E210US885G0&p=Lovable", "legitimate"),
    ("https://www.google.com/search?q=test&oq=test&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECAAQQzIE", "legitimate"),
    ("https://www.amazon.com/dp/B08N5WRWNW?ref=cm_sw_r_cp_api_i_dl_ABC123", "legitimate"),
    
    # Phishing URLs
    ("http://paypal-verify.fake.com", "phishing"),
    ("http://google-security.tk/signin", "phishing"),
    ("http://faceboook.com/login", "phishing"),
    ("http://paypal-secure.login-verification.com/signin", "phishing"),
    ("http://amazon.com-account-verification.net/update", "phishing"),
]

print("="*70)
print("MODEL ACCURACY TEST")
print("="*70)
correct = 0
total = len(tests)

for url, expected in tests:
    f = fe.extract_features(url).reshape(1,-1)
    p = model.predict_proba(scaler.transform(f))[0][1]
    pred = "phishing" if p >= 0.5 else "legitimate"
    status = "PASS" if pred == expected else "FAIL"
    if pred == expected:
        correct += 1
    print(f"[{status}] {pred:10} ({p*100:5.1f}%) - {url[:50]}...")

print("="*70)
print(f"ACCURACY: {correct}/{total} ({correct/total*100:.0f}%)")
print("="*70)
