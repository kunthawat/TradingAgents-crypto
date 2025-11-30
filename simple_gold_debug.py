#!/usr/bin/env python3
"""
Simple debug script to test Gold API connection without complex imports
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_variables():
    """Test if environment variables are properly loaded"""
    print("🔍 Testing Environment Variables...")
    
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    print(f"RAPIDAPI_KEY: {'✅ Found' if rapidapi_key else '❌ Missing'}")
    if rapidapi_key:
        print(f"Key length: {len(rapidapi_key)} characters")
        print(f"Key format: {rapidapi_key[:10]}...{rapidapi_key[-10:]}")
    
    return rapidapi_key

def test_direct_api_call():
    """Test direct API call to RapidAPI"""
    print("\n🌐 Testing Direct API Call...")
    
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    if not rapidapi_key:
        print("❌ No RAPIDAPI_KEY found")
        return None
    
    url = "https://gold-price-api.p.rapidapi.com/v1/gold/history"
    headers = {
        'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    try:
        print(f"Making request to: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ API Response received successfully")
                print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                # Pretty print the response
                print("\n📄 Full API Response:")
                print(json.dumps(data, indent=2))
                
                return data
            except json.JSONDecodeError as e:
                print(f"❌ JSON Decode Error: {e}")
                print(f"Raw Response: {response.text[:500]}...")
                return None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Error Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Exception: {e}")
        return None

def test_alternative_endpoints():
    """Test alternative API endpoints"""
    print("\n🔄 Testing Alternative Endpoints...")
    
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    if not rapidapi_key:
        print("❌ No RAPIDAPI_KEY found")
        return
    
    endpoints = [
        "/gold/current",
        "/gold/history",
        "/gold/spot",
        "/gold/price"
    ]
    
    base_url = "https://gold-price-api.p.rapidapi.com/v1"
    headers = {
        'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
        'x-rapidapi-key': rapidapi_key
    }
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            print(f"\n📍 Testing: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success - Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                # Show a preview of the data
                if isinstance(data, dict) and 'data' in data:
                    sample_data = data['data']
                    if isinstance(sample_data, list) and sample_data:
                        print(f"Sample item: {sample_data[0]}")
                    else:
                        print(f"Data content: {sample_data}")
                else:
                    print(f"Response preview: {str(data)[:200]}...")
            else:
                print(f"❌ Failed: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main debug function"""
    print("🧪 Simple Gold API Debug Script")
    print("=" * 50)
    
    # Test 1: Environment variables
    rapidapi_key = test_env_variables()
    if not rapidapi_key:
        print("\n❌ RAPIDAPI_KEY not found. Please add it to your .env file.")
        return False
    
    # Test 2: Direct API call
    api_response = test_direct_api_call()
    
    # Test 3: Alternative endpoints
    test_alternative_endpoints()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Debug Summary:")
    print(f"Environment Variables: ✅" if rapidapi_key else "❌")
    print(f"Direct API Call: ✅" if api_response else "❌")
    
    if api_response:
        print("\n🔍 API Response Analysis:")
        if isinstance(api_response, dict):
            print(f"Response structure: {list(api_response.keys())}")
            
            # Look for data in common locations
            data_locations = ['data', 'history', 'prices', 'results', 'items']
            for location in data_locations:
                if location in api_response:
                    print(f"Found data in '{location}': {type(api_response[location])}")
                    if isinstance(api_response[location], list):
                        print(f"  - Number of items: {len(api_response[location])}")
                        if api_response[location]:
                            print(f"  - First item keys: {list(api_response[location][0].keys()) if isinstance(api_response[location][0], dict) else 'Not a dict'}")
    
    return api_response is not None

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
