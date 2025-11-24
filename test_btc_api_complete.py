#!/usr/bin/env python3
"""
Complete BTC API Test Script for TradingAgents Crypto

This script demonstrates how to use the API to analyze BTC and get results.
"""

import requests
import json
import time
import sys

# API Configuration
BASE_URL = "http://127.0.0.1:5001"
API_ENDPOINT = f"{BASE_URL}/api/start_analysis"
HEALTH_ENDPOINT = f"{BASE_URL}/health"

# Test Configuration
SECRET_PASSWORD = "your_secret_password_here"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(HEALTH_ENDPOINT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service is healthy: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_btc_analysis():
    """Test BTC analysis via API"""
    print("\n🚀 Starting BTC analysis...")
    
    # Prepare request data
    request_data = {
        "ticker": "BTC",
        "analysis_date": "2025-11-24",
        "analysts": ["fundamentals", "market", "news"],
        "research_depth": 2,
        "llm_provider": "openai",
        "shallow_thinker": "deepseek-ai/DeepSeek-R1-0528",
        "deep_thinker": "deepseek-ai/DeepSeek-R1-0528",
        "language": "english",
        "secret_pass": SECRET_PASSWORD,
        "session_id": f"btc_test_{int(time.time())}"
    }
    
    print(f"📤 Sending request to: {API_ENDPOINT}")
    print(f"📊 Request data: {json.dumps(request_data, indent=2)}")
    
    try:
        # Send the request
        response = requests.post(
            API_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=request_data,
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis started successfully!")
            print(f"📋 Session ID: {data.get('session_id')}")
            print(f"📊 Status: {data.get('status')}")
            
            # Explain what happens next
            print(f"\n🔄 What happens next:")
            print(f"   • Analysis is running in the background")
            print(f"   • Multiple AI agents are analyzing BTC")
            print(f"   • Results will be available via WebSocket")
            print(f"   • Analysis typically takes 2-10 minutes")
            
            return data.get('session_id')
            
        elif response.status_code == 401:
            print(f"❌ Authentication failed - Invalid password")
            return None
            
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"📄 Error response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out - server may be busy")
        return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

def test_different_cryptos():
    """Test API with different cryptocurrencies"""
    print(f"\n🪙 Testing different cryptocurrencies...")
    
    cryptos = ["ETH", "SOL", "ADA", "DOT"]
    
    for crypto in cryptos:
        print(f"\n📈 Testing {crypto} analysis...")
        
        request_data = {
            "ticker": crypto,
            "analysis_date": "2025-11-24",
            "analysts": ["market"],  # Quick test with just market analysis
            "research_depth": 1,
            "llm_provider": "openai",
            "shallow_thinker": "deepseek-ai/DeepSeek-R1-0528",
            "deep_thinker": "deepseek-ai/DeepSeek-R1-0528",
            "language": "english",
            "secret_pass": SECRET_PASSWORD,
            "session_id": f"{crypto}_test_{int(time.time())}"
        }
        
        try:
            response = requests.post(
                API_ENDPOINT,
                headers={"Content-Type": "application/json"},
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {crypto} analysis started: {data.get('session_id')}")
            else:
                print(f"❌ {crypto} analysis failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {crypto} test error: {e}")

def main():
    """Main test function"""
    print("🤖 TradingAgents Crypto - API Test Suite")
    print("=" * 50)
    
    # Test 1: Health Check
    if not test_health_check():
        print("❌ Health check failed - exiting")
        sys.exit(1)
    
    # Test 2: BTC Analysis
    session_id = test_btc_analysis()
    if not session_id:
        print("❌ BTC analysis failed - exiting")
        sys.exit(1)
    
    # Test 3: Different Cryptocurrencies
    test_different_cryptos()
    
    print(f"\n🎉 API Test Suite Completed!")
    print(f"📝 Summary:")
    print(f"   ✅ Health check passed")
    print(f"   ✅ BTC analysis started (Session: {session_id})")
    print(f"   ✅ Multiple crypto tests completed")
    
    print(f"\n📚 Next Steps:")
    print(f"   1. Monitor analysis progress via WebSocket")
    print(f"   2. Check results at: {BASE_URL}/analysis?session={session_id}")
    print(f"   3. Review API documentation in API_USAGE_COMPLETE_GUIDE.md")

if __name__ == "__main__":
    main()
