#!/usr/bin/env python3
"""
Test current gold API response to identify parsing issues
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_raw_api_response():
    """Test the raw API response to see current format"""
    print("=== Testing Raw Gold API Response ===")
    
    try:
        from tradingagents.dataflows.gold_utils import GoldPriceAPI
        
        # Check environment
        api_key = os.getenv('RAPIDAPI_KEY')
        if not api_key:
            print("❌ RAPIDAPI_KEY not found in environment")
            return
        
        print(f"✓ RAPIDAPI_KEY found (length: {len(api_key)})")
        
        # Create API instance
        api = GoldPriceAPI()
        
        # Test current price endpoint
        print("\n--- Testing Current Price Endpoint ---")
        current_data = api.get_current_gold_price()
        print(f"Current price response type: {type(current_data)}")
        print(f"Current price response keys: {list(current_data.keys()) if isinstance(current_data, dict) else 'Not a dict'}")
        print(f"Current price response: {json.dumps(current_data, indent=2, default=str)}")
        
        # Test history endpoint
        print("\n--- Testing History Endpoint ---")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        history_data = api.get_gold_history(start_date, end_date)
        print(f"History response type: {type(history_data)}")
        print(f"History response keys: {list(history_data.keys()) if isinstance(history_data, dict) else 'Not a dict'}")
        print(f"History response: {json.dumps(history_data, indent=2, default=str)}")
        
        return current_data, history_data
        
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def test_parsing_logic():
    """Test the current parsing logic with the API response"""
    print("\n=== Testing Current Parsing Logic ===")
    
    try:
        from tradingagents.dataflows.gold_utils import GoldPriceAPI
        
        api = GoldPriceAPI()
        
        # Get some data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        raw_data = api.get_gold_history(start_date, end_date)
        if not raw_data:
            print("❌ No raw data received")
            return
        
        print(f"Raw data received: {json.dumps(raw_data, indent=2, default=str)}")
        
        # Test parsing
        print("\n--- Testing Parse Method ---")
        df = api.parse_gold_data(raw_data)
        
        if df.empty:
            print("❌ Parsed DataFrame is empty")
        else:
            print(f"✓ Parsed DataFrame shape: {df.shape}")
            print(f"✓ DataFrame columns: {list(df.columns)}")
            print(f"✓ DataFrame dtypes: {df.dtypes.to_dict()}")
            
            # Show first few rows
            print("\n--- First 5 Rows of Parsed Data ---")
            print(df.head())
            
            # Check for zero prices
            if 'close' in df.columns:
                zero_prices = (df['close'] == 0).sum()
                print(f"\n--- Price Analysis ---")
                print(f"Total rows: {len(df)}")
                print(f"Zero price rows: {zero_prices}")
                print(f"Non-zero price rows: {len(df) - zero_prices}")
                
                if zero_prices > 0:
                    print("❌ Found zero prices - parsing issue confirmed!")
                else:
                    print("✓ No zero prices found")
                
                # Show price range
                if len(df) > 0 and df['close'].max() > 0:
                    print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
                    print(f"Latest price: ${df['close'].iloc[-1]:.2f}")
        
    except Exception as e:
        print(f"❌ Error testing parsing: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests to identify the parsing issue"""
    print("🔍 Testing Current Gold API Implementation")
    print("=" * 50)
    
    # Test raw API response
    current_data, history_data = test_raw_api_response()
    
    # Test parsing logic
    test_parsing_logic()
    
    print("\n🎯 Analysis Complete!")
    print("Check the output above to identify the parsing issue.")

if __name__ == "__main__":
    main()
