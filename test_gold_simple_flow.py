#!/usr/bin/env python3
"""
Simple test for gold functionality
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gold_utils_direct():
    """Test gold utils directly"""
    print("=== Testing Gold Utils Directly ===")
    
    try:
        from tradingagents.dataflows.gold_utils import GoldPriceAPI
        
        api = GoldPriceAPI()
        curr_date = datetime.now().strftime("%Y-%m-%d")
        
        # Test current price
        print("Testing get_current_price...")
        result = api.get_current_price()
        print(f"✓ Current price result: {result}")
        print()
        
        # Test historical data
        print("Testing get_historical_data...")
        result = api.get_historical_data(curr_date, 7)
        print(f"✓ Historical data result length: {len(result)}")
        if result:
            print(f"Sample data: {result[0]}")
        print()
        
        # Test market analysis
        print("Testing get_market_analysis...")
        result = api.get_market_analysis(curr_date)
        print(f"✓ Market analysis result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
    except Exception as e:
        print(f"✗ Error testing gold utils: {e}")
        import traceback
        traceback.print_exc()
        print()

def test_interface_functions():
    """Test interface functions directly"""
    print("=== Testing Interface Functions Directly ===")
    
    try:
        # Import only what we need
        from tradingagents.dataflows.gold_utils import GoldPriceAPI
        from tradingagents.dataflows.interface import get_gold_market_analysis, detect_asset_type
        
        curr_date = datetime.now().strftime("%Y-%m-%d")
        
        # Test asset detection
        print("Testing detect_asset_type...")
        result = detect_asset_type("GOLD")
        print(f"✓ GOLD → {result}")
        result = detect_asset_type("BTC")
        print(f"✓ BTC → {result}")
        print()
        
        # Test gold market analysis
        print("Testing get_gold_market_analysis...")
        result = get_gold_market_analysis("GOLD", curr_date)
        print(f"✓ Gold market analysis result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
    except Exception as e:
        print(f"✗ Error testing interface functions: {e}")
        import traceback
        traceback.print_exc()
        print()

def test_toolkit_gold_tools():
    """Test gold tools in toolkit"""
    print("=== Testing Gold Tools in Toolkit ===")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        toolkit = Toolkit()
        curr_date = datetime.now().strftime("%Y-%m-%d")
        
        # Test gold market analysis
        print("Testing get_gold_market_analysis...")
        result = toolkit.get_gold_market_analysis("GOLD", curr_date)
        print(f"✓ Gold market analysis result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
        # Test gold price history
        print("Testing get_gold_price_history...")
        result = toolkit.get_gold_price_history("GOLD", curr_date, 7)
        print(f"✓ Gold price history result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
    except Exception as e:
        print(f"✗ Error testing toolkit gold tools: {e}")
        import traceback
        traceback.print_exc()
        print()

def main():
    """Run all tests"""
    print("🧪 Testing Gold Functionality")
    print("=" * 40)
    print()
    
    # Check environment
    print("=== Environment Check ===")
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    if rapidapi_key:
        print(f"✓ RAPIDAPI_KEY found (length: {len(rapidapi_key)})")
    else:
        print("✗ RAPIDAPI_KEY not found")
    print()
    
    # Run tests
    test_gold_utils_direct()
    test_interface_functions()
    test_toolkit_gold_tools()
    
    print("🎉 Gold functionality testing finished!")

if __name__ == "__main__":
    main()
