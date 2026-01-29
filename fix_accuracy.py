"""
Add more legitimate URLs with complex query strings to improve accuracy
Then retrain the model
"""
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import lightgbm as lgb

from backend.app.advanced_feature_extractor import AdvancedFeatureExtractor

# Load existing dataset
df = pd.read_csv('ml_engine/data/phishing_dataset.csv')
print(f"Original dataset: {len(df)} URLs")

# Add more legitimate URLs with COMPLEX query strings (search engines, trackers, etc.)
new_legitimate_urls = [
    # Search engine URLs with query params
    "https://search.yahoo.com/search?p=test+query&fr=mcafee&type=E210US885G0",
    "https://search.yahoo.com/search?d=%7b%22dn%22%3a%22yk%22%7d&fr=mcafee&p=search",
    "https://www.google.com/search?q=python+programming&oq=python&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECAAQQzIECAAQQzIECAAQQ",
    "https://www.google.com/search?q=weather&source=hp&ei=abc123&iflsig=ALs-wAMAAAAAY",
    "https://www.bing.com/search?q=machine+learning&form=QBLH&sp=-1&pq=machine+learning",
    "https://duckduckgo.com/?q=privacy+search&t=h_&ia=web",
    
    # E-commerce with tracking/session params
    "https://www.amazon.com/dp/B08N5WRWNW?ref=cm_sw_r_cp_api_i_dl_ABC123&encoding=UTF8&psc=1",
    "https://www.amazon.com/gp/product/B07XJ8C8F5?pf_rd_r=ABC123&pf_rd_p=DEF456&pd_rd_r=ghij",
    "https://www.ebay.com/itm/123456789?hash=item1234567890%3Ag%3AABCDEfg&var=654321",
    "https://www.walmart.com/ip/Product-Name/123456789?selected=true&irgwc=1&sourceid=imp_123",
    "https://www.target.com/p/product-name/-/A-12345678?preselect=12345#lnk=sametab",
    "https://www.bestbuy.com/site/product/1234567.p?skuId=1234567&ref=212&loc=1",
    
    # Social media with tracking
    "https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fexample.com&quote=Hello",
    "https://twitter.com/intent/tweet?text=Check%20this%20out&url=https%3A%2F%2Fexample.com",
    "https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fexample.com&title=Title",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf&index=2",
    "https://www.instagram.com/p/ABC123DEF/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA",
    
    # Analytics and tracking URLs
    "https://analytics.google.com/analytics/web/?authuser=0#/report-home/a12345w67890p123456",
    "https://www.googleadservices.com/pagead/aclk?sa=L&ai=ABC123&num=1&cid=ABC&sig=AOD64_0",
    "https://ad.doubleclick.net/ddm/trackclk/N123/B456/C789?dc_trk_aid=123&dc_trk_cid=456",
    
    # OAuth and authentication redirects
    "https://accounts.google.com/o/oauth2/v2/auth?client_id=123.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fexample.com&response_type=code&scope=email",
    "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=abc&response_type=code&redirect_uri=https%3A%2F%2Fexample.com",
    "https://github.com/login/oauth/authorize?client_id=abc123&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&scope=user%3Aemail",
    
    # News and media with tracking
    "https://www.nytimes.com/2024/01/15/technology/article.html?smid=tw-nytimes&smtyp=cur",
    "https://www.bbc.com/news/world-us-canada-12345678?xtor=AL-72-%5Bpartner%5D-%5Bbbc.news%5D&at_medium=custom7",
    "https://www.cnn.com/2024/01/15/tech/article/index.html?utm_source=twCNN&utm_medium=social&utm_term=link",
    
    # Cloud services
    "https://console.aws.amazon.com/console/home?region=us-east-1#resource-groups:settings",
    "https://portal.azure.com/#blade/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade/overview",
    "https://console.cloud.google.com/storage/browser?project=my-project-123456&prefix=&forceOnObjectsSortingFiltering=false",
    
    # Banking and finance (legitimate)
    "https://www.chase.com/digital/login?fromOrigin=https%3A%2F%2Fwww.chase.com&lang=en",
    "https://www.wellsfargo.com/biz/loans/sba-loans/?gclid=CjAwKCAiA75aBR&gclsrc=aw.ds",
    "https://www.paypal.com/webapps/mpp/paypal-safety-and-security?locale.x=en_US",
    
    # More Yahoo URLs
    "https://search.yahoo.com/search?p=how+to+code&fr=yfp-hrmob&fr2=p%3Afp%2Cm%3Asb&.tsrc=yfp-hrmob",
    "https://search.yahoo.com/search?d=%7B%22id%22%3A%22123%22%7D&p=test&fr=mcafee",
    "https://mail.yahoo.com/d/folders/1?.intl=us&.lang=en-US&.partner=none&.src=fp",
    "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch",
    
    # More Google complex URLs  
    "https://www.google.com/maps/place/New+York/@40.7127753,-74.0059728,11z/data=!3m1!4b1!4m6!3m5!1s0x89c24fa5d33f083b",
    "https://calendar.google.com/calendar/u/0/r?pli=1&sf=true",
    "https://docs.google.com/document/d/1abc123DEF456ghiJKL789/edit?usp=sharing&ouid=123&rtpof=true&sd=true",
    "https://drive.google.com/file/d/1ABC123def456GHI/view?usp=sharing&resourcekey=0-abc123",
]

# Create new rows
new_rows = pd.DataFrame({'url': new_legitimate_urls, 'label': 0})
df = pd.concat([df, new_rows], ignore_index=True)
print(f"After adding complex legitimate URLs: {len(df)} URLs")
print(f"  Phishing: {sum(df.label==1)}")
print(f"  Legitimate: {sum(df.label==0)}")

# Save updated dataset
df.to_csv('ml_engine/data/phishing_dataset.csv', index=False)
print("Updated dataset saved!")

# Now retrain the model
print("\n" + "="*60)
print("RETRAINING MODEL")
print("="*60)

fe = AdvancedFeatureExtractor()
X = np.array([fe.extract_features(url) for url in df['url']])
y = df['label'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train with adjusted hyperparameters for better generalization
model = lgb.LGBMClassifier(
    n_estimators=150,
    random_state=42,
    class_weight='balanced',
    max_depth=5,  # Reduced to prevent overfitting
    learning_rate=0.05,  # Lower learning rate
    min_child_samples=5,  # Prevent overfitting on small samples
    reg_alpha=0.1,  # L1 regularization
    reg_lambda=0.1,  # L2 regularization
    verbose=-1
)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

print(f"\nModel Performance:")
print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"  Precision: {precision_score(y_test, y_pred):.4f}")
print(f"  Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"  F1-Score:  {f1_score(y_test, y_pred):.4f}")
print(f"  ROC-AUC:   {roc_auc_score(y_test, y_proba):.4f}")

# Save model
with open('backend/models/phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('backend/models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save model info
info = {
    'best_model': 'LightGBM',
    'results': {
        'LightGBM': {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred)),
            'recall': float(recall_score(y_test, y_pred)),
            'f1_score': float(f1_score(y_test, y_pred)),
            'roc_auc': float(roc_auc_score(y_test, y_proba))
        }
    },
    'training_date': datetime.now().isoformat(),
    'dataset_size': len(df)
}
with open('backend/models/model_comparison.json', 'w') as f:
    json.dump(info, f, indent=2)

print("\nModel saved!")

# Test with problematic URLs
print("\n" + "="*60)
print("TESTING WITH PREVIOUSLY PROBLEMATIC URLS")
print("="*60)

test_urls = [
    ("https://www.google.com", "Simple legitimate"),
    ("https://search.yahoo.com/search?d=%7b%22dn%22%3a%22yk%22%2c%22subdn%22%3a%22publiccompany%22%2c%22ykid%22%3a%220d14d6b9-779c-4435-a2f1-70077358e09e%22%7d&fr2=p%3ads%2cv%3aomn%2cm%3asa%2cbrws%3achrome%2cpos%3a1%2csa_mk%3a30&mkr=30&fr=mcafee&type=E210US885G0&p=Lovable", "Yahoo Search (COMPLEX)"),
    ("https://www.amazon.com/dp/B08N5WRWNW?ref=cm_sw_r_cp_api", "Amazon with params"),
    ("http://paypal-verify.fake.com/login", "Phishing"),
    ("http://google-security.tk/signin", "Phishing"),
]

for url, desc in test_urls:
    f = fe.extract_features(url).reshape(1, -1)
    f_scaled = scaler.transform(f)
    p = model.predict_proba(f_scaled)[0][1]
    result = "PHISHING" if p >= 0.5 else "LEGIT"
    status = "OK" if (result == "LEGIT" and "Phishing" not in desc) or (result == "PHISHING" and "Phishing" in desc) else "FAIL"
    print(f"  [{status}] {result:8} ({p*100:5.1f}%) - {desc[:40]}")
