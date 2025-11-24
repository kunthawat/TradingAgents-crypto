#!/usr/bin/env python3
"""
Test script to verify the TradingAgents API works on port 5000
"""

import requests
import json
import time
import sys

def test_api_endpoints():
    """Test all API endpoints on port 5000"""
    base_url = "http://localhost:5000"
    
    print("Testing TradingAgents API on port 5000")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - make sure it's running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: API info
    print("\n2. Testing API info endpoint...")
    try:
        response = requests.get(f"{base_url}/api/info", timeout=10)
        if response.status_code == 200:
            print("✅ API info endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API info error: {e}")
        return False
    
    # Test 3: Start BTC analysis (without secret password for testing)
    print("\n3. Testing BTC analysis endpoint...")
    test_data = {
        "ticker": "BTC",
        "analysis_date": "2024-05-10",
        "llm_provider": "openai",
        "shallow_thinker": "gpt-4o-mini",
        "deep_thinker": "gpt-4o",
        "research_depth": "comprehensive",
        "analysts": ["market", "news", "social", "fundamentals"],
        "secret_pass": "test_password"  # This will likely fail but tests the endpoint
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/start_analysis",
            json=test_data,
            timeout=10
        )
        if response.status_code == 401:
            print("✅ Analysis endpoint working (password validation working)")
            print("   Expected 401 error for invalid password")
        elif response.status_code == 200:
            print("✅ Analysis started successfully")
            session_id = response.json().get('session_id')
            print(f"   Session ID: {session_id}")
            
            # Test 4: Check session status
            if session_id:
                print(f"\n4. Testing session status for {session_id}...")
                time.sleep(2)  # Wait a bit for analysis to start
                
                status_response = requests.get(
                    f"{base_url}/api/status/{session_id}",
                    timeout=10
                )
                if status_response.status_code == 200:
                    print("✅ Session status endpoint working")
                    status_data = status_response.json()
                    print(f"   Status: {status_data.get('status', 'unknown')}")
                    print(f"   Progress: {status_data.get('progress', 0)}%")
                else:
                    print(f"❌ Session status failed: {status_response.status_code}")
        else:
            print(f"❌ Analysis endpoint unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Analysis endpoint error: {e}")
        return False
    
    return True

def test_web_interface():
    """Test the web interface on port 5000"""
    base_url = "http://localhost:5000"
    
    print("\n5. Testing web interface...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Web interface accessible")
            if "TradingAgents" in response.text or "trading" in response.text.lower():
                print("✅ Web interface content looks correct")
            else:
                print("⚠️  Web interface content may not be loading correctly")
        else:
            print(f"❌ Web interface failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web interface error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("TradingAgents API Port 5000 Test")
    print("=" * 60)
    
    # Test API endpoints
    api_success = test_api_endpoints()
    
    # Test web interface
    web_success = test_web_interface()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print(f"API Tests: {'✅ PASSED' if api_success else '❌ FAILED'}")
    print(f"Web Interface: {'✅ PASSED' if web_success else '❌ FAILED'}")
    
    if api_success and web_success:
        print("\n🎉 ALL TESTS PASSED! Your TradingAgents app is working on port 5000!")
        print("\nYou can now:")
        print("- Access web app at: http://localhost:5000")
        print("- Use API endpoints at: http://localhost:5000/api/")
        print("- Run with Docker: docker run -p 5000:5000 tradingagents")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure the server is running: python web_app.py")
        print("2. Check if port 5000 is available: lsof -i :5000")
        print("3. Verify Docker configuration if using containers")
    
    sys.exit(0 if (api_success and web_success) else 1)
