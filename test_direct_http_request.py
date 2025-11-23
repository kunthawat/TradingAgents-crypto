#!/usr/bin/env python3
"""
Test direct HTTP request to embeddings endpoint
"""

import sys
import os
import json
import requests

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_direct_embeddings_request():
    """Test direct HTTP request to embeddings endpoint"""
    
    # Import config to get API key and endpoint
    import tradingagents.default_config as default_config
    config = default_config.DEFAULT_CONFIG
    
    api_key = config['api_key']
    embeddings_url = config['embeddings_url']
    
    print(f"Testing direct HTTP request to embeddings endpoint...")
    print(f"URL: {embeddings_url}")
    print(f"API Key: {api_key[:10]}...{api_key[-10:]}")
    print("=" * 60)
    
    # Prepare the request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "input": "This is a test for embeddings",
        "model": "Qwen/Qwen3-Embedding-8B"
    }
    
    try:
        print(f"Sending request...")
        print(f"Headers: {headers}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(embeddings_url, headers=headers, json=data, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"   Embedding dimensions: {len(result['data'][0]['embedding'])}")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_request_formats():
    """Test different request formats"""
    
    import tradingagents.default_config as default_config
    config = default_config.DEFAULT_CONFIG
    
    api_key = config['api_key']
    embeddings_url = config['embeddings_url']
    
    print(f"\nTesting different request formats...")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Different request formats to try
    test_cases = [
        {
            "name": "Standard format",
            "data": {
                "input": "This is a test",
                "model": "Qwen/Qwen3-Embedding-8B"
            }
        },
        {
            "name": "Array input",
            "data": {
                "input": ["This is a test"],
                "model": "Qwen/Qwen3-Embedding-8B"
            }
        },
        {
            "name": "Different model name",
            "data": {
                "input": "This is a test",
                "model": "Qwen3-Embedding-8B"
            }
        },
        {
            "name": "No model specified",
            "data": {
                "input": "This is a test"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(embeddings_url, headers=headers, json=test_case['data'], timeout=10)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ SUCCESS!")
                return True
            else:
                print(f"❌ Failed: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    return False

if __name__ == "__main__":
    # Test direct request
    direct_success = test_direct_embeddings_request()
    
    # Test different formats
    format_success = test_different_request_formats()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
    if direct_success or format_success:
        print("✅ Direct HTTP request works!")
        print("   The issue might be with the OpenAI client library")
    else:
        print("❌ Direct HTTP request also fails")
        print("   The endpoint or API key might be incorrect")
