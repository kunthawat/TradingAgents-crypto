#!/usr/bin/env python3
"""
Test script to verify gold data fix is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gold_data_parsing():
    """Test the fixed gold data parsing"""
    print("🧪 Testing Gold Data Parsing Fix...")
    
    try:
        from tradingagents.dataflows.gold_utils import GoldPriceAPI
        
        # Create API instance
        api = GoldPriceAPI()
        print("✅ GoldPriceAPI instance created")
        
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
        print(df.tail(3)[['date', 'open', 'high', 'low', 'close', 'volume']].to_string())
        
        # Test summary
        print("\n📈 Testing summary generation...")
        summary = api.get_gold_summary(df)
        
        if summary:
            print(f"✅ Summary generated successfully")
            print(f"Current price: ${summary.get('current_price', 'N/A'):,.2f}")
            print(f"Price change: {summary.get('price_change_pct', 'N/A'):+.2f}%")
            print(f"Period high: ${summary.get('period_high', 'N/A'):,.2f}")
            print(f"Period low: ${summary.get('period_low', 'N/A'):,.2f}")
            return True
        else:
            print("❌ Failed to generate summary")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gold_price_function():
    """Test the get_gold_price_data function"""
    print("\n🧪 Testing get_gold_price_data Function...")
    
    try:
        from tradingagents.dataflows.gold_utils import get_gold_price_data
        
        result = get_gold_price_data("GOLD", "2025-11-01", "2025-11-30")
        
        if result and "$0.00" not in result:
            print("✅ get_gold_price_data function works correctly")
            print("Sample output:")
            print(result[:500] + "..." if len(result) > 500 else result)
            return True
        else:
            print("❌ get_gold_price_data function still returning $0.00 values")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Gold Data Fix Verification")
    print("=" * 50)
    
    # Test 1: Data parsing
    parsing_test = test_gold_data_parsing()
    
    # Test 2: Price function
    price_test = test_gold_price_function()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Data Parsing: {'✅' if parsing_test else '❌'}")
    print(f"Price Function: {'✅' if price_test else '❌'}")
    
    if parsing_test and price_test:
        print("\n🎉 Gold data fix is working correctly!")
        print("The $0.00 issue has been resolved.")
        return True
    else:
        print("\n❌ Gold data fix needs more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
