"""
Feature Extraction Module for Phishing URL Detection
Extracts lexical and structural features from URLs
"""

import re
from urllib.parse import urlparse
import tldextract
import numpy as np


class URLFeatureExtractor:
    """Extract features from URLs for ML model"""
    
    def __init__(self):
        self.feature_names = [
            'url_length',
            'num_dots',
            'num_hyphens',
            'num_underscores',
            'num_slashes',
            'num_questionmarks',
            'num_equals',
            'num_at',
            'num_ampersand',
            'num_digits',
            'num_special_chars',
            'has_ip',
            'has_https',
            'domain_length',
            'subdomain_length',
            'path_length',
            'num_subdomains',
            'hostname_length',
            'num_params',
            'entropy'
        ]
    
    def extract_features(self, url):
        """
        Extract all features from a single URL
        
        Args:
            url (str): URL to analyze
            
        Returns:
            np.array: Feature vector
        """
        features = []
        
        # Basic URL properties
        features.append(len(url))  # url_length
        features.append(url.count('.'))  # num_dots
        features.append(url.count('-'))  # num_hyphens
        features.append(url.count('_'))  # num_underscores
        features.append(url.count('/'))  # num_slashes
        features.append(url.count('?'))  # num_questionmarks
        features.append(url.count('='))  # num_equals
        features.append(url.count('@'))  # num_at
        features.append(url.count('&'))  # num_ampersand
        features.append(sum(c.isdigit() for c in url))  # num_digits
        
        # Special characters count
        special_chars = re.findall(r'[^a-zA-Z0-9]', url)
        features.append(len(special_chars))  # num_special_chars
        
        # Check if URL contains IP address
        ip_pattern = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
        has_ip = 1 if re.search(ip_pattern, url) else 0
        features.append(has_ip)
        
        # HTTPS check
        features.append(1 if url.startswith('https://') else 0)  # has_https
        
        # Parse URL components
        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
            
            # Domain features
            domain = extracted.domain
            subdomain = extracted.subdomain
            path = parsed.path
            
            features.append(len(domain))  # domain_length
            features.append(len(subdomain))  # subdomain_length
            features.append(len(path))  # path_length
            
            # Count subdomains
            num_subdomains = len(subdomain.split('.')) if subdomain else 0
            features.append(num_subdomains)  # num_subdomains
            
            # Hostname length
            hostname = parsed.netloc
            features.append(len(hostname))  # hostname_length
            
            # Query parameters count
            query = parsed.query
            num_params = len(query.split('&')) if query else 0
            features.append(num_params)  # num_params
            
        except Exception as e:
            # If parsing fails, use default values
            features.extend([0, 0, 0, 0, 0, 0])
        
        # Calculate Shannon entropy
        entropy = self._calculate_entropy(url)
        features.append(entropy)
        
        return np.array(features)
    
    def extract_batch(self, urls):
        """
        Extract features from multiple URLs
        
        Args:
            urls (list): List of URLs
            
        Returns:
            np.array: Feature matrix (n_samples, n_features)
        """
        return np.array([self.extract_features(url) for url in urls])
    
    def _calculate_entropy(self, text):
        """Calculate Shannon entropy of a string"""
        if not text:
            return 0
        
        # Count character frequencies
        frequencies = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0
        text_len = len(text)
        for count in frequencies.values():
            probability = count / text_len
            entropy -= probability * np.log2(probability)
        
        return entropy


def main():
    """Test the feature extractor"""
    extractor = URLFeatureExtractor()
    
    # Test URLs
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login.php",
        "https://secure-banking-login.phishing-site.com/verify?id=123&token=abc"
    ]
    
    print("Testing Feature Extraction:\n")
    for url in test_urls:
        features = extractor.extract_features(url)
        print(f"URL: {url}")
        print(f"Features: {features}")
        print(f"Feature count: {len(features)}\n")


if __name__ == "__main__":
    main()
