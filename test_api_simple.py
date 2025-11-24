#!/usr/bin/env python3
"""
Simple API test script to verify TradingAgents API functionality
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the main API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing TradingAgents API...")
    print(f"📍 Base URL: {base_url}")
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Failed: {e}")
    
    # Test 2: Analyze BTC
    print("\n2. Testing BTC analysis endpoint...")
    try:
        payload = {
            "ticker": "BTC",
            "news_ticker": "BTC",
            "interval": "1d",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
        
        print(f"   Sending request: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{base_url}/analyze",
            json=payload,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Analysis completed successfully!")
            print(f"   📊 Result keys: {list(result.keys())}")
            
            # Check for key components
            if 'final_decision' in result:
                print(f"   🎯 Final Decision: {result['final_decision']}")
            if 'bull_researcher' in result:
                print(f"   📈 Bull Researcher: Available")
            if 'bear_researcher' in result:
                print(f"   📉 Bear Researcher: Available")
            if 'risk_manager' in result:
                print(f"   ⚠️  Risk Manager: Available")
                
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   Failed: {e}")
    
    # Test 3: Check if server is running
    print("\n3. Testing server availability...")
    try:
        response = requests.get(base_url, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Server is running")
        else:
            print(f"   ⚠️  Server returned: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Server not accessible: {e}")
        print("   💡 Make sure the web app is running with: python3 web_app.py")

if __name__ == "__main__":
    test_api_endpoints()
