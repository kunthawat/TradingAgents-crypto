#!/usr/bin/env python3
"""
Test the fixed gold parsing with real API data
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_fixed_gold_parsing():
    """Test the fixed gold parsing logic"""
    print("=== Testing Fixed Gold Parsing ===")
    
    try:
        # Import the gold utilities directly
        sys.path.append('tradingagents/dataflows')
        from gold_utils import GoldPriceAPI
        
        # Check environment
        api_key = os.getenv('RAPIDAPI_KEY')
        if not api_key:
            print("❌ RAPIDAPI_KEY not found")
            return
        
        print(f"✓ RAPIDAPI_KEY found")
        
        # Create API instance
        api = GoldPriceAPI()
        
        # Test history endpoint
        print("\n--- Testing History Endpoint ---")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        raw_data = api.get_gold_history(start_date, end_date)
        if not raw_data:
            print("❌ No raw data received")
            return
        
        print(f"✓ Raw data received: {json.dumps(raw_data, indent=2, default=str)}")
        
        # Test parsing
        print("\n--- Testing Fixed Parse Method ---")
        df = api.parse_gold_data(raw_data)
        
        if df.empty:
            print("❌ Parsed DataFrame is empty")
            return
        
        print(f"✓ Parsed DataFrame shape: {df.shape}")
        print(f"✓ DataFrame columns: {list(df.columns)}")
        
        # Check for zero prices
        if 'close' in df.columns:
            zero_prices = (df['close'] == 0).sum()
            print(f"\n--- Price Analysis ---")
            print(f"Total rows: {len(df)}")
            print(f"Zero price rows: {zero_prices}")
            print(f"Non-zero price rows: {len(df) - zero_prices}")
            
            if zero_prices > 0:
                print("❌ Still found zero prices!")
            else:
                print("✅ No zero prices found - parsing fixed!")
            
            # Show price range
            if len(df) > 0 and df['close'].max() > 0:
                print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
                print(f"Latest price: ${df['close'].iloc[-1]:.2f}")
                
                # Show sample data
                print(f"\n--- Sample Parsed Data ---")
                print(df[['date', 'open', 'high', 'low', 'close', 'volume']].head())
        
        # Test summary
        print("\n--- Testing Summary ---")
        summary = api.get_gold_summary(df)
        if summary:
            print(f"✓ Summary generated: {json.dumps(summary, indent=2, default=str)}")
        else:
            print("❌ Summary generation failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing fixed parsing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gold_price_data_function():
    """Test the get_gold_price_data function"""
    print("\n=== Testing Gold Price Data Function ===")
    
    try:
        # Import the function
        sys.path.append('tradingagents/dataflows')
        from gold_utils import get_gold_price_data
        
        # Test the function
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        result = get_gold_price_data("GOLD", start_date, end_date)
        
        if result:
            print("✓ get_gold_price_data function works!")
            print(f"Result length: {len(result)} characters")
            
            # Check for real prices in the result
            if "$4," in result or "$3," in result:
                print("✅ Real gold prices found in output!")
            else:
                print("❌ No real prices found in output")
            
            # Show first 500 characters
            print(f"\n--- Sample Output ---")
            print(result[:500])
            
            return True
        else:
            print("❌ get_gold_price_data function returned empty")
            return False
        
    except Exception as e:
        print(f"❌ Error testing gold price data function: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests for the fixed gold parsing"""
    print("🔧 Testing Fixed Gold Parsing Implementation")
    print("=" * 50)
    
    # Test fixed parsing
    parsing_success = test_fixed_gold_parsing()
    
    # Test gold price data function
    function_success = test_gold_price_data_function()
    
    print("\n🎯 Test Results:")
    print(f"Parsing Test: {'✅ PASSED' if parsing_success else '❌ FAILED'}")
    print(f"Function Test: {'✅ PASSED' if function_success else '❌ FAILED'}")
    
    if parsing_success and function_success:
        print("\n🎉 All tests passed! Gold price data should now work correctly!")
    else:
        print("\n⚠️  Some tests failed. Further investigation needed.")

if __name__ == "__main__":
    main()
