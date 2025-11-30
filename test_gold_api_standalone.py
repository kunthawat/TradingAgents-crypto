#!/usr/bin/env python3
"""
Standalone test for Gold API to bypass import issues
"""

import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time

def test_gold_api_direct():
    """Test the Gold API directly without module imports"""
    print("=== Direct Gold API Test ===")
    
    # Get API key
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("❌ RAPIDAPI_KEY not found in environment")
        return
    
    print(f"✓ RAPIDAPI_KEY found (length: {len(api_key)})")
    
    # API configuration
    base_url = "https://gold-price-api.p.rapidapi.com/v1"
    headers = {
        'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
        'x-rapidapi-key': api_key
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    # Test different endpoints
    endpoints_to_test = [
        "/gold/history",
        "/gold/current", 
        "/gold/price",
        "/gold",
        "/latest"
    ]
    
    for endpoint in endpoints_to_test:
        print(f"\n--- Testing Endpoint: {endpoint} ---")
        
        try:
            url = f"{base_url}{endpoint}"
            print(f"Requesting: {url}")
            
            # Try with and without parameters
            for params in [{}, {"start_date": "2025-11-01", "end_date": "2025-11-30"}]:
                try:
                    response = session.get(url, params=params, timeout=10)
                    print(f"Status Code: {response.status_code}")
                    print(f"Headers: {dict(response.headers)}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(f"Response Type: {type(data)}")
                            print(f"Response Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                            print(f"Response Sample: {json.dumps(data, indent=2, default=str)[:1000]}...")
                            
                            # Analyze the response structure
                            if isinstance(data, dict):
                                if 'history' in data:
                                    print(f"History entries: {len(data['history'])}")
                                    if data['history']:
                                        print(f"Sample history item: {data['history'][0]}")
                                elif 'data' in data:
                                    print(f"Data entries: {len(data['data'])}")
                                    if data['data']:
                                        print(f"Sample data item: {data['data'][0]}")
                                elif isinstance(data, list):
                                    print(f"List length: {len(data)}")
                                    if data:
                                        print(f"Sample list item: {data[0]}")
                            
                            break  # Success, no need to try other params
                            
                        except json.JSONDecodeError as e:
                            print(f"JSON Decode Error: {e}")
                            print(f"Raw Response: {response.text[:500]}...")
                    else:
                        print(f"Error Response: {response.text[:500]}...")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Request Error: {e}")
                    
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    session.close()

def test_manual_gold_request():
    """Test manual request to understand API structure"""
    print("\n=== Manual Gold API Request Test ===")
    
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("❌ RAPIDAPI_KEY not found")
        return
    
    # Try different RapidAPI gold endpoints
    possible_endpoints = [
        "https://gold-price-api.p.rapidapi.com/v1/gold/history",
        "https://gold-price-api.p.rapidapi.com/v1/gold/current",
        "https://gold-price-api.p.rapidapi.com/v1/latest",
        "https://market-data-tracker.p.rapidapi.com/gold/price",
        "https://gold-api.p.rapidapi.com/v1/spot",
        "https://api.metals.live/v1/spot/gold"
    ]
    
    headers = {
        'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
        'x-rapidapi-key': api_key
    }
    
    for url in possible_endpoints:
        print(f"\n--- Testing URL: {url} ---")
        
        try:
            # Update host header based on URL
            if 'gold-price-api' in url:
                headers['x-rapidapi-host'] = 'gold-price-api.p.rapidapi.com'
            elif 'market-data-tracker' in url:
                headers['x-rapidapi-host'] = 'market-data-tracker.p.rapidapi.com'
            elif 'gold-api' in url:
                headers['x-rapidapi-host'] = 'gold-api.p.rapidapi.com'
            elif 'metals.live' in url:
                headers['x-rapidapi-host'] = 'api.metals.live'
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✓ Success! Response type: {type(data)}")
                    print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    
                    # Look for price data
                    if isinstance(data, dict):
                        for key in ['price', 'close', 'last', 'spot', 'bid', 'ask']:
                            if key in data:
                                print(f"Found price field '{key}': {data[key]}")
                    
                    print(f"Sample: {json.dumps(data, indent=2, default=str)[:800]}...")
                    break  # Found working endpoint
                    
                except json.JSONDecodeError:
                    print(f"Raw response: {response.text[:300]}...")
            else:
                print(f"Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"Request failed: {e}")

def main():
    """Run all API tests"""
    print("🔍 Standalone Gold API Diagnosis")
    print("=" * 50)
    
    # Test the configured API
    test_gold_api_direct()
    
    # Test alternative endpoints
    test_manual_gold_request()
    
    print("\n🎯 API Diagnosis Complete!")

if __name__ == "__main__":
    main()
