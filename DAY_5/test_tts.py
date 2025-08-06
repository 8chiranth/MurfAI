#!/usr/bin/env python3
"""
Test script for the TTS Flask server
Usage: python test_tts.py
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5001"

def test_endpoint(url, method="GET", data=None, description=""):
    """Test a single endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"📡 {method} {url}")
    print("-" * 40)
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=30)
        
        print(f"📊 Status: {response.status_code}")
        
        try:
            json_response = response.json()
            print(f"📝 Response:")
            print(json.dumps(json_response, indent=2))
            
            if response.status_code == 200:
                print("✅ SUCCESS")
                return True
            else:
                print("❌ FAILED")
                return False
                
        except json.JSONDecodeError:
            print(f"📝 Response (text): {response.text[:200]}...")
            return response.status_code == 200
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR - Is your Flask server running?")
        print(f"   Start server with: python app.py")
        return False
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Flask TTS Server Test Suite")
    print("=" * 50)
    
    tests = [
        {
            "url": f"{BASE_URL}/health",
            "method": "GET",
            "description": "Health Check Endpoint"
        },
        {
            "url": f"{BASE_URL}/tts/test",
            "method": "GET", 
            "description": "TTS Test Endpoint"
        },
        {
            "url": f"{BASE_URL}/",
            "method": "GET",
            "description": "Home Page"
        },
        {
            "url": f"{BASE_URL}/tts",
            "method": "POST",
            "data": {
                "text": "Hello! This is a test of the Murf TTS integration. The system is working correctly.",
                "voice_id": "en-US-davis",
                "format": "mp3"
            },
            "description": "TTS Conversion Endpoint"
        }
    ]
    
    results = []
    
    for test in tests:
        success = test_endpoint(
            test["url"], 
            test.get("method", "GET"), 
            test.get("data"), 
            test["description"]
        )
        results.append(success)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your TTS server is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
    
    print("\n🔗 Quick Access URLs:")
    print(f"   • Test endpoint: {BASE_URL}/tts/test")
    print(f"   • Health check: {BASE_URL}/health")
    print(f"   • Main app: {BASE_URL}/")

if __name__ == "__main__":
    main()