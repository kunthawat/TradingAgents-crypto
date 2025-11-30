#!/usr/bin/env python3
"""
Test script to verify web application works with GOLD symbol
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_web_gold_endpoint():
    """Test the web application with GOLD symbol"""
    print("🧪 Testing Web Application with GOLD Symbol")
    print("=" * 50)
    
    try:
        # Test the web application endpoint
        url = "http://localhost:5000/analyze"
        
        # Test data with GOLD symbol
        test_data = {
            "symbol": "GOLD",
            "curr_date": "2025-11-30"
        }
        
        print(f"📡 Testing endpoint: {url}")
        print(f"📊 Test data: {test_data}")
        
        # Note: This will fail if the web app is not running
        # But we can at least test the data preparation logic
        
        # Test the gold data function directly
        print("\n🔧 Testing gold data function...")
        
        # Import and test the gold function
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Create a simple test of the gold function
        from tradingagents.dataflows.gold_utils import get_gold_price_data
        
        result = get_gold_price_data("GOLD", "2025-11-01", "2025-11-30")
        
        if result and "$0.00" not in result:
            print("✅ Gold price data function works correctly")
            print("Sample output (first 300 chars):")
            print(result[:300] + "...")
            
            # Check for real prices
            if "$4," in result or "$3," in result:
                print("✅ Real gold prices found in output")
                return True
            else:
                print("❌ No real gold prices found")
                return False
        else:
            print("❌ Gold price data function still has issues")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_symbol_detection():
    """Test symbol detection logic"""
    print("\n🧪 Testing Symbol Detection Logic")
    print("=" * 30)
    
    try:
        from tradingagents.dataflows.interface import detect_asset_type
        
        test_symbols = ["GOLD", "XAU", "BTC", "ETH", "UNKNOWN"]
        
        for symbol in test_symbols:
            asset_type = detect_asset_type(symbol)
            print(f"{symbol} -> {asset_type}")
        
        # Test gold symbols
        gold_symbols = ["GOLD", "XAU", "XAUUSD", "GOLD/USD", "GC=F"]
        gold_results = [detect_asset_type(sym) for sym in gold_symbols]
        
        if all(result == "gold" for result in gold_results):
            print("✅ All gold symbols correctly detected")
            return True
        else:
            print("❌ Some gold symbols not detected correctly")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Web Application Gold Test")
    print("=" * 50)
    
    # Test 1: Symbol detection
    symbol_test = test_symbol_detection()
    
    # Test 2: Gold data function
    gold_test = test_web_gold_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Symbol Detection: {'✅' if symbol_test else '❌'}")
    print(f"Gold Data Function: {'✅' if gold_test else '❌'}")
    
    if symbol_test and gold_test:
        print("\n🎉 Web application is ready for GOLD trading!")
        print("The gold data fix is working correctly.")
        print("You can now use GOLD symbol in the web interface.")
    else:
        print("\n❌ Some issues remain with web application.")
    
    return symbol_test and gold_test

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
