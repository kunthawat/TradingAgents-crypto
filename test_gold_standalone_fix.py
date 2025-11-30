#!/usr/bin/env python3
"""
Standalone test of the gold API fix without full module imports
"""

import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time

class StandaloneGoldAPI:
    """Standalone gold API for testing"""
    
    def __init__(self, api_key):
        self.base_url = "https://gold-price-api.p.rapidapi.com/v1"
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        })
    
    def get_gold_history(self, start_date=None, end_date=None):
        """Get gold history data"""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        try:
            response = self.session.get(f"{self.base_url}/gold/history", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return {}
    
    def parse_gold_data(self, api_response):
        """Parse gold data with the fixed logic"""
        if not api_response:
            print("❌ No API response received")
            return pd.DataFrame()
        
        # Handle different API response formats
        if 'history' in api_response:
            # New API format: {"asset": "gold", "count": 22, "history": [...]}
            history_data = api_response['history']
        elif 'data' in api_response:
            # Old API format: {"success": true, "data": [...]}
            history_data = api_response['data']
        elif isinstance(api_response, list):
            # Direct list format
            history_data = api_response
        else:
            print(f"❌ Unknown API response format: {list(api_response.keys()) if isinstance(api_response, dict) else type(api_response)}")
            return pd.DataFrame()
        
        if not history_data:
            print("❌ No history data found in API response")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(history_data)
        
        # Ensure required columns exist
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return pd.DataFrame()
        
        # Ensure proper data types
        df['date'] = pd.to_datetime(df['date'])
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        print(f"✅ Successfully parsed {len(df)} rows of gold data")
        return df

def test_standalone_gold_fix():
    """Test the standalone gold fix"""
    print("=== Testing Standalone Gold Fix ===")
    
    # Check environment
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("❌ RAPIDAPI_KEY not found")
        return False
    
    print(f"✓ RAPIDAPI_KEY found")
    
    # Create API instance
    api = StandaloneGoldAPI(api_key)
    
    # Test API call
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    print(f"\n--- Testing API Call ({start_date} to {end_date}) ---")
    raw_data = api.get_gold_history(start_date, end_date)
    
    if not raw_data:
        print("❌ No raw data received")
        return False
    
    print(f"✓ Raw data received")
    print(f"Response keys: {list(raw_data.keys())}")
    
    # Test parsing
    print("\n--- Testing Fixed Parsing ---")
    df = api.parse_gold_data(raw_data)
    
    if df.empty:
        print("❌ Parsed DataFrame is empty")
        return False
    
    print(f"✓ DataFrame shape: {df.shape}")
    print(f"✓ Columns: {list(df.columns)}")
    
    # Check for real prices
    if 'close' in df.columns:
        zero_prices = (df['close'] == 0).sum()
        print(f"\n--- Price Analysis ---")
        print(f"Total rows: {len(df)}")
        print(f"Zero price rows: {zero_prices}")
        print(f"Non-zero price rows: {len(df) - zero_prices}")
        
        if zero_prices > 0:
            print("❌ Still found zero prices!")
            return False
        else:
            print("✅ No zero prices found - parsing fixed!")
        
        # Show price range
        if len(df) > 0 and df['close'].max() > 0:
            print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
            print(f"Latest price: ${df['close'].iloc[-1]:.2f}")
            
            # Show sample data
            print(f"\n--- Sample Data ---")
            print(df[['date', 'open', 'high', 'low', 'close', 'volume']].head(3))
            
            return True
    
    return False

def main():
    """Run the standalone test"""
    print("🔧 Testing Standalone Gold Fix")
    print("=" * 40)
    
    success = test_standalone_gold_fix()
    
    print(f"\n🎯 Result: {'✅ PASSED' if success else '❌ FAILED'}")
    
    if success:
        print("\n🎉 The gold parsing fix works correctly!")
        print("Real gold prices are being extracted from the API response.")
        print("The web application should now show correct gold prices.")
    else:
        print("\n⚠️  The fix did not resolve the issue.")

if __name__ == "__main__":
    main()
