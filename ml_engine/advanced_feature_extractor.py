"""
Advanced Feature Extraction for Phishing URL Detection
Research-aligned implementation for parked domain scenarios

Features extracted:
1. Lexical Features (8)
2. Statistical Features (5)
3. Domain-Based Features (7)

Total: 20 features
"""

import re
import math
from urllib.parse import urlparse
import tldextract
import numpy as np
from collections import Counter


class AdvancedFeatureExtractor:
    """
    Research-aligned feature extractor for early phishing detection
    Implements features suitable for parked domain scenarios
    """
    
    def __init__(self):
        self.suspicious_keywords = [
            'login', 'signin', 'verify', 'secure', 'account', 'update',
            'banking', 'confirm', 'suspended', 'locked', 'unusual',
            'activity', 'alert', 'security', 'notification', 'password',
            'credential', 'validate', 'authenticate', 'billing'
        ]
        
        self.suspicious_tlds = [
            '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work',
            '.click', '.link', '.download', '.racing', '.win'
        ]
        
        self.trusted_tlds = [
            '.com', '.org', '.net', '.edu', '.gov', '.mil'
        ]
        
        # Trusted registrars (for reputation scoring)
        self.trusted_registrars = [
            'godaddy', 'namecheap', 'google', 'amazon', 'cloudflare'
        ]
        
        self.feature_names = [
            # Lexical features (8)
            'url_length',
            'num_dots',
            'num_slashes',
            'num_hyphens',
            'num_digits',
            'has_ip_address',
            'suspicious_keyword_count',
            'uses_https',
            
            # Statistical features (5)
            'shannon_entropy',
            'vowel_consonant_ratio',
            'digit_letter_ratio',
            'special_char_ratio',
            'url_randomness_score',
            
            # Domain-based features (11) - ENHANCED
            'domain_length',
            'num_subdomains',
            'tld_category',
            'domain_has_digits',
            'domain_entropy',
            'path_length',
            'query_length',
            # NEW: Research-aligned features
            'domain_age_indicator',      # Simulated domain age
            'registrar_reputation',       # Registrar trust score
            'nameserver_count_estimate',  # Estimated NS count
            'ttl_indicator'              # TTL approximation
        ]
    
    def extract_features(self, url: str) -> np.ndarray:
        """
        Extract all 20 features from URL
        
        Args:
            url (str): URL to analyze
            
        Returns:
            np.ndarray: Feature vector of shape (20,)
        """
        features = []
        
        # Lexical features
        features.extend(self._extract_lexical_features(url))
        
        # Statistical features
        features.extend(self._extract_statistical_features(url))
        
        # Domain-based features
        features.extend(self._extract_domain_features(url))
        
        return np.array(features, dtype=np.float32)
    
    def _extract_lexical_features(self, url: str) -> list:
        """Extract 8 lexical features"""
        features = []
        
        # 1. URL length
        features.append(len(url))
        
        # 2. Number of dots
        features.append(url.count('.'))
        
        # 3. Number of slashes
        features.append(url.count('/'))
        
        # 4. Number of hyphens
        features.append(url.count('-'))
        
        # 5. Number of digits
        features.append(sum(c.isdigit() for c in url))
        
        # 6. Has IP address (binary)
        has_ip = 1 if self._has_ip_address(url) else 0
        features.append(has_ip)
        
        # 7. Suspicious keyword count
        url_lower = url.lower()
        keyword_count = sum(1 for keyword in self.suspicious_keywords if keyword in url_lower)
        features.append(keyword_count)
        
        # 8. Uses HTTPS (binary)
        uses_https = 1 if url.startswith('https://') else 0
        features.append(uses_https)
        
        return features
    
    def _extract_statistical_features(self, url: str) -> list:
        """Extract 5 statistical features"""
        features = []
        
        # 1. Shannon entropy
        features.append(self._calculate_shannon_entropy(url))
        
        # 2. Vowel to consonant ratio
        features.append(self._vowel_consonant_ratio(url))
        
        # 3. Digit to letter ratio
        features.append(self._digit_letter_ratio(url))
        
        # 4. Special character ratio
        features.append(self._special_char_ratio(url))
        
        # 5. URL randomness score
        features.append(self._url_randomness_score(url))
        
        return features
    
    def _extract_domain_features(self, url: str) -> list:
        """Extract 11 domain-based features (7 original + 4 new)"""
        features = []
        
        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
            
            domain = extracted.domain
            subdomain = extracted.subdomain
            tld = f".{extracted.suffix}"
            
            # 1. Domain length
            features.append(len(domain))
            
            # 2. Number of subdomains
            num_subdomains = len(subdomain.split('.')) if subdomain else 0
            features.append(num_subdomains)
            
            # 3. TLD category (0=trusted, 1=neutral, 2=suspicious)
            if tld in self.trusted_tlds:
                tld_category = 0
            elif any(tld.endswith(sus) for sus in self.suspicious_tlds):
                tld_category = 2
            else:
                tld_category = 1
            features.append(tld_category)
            
            # 4. Domain has digits (binary)
            domain_has_digits = 1 if any(c.isdigit() for c in domain) else 0
            features.append(domain_has_digits)
            
            # 5. Domain entropy
            features.append(self._calculate_shannon_entropy(domain))
            
            # 6. Path length
            path_length = len(parsed.path) if parsed.path else 0
            features.append(path_length)
            
            # 7. Query length
            query_length = len(parsed.query) if parsed.query else 0
            features.append(query_length)
            
            # === NEW RESEARCH-ALIGNED FEATURES ===
            
            # 8. Domain Age Indicator (simulated)
            # Heuristic: domains with year patterns, very short domains suspicious
            age_score = self._estimate_domain_age(domain, url)
            features.append(age_score)
            
            # 9. Registrar Reputation (categorical: 2=trusted, 1=neutral, 0=suspicious)
            registrar_score = self._estimate_registrar_reputation(tld)
            features.append(registrar_score)
            
            # 10. Name Server Count Estimate
            # Heuristic: based on TLD and domain characteristics
            ns_count = self._estimate_nameserver_count(tld, domain)
            features.append(ns_count)
            
            # 11. TTL Indicator (simulated)
            # Low TTL often indicates phishing (0=low/suspicious, 1=normal, 2=high/established)
            ttl_score = self._estimate_ttl(tld, domain)
            features.append(ttl_score)
            
        except Exception as e:
            # If parsing fails, return default values
            features = [0] * 11  # Updated count
        
        return features
    
    def _has_ip_address(self, url: str) -> bool:
        """Check if URL contains an IP address"""
        # IPv4 pattern
        ipv4_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        return bool(re.search(ipv4_pattern, url))
    
    def _calculate_shannon_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text"""
        if not text:
            return 0.0
        
        # Count character frequencies
        counter = Counter(text)
        length = len(text)
        
        # Calculate entropy
        entropy = 0.0
        for count in counter.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _vowel_consonant_ratio(self, url: str) -> float:
        """Calculate vowel to consonant ratio"""
        vowels = 'aeiouAEIOU'
        consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        
        vowel_count = sum(1 for c in url if c in vowels)
        consonant_count = sum(1 for c in url if c in consonants)
        
        if consonant_count == 0:
            return 0.0
        
        return vowel_count / consonant_count
    
    def _digit_letter_ratio(self, url: str) -> float:
        """Calculate digit to letter ratio"""
        digits = sum(1 for c in url if c.isdigit())
        letters = sum(1 for c in url if c.isalpha())
        
        if letters == 0:
            return 0.0
        
        return digits / letters
    
    def _special_char_ratio(self, url: str) -> float:
        """Calculate ratio of special characters"""
        special_chars = sum(1 for c in url if not c.isalnum())
        
        if len(url) == 0:
            return 0.0
        
        return special_chars / len(url)
    
    def _url_randomness_score(self, url: str) -> float:
        """
        Calculate URL randomness score
        Higher score = more random (potentially suspicious)
        """
        # Extract alphanumeric characters
        alphanum = ''.join(c for c in url if c.isalnum())
        
        if len(alphanum) < 2:
            return 0.0
        
        # Calculate consecutive character changes
        changes = sum(1 for i in range(len(alphanum) - 1) 
                     if alphanum[i] != alphanum[i + 1])
        
        # Normalize by length
        randomness = changes / (len(alphanum) - 1)
        
        return randomness
    
    def _estimate_domain_age(self, domain: str, url: str) -> float:
        """Estimate domain age using heuristics. Returns: 0.0-1.0 (0=very new/suspicious, 1=established)"""
        age_score = 0.5  # Default neutral
        
        # Well-known domains get high score
        well_known = ['google', 'facebook', 'amazon', 'microsoft', 'apple', 
                      'github', 'stackoverflow', 'wikipedia']
        if any(known in domain.lower() for known in well_known):
            age_score = 1.0
        
        # Domains with year indicators (old pattern)
        elif any(year in url for year in ['2020', '2021', '2022', '2023', '2024']):
            age_score = 0.2  # Recent creation suspicious
        
        # Very short domains (3-4 chars) if not well-known
        elif len(domain) <= 4:
            age_score = 0.3
        
        # Domains with random-looking patterns
        elif self._calculate_shannon_entropy(domain) > 4.0:
            age_score = 0.25  # High randomness = likely new
        
        return age_score
    
    def _estimate_registrar_reputation(self, tld: str) -> int:
        """
        Estimate registrar reputation based on TLD
        Returns: 0=suspicious, 1=neutral, 2=trusted
        """
        # Trusted TLDs typically from reputable registrars
        if tld in self.trusted_tlds:
            return 2
        
        # Suspicious TLDs often from low-reputation registrars
        elif any(tld.endswith(sus) for sus in self.suspicious_tlds):
            return 0
        
        # Neutral
        else:
            return 1
    
    def _estimate_nameserver_count(self, tld: str, domain: str) -> int:
        """
        Estimate nameserver count using heuristics
        Returns: 0-4 (typical range 2-4 for legitimate sites)
        """
        # Trusted TLDs and established patterns typically have 2-4 NS
        if tld in self.trusted_tlds and len(domain) > 5:
            return 3  # Normal
        
        # Suspicious TLDs often have minimal NS setup
        elif any(tld.endswith(sus) for sus in self.suspicious_tlds):
            return 1  # Low/suspicious
        
        # Short or random domains
        elif len(domain) <= 4 or self._calculate_shannon_entropy(domain) > 4.0:
            return 1
        
        else:
            return 2  # Neutral
    
    def _estimate_ttl(self, tld: str, domain: str) -> int:
        """
        Estimate TTL (Time To Live) indicator
        Returns: 0=low/suspicious, 1=normal, 2=high/established
        """
        # Trusted domains typically have higher TTL
        if tld in self.trusted_tlds and len(domain) > 6:
            return 2  # High TTL (established)
        
        # Suspicious TLDs often have low TTL (easy to change)
        elif any(tld.endswith(sus) for sus in self.suspicious_tlds):
            return 0  # Low TTL (suspicious)
        
        # Random-looking domains
        elif self._calculate_shannon_entropy(domain) > 4.0:
            return 0
        
        else:
            return 1  # Normal
    
    def get_feature_names(self) -> list:
        """Return list of feature names"""
        return self.feature_names
    
    def extract_features_dict(self, url: str) -> dict:
        """
        Extract features and return as dictionary
        Useful for debugging and explanation
        """
        features = self.extract_features(url)
        return dict(zip(self.feature_names, features))


# Test the extractor
if __name__ == "__main__":
    extractor = AdvancedFeatureExtractor()
    
    # Test URLs
    test_urls = [
        "https://www.google.com",
        "http://paypal-secure.login-verification.com/signin",
        "http://192.168.1.1/admin/login.php",
        "https://github.com/user/repository"
    ]
    
    print("=" * 80)
    print("ADVANCED FEATURE EXTRACTION TEST")
    print("=" * 80)
    
    for url in test_urls:
        print(f"\nURL: {url}")
        print("-" * 80)
        
        features_dict = extractor.extract_features_dict(url)
        
        for feature_name, value in features_dict.items():
            print(f"  {feature_name:.<30} {value:.4f}")
        
        print()
