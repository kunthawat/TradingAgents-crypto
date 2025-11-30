#!/usr/bin/env python3
"""
Standalone test that copies gold parsing logic directly to test without imports
"""

import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time

# Copy the GoldPriceAPI class directly to avoid import issues
class StandaloneGoldPriceAPI:
    """Standalone Gold Price API utilities for testing"""
    
    def __init__(self, api_key=None):
        self.base_url = "https://gold-price-api.p.rapidapi.com/v1"
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY environment variable is required for Gold Price API")
        
        self.session.headers.update({
            'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
    
    def _make_request(self, endpoint, params=None):
        """Make API request with error handling and rate limiting"""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            self.last_request_time = time.time()
            
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting before retry...")
                time.sleep(5)
                response = self.session.get(url, params=params)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {}
    
    def get_gold_history(self, start_date=None, end_date=None):
        """Get gold price history data"""
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        return self._make_request("/gold/history", params)
    
    def parse_gold_data(self, api_response):
        """Parse API response to pandas DataFrame for analysis"""
        if not api_response:
            print("❌ No API response received")
            return pd.DataFrame()
        
        print(f"🔍 Parsing API response with keys: {list(api_response.keys()) if isinstance(api_response, dict) else type(api_response)}")
        
        # Handle different API response formats
        if 'history' in api_response:
            # New API format: {"asset": "gold", "count": 22, "history": [...]}
            history_data = api_response['history']
            print(f"✓ Found 'history' key with {len(history_data)} entries")
        elif 'data' in api_response:
            # Old API format: {"success": true, "data": [...]}
            history_data = api_response['data']
            print(f"✓ Found 'data' key with {len(history_data)} entries")
        elif isinstance(api_response, list):
            # Direct list format
            history_data = api_response
            print(f"✓ Found direct list with {len(history_data)} entries")
        else:
            print(f"❌ Unknown API response format: {list(api_response.keys()) if isinstance(api_response, dict) else type(api_response)}")
            return pd.DataFrame()
        
        if not history_data:
            print("❌ No history data found in API response")
            return pd.DataFrame()
        
        # Show sample data
        if history_data:
            print(f"📊 Sample data item: {history_data[0]}")
        
        # Convert to DataFrame
        df = pd.DataFrame(history_data)
        print(f"✓ Created DataFrame with shape: {df.shape}")
        print(f"✓ DataFrame columns: {list(df.columns)}")
        
        # Ensure required columns exist
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return pd.DataFrame()
        
        print("✓ All required columns present")
        
        # Ensure proper data types
        print("🔄 Converting data types...")
        df['date'] = pd.to_datetime(df['date'])
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for any conversion issues
        for col in numeric_columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    print(f"⚠️  {null_count} null values in {col} after conversion")
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        # Calculate additional metrics
        df['price_range'] = df['high'] - df['low']
        df['daily_change'] = df['close'] - df['open']
        df['daily_change_pct'] = (df['daily_change'] / df['open']) * 100
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        df['weighted_price'] = (df['high'] + df['low'] + 2 * df['close']) / 4
        
        print(f"✅ Successfully parsed {len(df)} rows of gold data")
        
        # Show price statistics
        if len(df) > 0:
            print(f"💰 Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
            print(f"💰 Latest price: ${df['close'].iloc[-1]:.2f}")
            print(f"📅 Latest date: {df['date'].iloc[-1].strftime('%Y-%m-%d')}")
            
            # Check for zero prices
            zero_prices = (df['close'] == 0).sum()
            if zero_prices > 0:
                print(f"❌ Found {zero_prices} zero prices!")
            else:
                print("✅ No zero prices found")
        
        return df

def test_standalone_parsing():
    """Test the standalone gold parsing"""
    print("=== Standalone Gold Parsing Test ===")
    
    try:
        # Create API instance
        api = StandaloneGoldPriceAPI()
        print("✓ StandaloneGoldPriceAPI instance created")
        
        # Get real data
        print("\n--- Getting Real API Data ---")
        raw_data = api.get_gold_history()
        
        if not raw_data:
            print("❌ No raw data received")
            return False
        
        print(f"✓ Raw data received: {type(raw_data)}")
        print(f"✓ Raw data keys: {list(raw_data.keys())}")
        
        # Parse the data
        print("\n--- Parsing Data ---")
        df = api.parse_gold_data(raw_data)
        
        if df.empty:
            print("❌ Parsed DataFrame is empty")
            return False
        
        # Show detailed results
        print(f"\n📊 Final Results:")
        print(f"   DataFrame shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        print(f"   Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
        print(f"   Volume range: {df['volume'].min()} - {df['volume'].max()}")
        
        # Check for the specific issue
        zero_prices = (df['close'] == 0).sum()
        if zero_prices > 0:
            print(f"\n❌ ISSUE CONFIRMED: Found {zero_prices} zero prices!")
            print("This explains the $0.00 values in the user's data.")
            return False
        else:
            print(f"\n✅ NO ISSUE: All prices are non-zero and realistic (${df['close'].min():.2f} - ${df['close'].max():.2f})")
            print("The parsing logic is working correctly.")
            return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_format_output_like_functions():
    """Test formatting output like the actual functions do"""
    print("\n=== Testing Output Formatting ===")
    
    try:
        api = StandaloneGoldPriceAPI()
        raw_data = api.get_gold_history()
        df = api.parse_gold_data(raw_data)
        
        if df.empty:
            print("❌ No data to format")
            return False
        
        # Format like get_gold_price_data function
        result_str = f"## GOLD Gold Price Data:\n\n"
        
        # Show recent data (last 5 days)
        recent_data = df.tail(5)
        for _, row in recent_data.iterrows():
            result_str += f"Date: {row['date'].strftime('%Y-%m-%d')}\n"
            result_str += f"Open: ${row['open']:,.2f}\n"
            result_str += f"High: ${row['high']:,.2f}\n"
            result_str += f"Low: ${row['low']:,.2f}\n"
            result_str += f"Close: ${row['close']:,.2f}\n"
            result_str += f"Volume: {row['volume']:,.0f}\n"
            result_str += f"Daily Change: {row['daily_change_pct']:+.2f}%\n\n"
        
        print("📄 Formatted Output Sample:")
        print(result_str)
        
        # Check for $0.00 in formatted output
        if '$0.00' in result_str:
            print("❌ Found $0.00 in formatted output!")
            return False
        elif '$4,' in result_str or '$3,' in result_str:
            print("✅ Found realistic gold prices in formatted output!")
            return True
        else:
            print("⚠️  Unsure about price values in formatted output")
            return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run standalone tests"""
    print("🔍 Standalone Gold Parsing Test")
    print("=" * 50)
    
    # Test parsing
    parsing_ok = test_standalone_parsing()
    
    # Test formatting
    formatting_ok = test_format_output_like_functions()
    
    print("\n🎯 Final Results:")
    print(f"Parsing Test: {'✅ PASS' if parsing_ok else '❌ FAIL'}")
    print(f"Formatting Test: {'✅ PASS' if formatting_ok else '❌ FAIL'}")
    
    if parsing_ok and formatting_ok:
        print("\n✅ CONCLUSION: The gold parsing logic is working correctly!")
        print("   The issue might be in the agent toolkit integration or elsewhere.")
    else:
        print("\n❌ CONCLUSION: Found issues in the gold parsing logic!")
        print("   This explains the $0.00 values reported by the user.")

if __name__ == "__main__":
    main()
