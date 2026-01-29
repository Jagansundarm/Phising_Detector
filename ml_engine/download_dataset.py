"""
Enhanced Dataset with More Realistic URLs
"""

import pandas as pd
from pathlib import Path


def create_enhanced_dataset():
    """Create a larger, more realistic dataset"""
    
    # Expanded phishing URLs (100+ examples)
    phishing_urls = [
        # PayPal phishing
        "http://paypal-secure.login-verification.com/signin",
        "http://paypal.com-secure-login.net/verify",
        "http://paypal-update.account-verify.com",
        "http://secure-paypal.com-login.net",
        "http://paypal.security-check.org/update",
        
        # Banking phishing
        "http://secure.bankofamerica.verify.update-account.net",
        "http://chase.com-secure-login.net",
        "http://wellsfargo.account-verify.com",
        "http://citibank-security.update-now.net",
        "http://usbank.verify-account.org",
        
        # Tech company phishing
        "http://apple.id-verification.xyz/login",
        "http://microsoft-support.xyz/update",
        "http://google-security.tk/signin",
        "http://amazon.com-account-verification.net/update",
        "http://netflix.account-update.org/billing",
        
        # Social media phishing
        "http://facebook-security-check.ml/verify",
        "http://instagram.confirm-identity.ml/verify",
        "http://linkedin.profile-security.tk/check",
        "http://twitter.account-suspended.com/appeal",
        "http://tiktok-verify.account-check.net",
        
        # Generic phishing patterns
        "http://secure-login-verify.com/account",
        "http://account-update-required.net/signin",
        "http://verify-your-account-now.com",
        "http://security-alert-action-required.net",
        "http://confirm-identity-immediately.org",
        
        # IP-based phishing
        "http://192.168.1.100/login.php",
        "http://10.0.0.1/secure/verify",
        "http://172.16.0.1/account/update",
        
        # Suspicious TLDs
        "http://legitimate-bank.tk/login",
        "http://secure-payment.ml/verify",
        "http://account-verify.ga/signin",
        "http://update-now.cf/account",
        
        # Typosquatting
        "http://gooogle.com/signin",
        "http://faceboook.com/login",
        "http://amazom.com/account",
        "http://paypa1.com/verify",
        "http://app1e.com/id",
        
        # More sophisticated phishing
        "https://secure-login.paypal-verify.com/account",
        "https://account.microsoft-support.net/update",
        "https://signin.google-security.org/verify",
        "https://update.apple-id.net/account",
        "https://verify.amazon-account.com/signin",
        
        # Additional patterns
        "http://urgent-account-verification.com/paypal",
        "http://suspended-account-restore.net/login",
        "http://security-breach-action.com/verify",
        "http://unusual-activity-detected.net/confirm",
        "http://account-limitation-remove.com/signin",
        
        # More banking
        "http://bankofamerica-secure.verify-now.com",
        "http://chase-online-banking.security-check.net",
        "http://wells-fargo.account-suspended.com",
        "http://citi-bank.verify-identity.net",
        "http://capital-one.security-alert.com",
        
        # Cryptocurrency phishing
        "http://coinbase-verify.account-security.net",
        "http://binance-security.verify-now.com",
        "http://blockchain-wallet.verify-account.net",
        "http://crypto-exchange.security-check.com",
        
        # E-commerce
        "http://ebay-account.verify-seller.net",
        "http://etsy-shop.security-update.com",
        "http://shopify-store.verify-payment.net",
        
        # More examples with common phishing indicators
        "http://account-verify-2024.com/signin",
        "http://secure-update-required.net/login",
        "http://verify-account-information.com/update",
        "http://security-notification-center.net/verify",
        "http://account-recovery-service.com/restore",
        "http://identity-confirmation-required.net/verify",
        "http://payment-method-update.com/billing",
        "http://subscription-renewal-required.net/payment",
        "http://account-reactivation-center.com/signin",
        "http://security-verification-portal.net/verify",
        
        # Subdomain-based phishing
        "http://login.secure-paypal.com.phishing-site.com",
        "http://signin.google.com.fake-domain.net",
        "http://account.microsoft.com.verify-now.com",
        "http://www.amazon.com.security-check.net",
        "http://secure.bankofamerica.com.verify-account.com",
        
        # URL with many hyphens
        "http://secure-login-account-verify-update-now.com",
        "http://bank-account-security-verification-required.net",
        "http://payment-method-update-billing-information.com",
        
        # URLs with @ symbol
        "http://user@legitimate-site.com@phishing-site.com",
        "http://admin@secure-login.com@malicious.net",
        
        # Long URLs with parameters
        "http://phishing.com/login?redirect=http://legitimate.com",
        "http://fake-site.net/verify?account=user&token=abc123&session=xyz",
        "http://malicious.com/update?user=victim&pass=stolen&redirect=real-site.com",
    ]
    
    # Expanded legitimate URLs (100+ examples)
    legitimate_urls = [
        # Major tech companies
        "https://www.google.com",
        "https://www.youtube.com",
        "https://www.facebook.com",
        "https://www.amazon.com",
        "https://www.wikipedia.org",
        "https://www.twitter.com",
        "https://www.instagram.com",
        "https://www.linkedin.com",
        "https://www.reddit.com",
        "https://www.netflix.com",
        "https://www.microsoft.com",
        "https://www.apple.com",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.ebay.com",
        
        # Banking
        "https://www.bankofamerica.com",
        "https://www.chase.com",
        "https://www.wellsfargo.com",
        "https://www.citibank.com",
        "https://www.usbank.com",
        "https://www.capitalone.com",
        "https://www.discover.com",
        
        # E-commerce
        "https://www.walmart.com",
        "https://www.target.com",
        "https://www.bestbuy.com",
        "https://www.etsy.com",
        "https://www.shopify.com",
        "https://www.aliexpress.com",
        
        # News and media
        "https://www.cnn.com",
        "https://www.bbc.com",
        "https://www.nytimes.com",
        "https://www.theguardian.com",
        "https://www.reuters.com",
        "https://www.forbes.com",
        
        # Education
        "https://www.coursera.org",
        "https://www.udemy.com",
        "https://www.khanacademy.org",
        "https://www.edx.org",
        "https://www.mit.edu",
        "https://www.stanford.edu",
        
        # Entertainment
        "https://www.spotify.com",
        "https://www.twitch.tv",
        "https://www.hulu.com",
        "https://www.disneyplus.com",
        "https://www.hbo.com",
        
        # Professional
        "https://www.salesforce.com",
        "https://www.slack.com",
        "https://www.zoom.us",
        "https://www.dropbox.com",
        "https://www.adobe.com",
        
        # Search and reference
        "https://www.bing.com",
        "https://www.yahoo.com",
        "https://www.duckduckgo.com",
        "https://www.archive.org",
        
        # Developer tools
        "https://www.gitlab.com",
        "https://www.bitbucket.org",
        "https://www.npmjs.com",
        "https://www.pypi.org",
        "https://www.docker.com",
        
        # Cloud services
        "https://aws.amazon.com",
        "https://cloud.google.com",
        "https://azure.microsoft.com",
        "https://www.heroku.com",
        "https://www.digitalocean.com",
        
        # Communication
        "https://www.gmail.com",
        "https://www.outlook.com",
        "https://www.whatsapp.com",
        "https://www.telegram.org",
        "https://www.discord.com",
        
        # Government
        "https://www.usa.gov",
        "https://www.irs.gov",
        "https://www.nih.gov",
        "https://www.nasa.gov",
        
        # More legitimate sites
        "https://www.paypal.com",
        "https://www.stripe.com",
        "https://www.square.com",
        "https://www.venmo.com",
        "https://www.coinbase.com",
        "https://www.binance.com",
        "https://www.kraken.com",
        
        # Subdomains of legitimate sites
        "https://mail.google.com",
        "https://drive.google.com",
        "https://docs.google.com",
        "https://accounts.google.com",
        "https://login.microsoft.com",
        "https://account.microsoft.com",
        "https://www.amazon.com/gp/product",
        "https://www.amazon.com/dp/B08N5WRWNW",
        "https://github.com/user/repository",
        "https://stackoverflow.com/questions/12345",
        
        # More variety
        "https://www.airbnb.com",
        "https://www.uber.com",
        "https://www.lyft.com",
        "https://www.doordash.com",
        "https://www.grubhub.com",
        "https://www.booking.com",
        "https://www.expedia.com",
        "https://www.tripadvisor.com",
    ]
    
    # Create DataFrame
    df_phishing = pd.DataFrame({
        'url': phishing_urls,
        'label': 1  # 1 = phishing
    })
    
    df_legitimate = pd.DataFrame({
        'url': legitimate_urls,
        'label': 0  # 0 = legitimate
    })
    
    # Combine and shuffle
    df = pd.concat([df_phishing, df_legitimate], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    output_path = "ml_engine/data/phishing_dataset.csv"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print("=" * 60)
    print("ENHANCED DATASET CREATED")
    print("=" * 60)
    print(f"Total samples: {len(df)}")
    print(f"Phishing URLs: {sum(df['label'] == 1)}")
    print(f"Legitimate URLs: {sum(df['label'] == 0)}")
    print(f"Saved to: {output_path}")
    print("=" * 60)
    
    return df


if __name__ == "__main__":
    create_enhanced_dataset()
