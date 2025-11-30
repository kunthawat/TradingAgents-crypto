#!/usr/bin/env python3
"""
Direct test of gold API without full module imports
"""

import os
import requests
import json
from datetime import datetime, timedelta

def test_direct_api_call():
    """Test the RapidAPI gold endpoint directly"""
    print("=== Testing Direct Gold API Call ===")
    
    # Check environment
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("❌ RAPIDAPI_KEY not found in environment")
        return None
    
    print(f"✓ RAPIDAPI_KEY found (length: {len(api_key)})")
    
    # Setup API request
    base_url = "https://gold-price-api.p.rapidapi.com/v1"
    headers = {
        'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
        'x-rapidapi-key': api_key
    }
    
    try:
        # Test current price endpoint
        print("\n--- Testing Current Price Endpoint ---")
        current_url = f"{base_url}/gold/current"
        response = requests.get(current_url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            current_data = response.json()
            print(f"Response type: {type(current_data)}")
            print(f"Response keys: {list(current_data.keys()) if isinstance(current_data, dict) else 'Not a dict'}")
            print(f"Response: {json.dumps(current_data, indent=2, default=str)}")
        else:
            print(f"Error response: {response.text}")
            current_data = None
        
        # Test history endpoint
        print("\n--- Testing History Endpoint ---")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        history_url = f"{base_url}/gold/history"
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        response = requests.get(history_url, headers=headers, params=params)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            history_data = response.json()
            print(f"Response type: {type(history_data)}")
            print(f"Response keys: {list(history_data.keys()) if isinstance(history_data, dict) else 'Not a dict'}")
            print(f"Response: {json.dumps(history_data, indent=2, default=str)}")
        else:
            print(f"Error response: {response.text}")
            history_data = None
        
        return current_data, history_data
        
    except Exception as e:
        print(f"❌ Error making API call: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def analyze_api_response(current_data, history_data):
    """Analyze the API response to identify parsing issues"""
    print("\n=== Analyzing API Response ===")
    
    if history_data:
        print("--- History Data Analysis ---")
        
        # Check different possible structures
        if isinstance(history_data, dict):
            print("Response is a dictionary")
            print(f"Top-level keys: {list(history_data.keys())}")
            
            # Look for data in common locations
            possible_data_keys = ['history', 'data', 'results', 'prices', 'quotes']
            for key in possible_data_keys:
                if key in history_data:
                    print(f"Found data in '{key}' key")
                    data_array = history_data[key]
                    if isinstance(data_array, list) and len(data_array) > 0:
                        print(f"Data array length: {len(data_array)}")
                        print(f"First item: {json.dumps(data_array[0], indent=2, default=str)}")
                        
                        # Analyze the structure of the first item
                        first_item = data_array[0]
                        if isinstance(first_item, dict):
                            print(f"First item keys: {list(first_item.keys())}")
                            
                            # Look for price fields
                            price_fields = ['price', 'close', 'open', 'high', 'low', 'value']
                            found_prices = {}
                            for field in price_fields:
                                if field in first_item:
                                    found_prices[field] = first_item[field]
                            
                            if found_prices:
                                print(f"Found price fields: {found_prices}")
                            else:
                                print("❌ No price fields found in first item")
                    break
            else:
                print("❌ No recognized data key found")
        
        elif isinstance(history_data, list):
            print("Response is a list")
            if len(history_data) > 0:
                print(f"List length: {len(history_data)}")
                print(f"First item: {json.dumps(history_data[0], indent=2, default=str)}")
                
                # Analyze first item
                first_item = history_data[0]
                if isinstance(first_item, dict):
                    print(f"First item keys: {list(first_item.keys())}")
                    
                    # Look for price fields
                    price_fields = ['price', 'close', 'open', 'high', 'low', 'value']
                    found_prices = {}
                    for field in price_fields:
                        if field in first_item:
                            found_prices[field] = first_item[field]
                    
                    if found_prices:
                        print(f"Found price fields: {found_prices}")
                    else:
                        print("❌ No price fields found in first item")
        else:
            print(f"Response is unexpected type: {type(history_data)}")
    
    if current_data:
        print("\n--- Current Data Analysis ---")
        print(f"Current data: {json.dumps(current_data, indent=2, default=str)}")

def main():
    """Run direct API test"""
    print("🔍 Testing Gold API Directly")
    print("=" * 40)
    
    # Test API directly
    current_data, history_data = test_direct_api_call()
    
    # Analyze response
    analyze_api_response(current_data, history_data)
    
    print("\n🎯 Direct API Test Complete!")

if __name__ == "__main__":
    main()
