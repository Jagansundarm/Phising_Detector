"""
Comprehensive API Testing Script
Tests all endpoints of the research-aligned phishing detection system
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_health():
    """Test health check endpoint"""
    print_section("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print_section("TEST 2: Model Info")
    
    try:
        response = requests.get(f"{API_URL}/model-info")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Model Type: {data.get('model_type')}")
        print(f"Best Model: {data.get('best_model')}")
        print(f"F1-Score: {data.get('f1_score', 0):.4f}")
        print(f"Accuracy: {data.get('accuracy', 0):.4f}")
        print(f"Features Count: {data.get('features_count')}")
        
        assert response.status_code == 200
        assert data.get('features_count') == 20
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_predict_phishing():
    """Test prediction with known phishing URL"""
    print_section("TEST 3: Predict Phishing URL")
    
    test_url = "http://paypal-verify.suspicious-login.tk/account/update"
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"url": test_url}
        )
        print(f"Test URL: {test_url}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Prediction: {data.get('prediction')}")
        print(f"Confidence: {data.get('confidence', 0):.4f}")
        print(f"Risk Level: {data.get('risk_level')}")
        print(f"Is Safe: {data.get('is_safe')}")
        
        assert response.status_code == 200
        assert data.get('prediction') == 'phishing'
        assert data.get('is_safe') == False
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_predict_legitimate():
    """Test prediction with legitimate URL"""
    print_section("TEST 4: Predict Legitimate URL")
    
    test_url = "https://www.google.com"
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"url": test_url}
        )
        print(f"Test URL: {test_url}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Prediction: {data.get('prediction')}")
        print(f"Confidence: {data.get('confidence', 0):.4f}")
        print(f"Risk Level: {data.get('risk_level')}")
        print(f"Is Safe: {data.get('is_safe')}")
        
        assert response.status_code == 200
        assert data.get('prediction') == 'legitimate'
        assert data.get('is_safe') == True
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_explain():
    """Test explanation endpoint"""
    print_section("TEST 5: Feature Explanation")
    
    test_url = "http://192.168.1.1/admin/login.php?redirect=verify"
    
    try:
        response = requests.post(
            f"{API_URL}/explain",
            json={"url": test_url}
        )
        print(f"Test URL: {test_url}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        print(f"\nPrediction: {data.get('prediction')}")
        print(f"Confidence: {data.get('confidence', 0):.4f}")
        
        print(f"\nTop Indicators:")
        for i, indicator in enumerate(data.get('top_indicators', [])[:3], 1):
            print(f"  {i}. {indicator.get('feature')}: {indicator.get('value')}")
            print(f"     Severity: {indicator.get('severity')}")
            print(f"     {indicator.get('description')}")
        
        print(f"\nExplanation:")
        print(f"  {data.get('explanation')}")
        
        print(f"\nFeature Count: {len(data.get('features', {}))}")
        
        assert response.status_code == 200
        assert 'features' in data
        assert 'top_indicators' in data
        assert 'explanation' in data
        assert len(data.get('features', {})) == 20
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_edge_cases():
    """Test edge cases"""
    print_section("TEST 6: Edge Cases")
    
    test_cases = [
        ("https://github.com/user/phishing-detection", "legitimate"),
        ("http://bit.ly/shortened-url", "varies"),
        ("https://amazon.co.uk/products", "legitimate"),
    ]
    
    passed = 0
    for url, expected in test_cases:
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={"url": url}
            )
            data = response.json()
            print(f"\n  URL: {url}")
            print(f"  Prediction: {data.get('prediction')}")
            print(f"  Confidence: {data.get('confidence', 0):.4f}")
            
            if response.status_code == 200:
                passed += 1
                print(f"  ✅ Valid response")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def run_all_tests():
    """Run all tests and generate report"""
    print("\n" + "=" * 80)
    print("  RESEARCH-ALIGNED PHISHING DETECTION SYSTEM - API TEST SUITE")
    print("=" * 80)
    print(f"  Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  API URL: {API_URL}")
    print("=" * 80)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Model Info", test_model_info()))
    results.append(("Predict Phishing", test_predict_phishing()))
    results.append(("Predict Legitimate", test_predict_legitimate()))
    results.append(("Feature Explanation", test_explain()))
    results.append(("Edge Cases", test_edge_cases()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name:.<50} {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"  End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed == total:
        print("\n  🎉 ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT")
    else:
        print(f"\n  ⚠️  {total - passed} TEST(S) FAILED - REVIEW REQUIRED")
    
    print("=" * 80)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
