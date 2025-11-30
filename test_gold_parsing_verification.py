#!/usr/bin/env python3
"""
Test to verify gold parsing works correctly with real API data
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gold_parsing_with_real_data():
    """Test gold parsing with real API data"""
    print("=== Testing Gold Parsing with Real API Data ===")
    
    try:
        # Import the gold utils directly
        from tradingagents.dataflows.gold_utils import GoldPriceAPI
        
        # Create API instance
        api = GoldPriceAPI()
        print("✓ GoldPriceAPI instance created")
        
        # Get real data
        print("\n--- Getting Real API Data ---")
        raw_data = api.get_gold_history()
        print(f"Raw data keys: {list(raw_data.keys()) if raw_data else 'None'}")
        
        if raw_data:
            print(f"Asset: {raw_data.get('asset')}")
            print(f"Count: {raw_data.get('count')}")
            if 'history' in raw_data:
                print(f"History entries: {len(raw_data['history'])}")
                if raw_data['history']:
                    sample = raw_data['history'][0]
                    print(f"Sample entry: {sample}")
        
        # Parse the data
        print("\n--- Parsing Data ---")
        df = api.parse_gold_data(raw_data)
        
        if df.empty:
            print("❌ Parsed DataFrame is empty")
            return False
        else:
            print(f"✓ Parsed DataFrame shape: {df.shape}")
            print(f"✓ Columns: {list(df.columns)}")
            
            # Check for zero prices
            zero_prices = (df['close'] == 0).sum()
            print(f"Zero price rows: {zero_prices}")
            print(f"Non-zero price rows: {len(df) - zero_prices}")
            
            # Show price statistics
            if len(df) > 0:
                print(f"Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
                print(f"Latest price: ${df['close'].iloc[-1]:.2f}")
                print(f"Latest date: {df['date'].iloc[-1].strftime('%Y-%m-%d')}")
                
                # Show volume data
                if 'volume' in df.columns:
                    print(f"Volume range: {df['volume'].min()} - {df['volume'].max()}")
                    print(f"Latest volume: {df['volume'].iloc[-1]}")
                
                # Show first few rows
                print("\n--- First 3 Rows ---")
                print(df.head(3).to_string())
                
                return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gold_functions_directly():
    """Test the gold functions directly"""
    print("\n=== Testing Gold Functions Directly ===")
    
    try:
        from tradingagents.dataflows.gold_utils import get_gold_price_data, get_gold_technical_analysis
        
        # Test price data function
        print("\n--- Testing get_gold_price_data ---")
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        price_data = get_gold_price_data("GOLD", start_date, end_date)
        print(f"Price data result length: {len(price_data)}")
        print(f"Contains $0.00: {'$0.00' in price_data}")
        print(f"Contains realistic prices: {'$4,' in price_data or '$3,' in price_data}")
        
        # Show first 500 characters
        print(f"Sample output: {price_data[:500]}...")
        
        # Test technical analysis function
        print("\n--- Testing get_gold_technical_analysis ---")
        tech_analysis = get_gold_technical_analysis("GOLD", end_date, 30)
        print(f"Tech analysis result length: {len(tech_analysis)}")
        print(f"Contains $0.00: {'$0.00' in tech_analysis}")
        print(f"Contains realistic prices: {'$4,' in tech_analysis or '$3,' in tech_analysis}")
        
        # Show first 500 characters
        print(f"Sample output: {tech_analysis[:500]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_toolkit_integration():
    """Test if the agent toolkit can access gold functions"""
    print("\n=== Testing Agent Toolkit Integration ===")
    
    try:
        from tradingagents.agents.utils.agent_utils import AgentUtils
        
        # Check if gold tools are available
        tools = AgentUtils.get_available_tools()
        gold_tools = [tool for tool in tools if 'gold' in tool.lower()]
        
        print(f"Total tools available: {len(tools)}")
        print(f"Gold-related tools: {gold_tools}")
        
        # Test get_gold_technical_analysis specifically
        if hasattr(AgentUtils, 'get_gold_technical_analysis'):
            print("✓ get_gold_technical_analysis tool found")
            
            # Try to call it
            end_date = datetime.now().strftime("%Y-%m-%d")
            result = AgentUtils.get_gold_technical_analysis("GOLD", end_date, 30)
            print(f"Tool result length: {len(result)}")
            print(f"Contains $0.00: {'$0.00' in result}")
            print(f"Contains realistic prices: {'$4,' in result or '$3,' in result}")
            
        else:
            print("❌ get_gold_technical_analysis tool NOT found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests to identify where the $0.00 issue occurs"""
    print("🔍 Gold Parsing Verification Test")
    print("=" * 50)
    
    # Test 1: Direct parsing
    parsing_ok = test_gold_parsing_with_real_data()
    
    # Test 2: Function calls
    functions_ok = test_gold_functions_directly()
    
    # Test 3: Agent toolkit
    toolkit_ok = test_agent_toolkit_integration()
    
    print("\n🎯 Test Results Summary:")
    print(f"Direct Parsing: {'✅ PASS' if parsing_ok else '❌ FAIL'}")
    print(f"Function Calls: {'✅ PASS' if functions_ok else '❌ FAIL'}")
    print(f"Agent Toolkit: {'✅ PASS' if toolkit_ok else '❌ FAIL'}")
    
    if parsing_ok and functions_ok and toolkit_ok:
        print("\n✅ All tests passed! The issue might be elsewhere.")
    else:
        print("\n❌ Some tests failed. This explains the $0.00 issue.")

if __name__ == "__main__":
    main()
