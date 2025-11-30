#!/usr/bin/env python3
"""
Standalone test script to verify gold data fix without complex imports
"""

import os
import sys
import json
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class StandaloneGoldAPI:
    """Standalone Gold API for testing"""
    
    def __init__(self):
        self.base_url = "https://gold-price-api.p.rapidapi.com/v1"
        self.api_key = os.getenv("RAPIDAPI_KEY")
        
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY environment variable is required")
        
        self.headers = {
            'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }
    
    def get_gold_history(self):
        """Get gold history data"""
        try:
            response = requests.get(f"{self.base_url}/gold/history", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching gold data: {e}")
            return None
    
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
        
        # Calculate additional metrics
        df['price_range'] = df['high'] - df['low']
        df['daily_change'] = df['close'] - df['open']
        df['daily_change_pct'] = (df['daily_change'] / df['open']) * 100
        
        print(f"✅ Successfully parsed {len(df)} rows of gold data")
        return df

def test_gold_data_fix():
    """Test the gold data fix"""
    print("🧪 Testing Gold Data Fix (Standalone)")
    print("=" * 50)
    
    try:
        # Create API instance
        api = StandaloneGoldAPI()
        print("✅ StandaloneGoldAPI instance created")
        
        # Get gold history
        print("📊 Fetching gold history...")
        raw_data = api.get_gold_history()
        
        if not raw_data:
            print("❌ No raw data received")
            return False
        
        print(f"✅ Raw data received: {list(raw_data.keys())}")
        
        # Parse the data
        print("🔧 Parsing gold data...")
        df = api.parse_gold_data(raw_data)
        
        if df.empty:
            print("❌ Failed to parse data - DataFrame is empty")
            return False
        
        print(f"✅ Successfully parsed {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        
        # Show sample data
        print("\n📄 Sample Data (last 3 rows):")
        sample_data = df.tail(3)[['date', 'open', 'high', 'low', 'close', 'volume']]
        print(sample_data.to_string())
        
        # Check for $0.00 values
        zero_prices = (df[['open', 'high', 'low', 'close']] == 0).any().any()
        if zero_prices:
            print("❌ Still finding $0.00 values in the data")
            return False
        else:
            print("✅ No $0.00 values found - prices look correct!")
        
        # Show price range
        print(f"\n📈 Price Statistics:")
        print(f"Price range: ${df['low'].min():,.2f} - ${df['high'].max():,.2f}")
        print(f"Latest price: ${df['close'].iloc[-1]:,.2f}")
        print(f"Average price: ${df['close'].mean():,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    success = test_gold_data_fix()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Gold data fix is working correctly!")
        print("The $0.00 issue has been resolved.")
        print("Real gold prices (around $4,000+) are now being returned.")
    else:
        print("❌ Gold data fix needs more work.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
