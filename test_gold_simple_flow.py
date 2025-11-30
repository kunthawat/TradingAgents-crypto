#!/usr/bin/env python3
"""
Simple test to identify where $0.00 values are introduced in the gold data flow
"""

import sys
import os
sys.path.insert(0, '.')
os.environ['PYTHONPATH'] = '.'

import json
from tradingagents.dataflows.gold_utils import GoldPriceAPI
from tradingagents.dataflows.interface import get_gold_market_analysis
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def test_gold_data_simple():
    """Test the gold data flow step by step"""
    
    print("=== SIMPLE GOLD DATA FLOW TEST ===")
    
    # Step 1: Test GoldPriceAPI directly
    print("\n1. Testing GoldPriceAPI...")
    try:
        gold_api = GoldPriceAPI()
        raw_data = gold_api.get_gold_history()
        print(f"✓ Raw data fetched: {type(raw_data)}")
        
        if isinstance(raw_data, dict) and 'history' in raw_data:
            history = raw_data['history']
            if history:
                first_entry = history[0]
                price = first_entry.get('close', 0)
                volume = first_entry.get('volume', 0)
                
                print(f"  First entry - Price: ${price}, Volume: {volume}")
                
                if price == 0:
                    print("  ❌ $0.00 PRICE IN RAW API DATA!")
                else:
                    print(f"  ✓ Raw API price is realistic: ${price}")
                
                if volume == 0:
                    print("  ❌ ZERO VOLUME IN RAW API DATA!")
                else:
                    print(f"  ✓ Raw API volume is: {volume}")
            else:
                print("  ❌ No history data in API response!")
        else:
            print(f"  ❌ Unexpected API response format: {type(raw_data)}")
            
    except Exception as e:
        print(f"  ❌ GoldPriceAPI failed: {e}")
        return False
    
    # Step 2: Test parse_gold_data
    print("\n2. Testing parse_gold_data...")
    try:
        parsed_df = gold_api.parse_gold_data(raw_data)
        print(f"✓ Data parsed: {type(parsed_df)}, shape: {parsed_df.shape}")
        
        if not parsed_df.empty:
            latest_price = parsed_df.iloc[-1]['close']
            latest_volume = parsed_df.iloc[-1]['volume']
            
            print(f"  Latest - Price: ${latest_price}, Volume: {latest_volume}")
            
            if latest_price == 0:
                print("  ❌ $0.00 PRICE IN PARSED DATA!")
            else:
                print(f"  ✓ Parsed price is realistic: ${latest_price}")
            
            if latest_volume == 0:
                print("  ❌ ZERO VOLUME IN PARSED DATA!")
            else:
                print(f"  ✓ Parsed volume is: {latest_volume}")
        else:
            print("  ❌ Parsed DataFrame is empty!")
            
    except Exception as e:
        print(f"  ❌ parse_gold_data failed: {e}")
        return False
    
    # Step 3: Test get_gold_market_analysis
    print("\n3. Testing get_gold_market_analysis...")
    try:
        analysis_result = get_gold_market_analysis('GOLD', '2025-11-30')
        print(f"✓ Market analysis returned: {len(analysis_result)} characters")
        
        # Check for $0.00 in the analysis
        if '$0.00' in analysis_result:
            print("  ❌ $0.00 FOUND IN MARKET ANALYSIS!")
            # Find the line with $0.00
            lines = analysis_result.split('\n')
            for line in lines:
                if '$0.00' in line:
                    print(f"    Problem line: {line.strip()}")
        else:
            print("  ✓ No $0.00 found in market analysis")
            
        # Check for realistic prices
        if '$4,' in analysis_result or '$3,' in analysis_result or '$2,' in analysis_result:
            print("  ✓ Realistic gold prices found in analysis")
        else:
            print("  ❌ No realistic gold prices found in analysis")
            
    except Exception as e:
        print(f"  ❌ get_gold_market_analysis failed: {e}")
        return False
    
    # Step 4: Test TradingAgentsGraph
    print("\n4. Testing TradingAgentsGraph...")
    try:
        config = DEFAULT_CONFIG.copy()
        config.update({
            'llm_provider': 'openai',
            'session_id': 'test_session',
            'language': 'english'
        })
        
        graph = TradingAgentsGraph(
            selected_analysts=['market'],
            debug=False,
            config=config
        )
        
        init_state = graph.propagator.create_initial_state('GOLD', '2025-11-30')
        
        if 'asset_data' in init_state:
            asset_data = init_state['asset_data']
            print(f"✓ Asset data keys: {list(asset_data.keys())}")
            
            # Check for price in asset data
            if 'current_price' in asset_data:
                price = asset_data['current_price']
                print(f"  Asset data price: ${price}")
                
                if price == 0:
                    print("  ❌ $0.00 PRICE IN ASSET DATA!")
                else:
                    print(f"  ✓ Asset data price is realistic: ${price}")
            
            # Check for volume in asset data
            if 'volume' in asset_data:
                volume = asset_data['volume']
                print(f"  Asset data volume: {volume}")
                
                if volume == 0:
                    print("  ❌ ZERO VOLUME IN ASSET DATA!")
                else:
                    print(f"  ✓ Asset data volume is: {volume}")
        else:
            print("  ❌ No asset_data in initial state!")
            
    except Exception as e:
        print(f"  ❌ TradingAgentsGraph failed: {e}")
        return False
    
    print("\n=== TEST COMPLETE ===")
    return True

def analyze_volume_values():
    """Analyze what the volume values represent"""
    print("\n=== VOLUME ANALYSIS ===")
    
    try:
        gold_api = GoldPriceAPI()
        raw_data = gold_api.get_gold_history()
        
        if 'history' in raw_data:
            print("Raw volume values from API:")
            for i, entry in enumerate(raw_data['history'][:10]):
                date = entry.get('date', 'N/A')
                volume = entry.get('volume', 'N/A')
                close = entry.get('close', 'N/A')
                print(f"  {date}: Close=${close}, Volume={volume}")
        
        parsed_df = gold_api.parse_gold_data(raw_data)
        if not parsed_df.empty:
            print("\nParsed volume values:")
            for i, (_, row) in enumerate(parsed_df.head(10).iterrows()):
                date = row['date'].strftime('%Y-%m-%d')
                volume = row['volume']
                close = row['close']
                print(f"  {date}: Close=${close}, Volume={volume}")
        
        print("\nVolume Analysis:")
        print("- Gold volume typically represents trading volume in ounces or contracts")
        print("- Small volumes (like 9, 22) could indicate:")
        print("  * Data from a specific exchange or time period")
        print("  * Contract-based trading (futures)")
        print("  * Limited liquidity in the data source")
        print("- For gold spot trading, volumes are usually much larger")
        
    except Exception as e:
        print(f"Volume analysis failed: {e}")

if __name__ == "__main__":
    success = test_gold_data_simple()
    analyze_volume_values()
    
    if success:
        print("\n✅ All tests completed successfully")
    else:
        print("\n❌ Some tests failed")
