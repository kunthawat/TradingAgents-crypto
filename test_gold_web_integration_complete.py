#!/usr/bin/env python3
"""
Complete test to identify where $0.00 values are introduced in the web application
"""

import sys
import os
sys.path.insert(0, '.')
os.environ['PYTHONPATH'] = '.'

import json
from tradingagents.dataflows.gold_utils import GoldPriceAPI
from tradingagents.dataflows.interface import DataInterface
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def test_gold_data_flow():
    """Test the complete gold data flow to identify where $0.00 values appear"""
    
    print("=== COMPLETE GOLD DATA FLOW TEST ===")
    
    # Step 1: Test raw gold data fetching
    print("\n1. Testing raw gold data fetching...")
    gold_api = GoldPriceAPI()
    
    try:
        raw_data = gold_api.get_gold_history()
        print(f"✓ Raw data fetched successfully")
        print(f"  Data type: {type(raw_data)}")
        
        if isinstance(raw_data, dict):
            print(f"  Keys: {list(raw_data.keys())}")
            if 'history' in raw_data:
                hist_data = raw_data['history']
                if hist_data:
                    first_entry = hist_data[0]
                    print(f"  First entry keys: {list(first_entry.keys())}")
                    print(f"  First entry price: {first_entry.get('close', 'N/A')}")
                    print(f"  First entry volume: {first_entry.get('volume', 'N/A')}")
                    
                    # Check for $0.00 values
                    if first_entry.get('close') == 0 or str(first_entry.get('close', '')).startswith('0.00'):
                        print("  ❌ $0.00 PRICE FOUND IN RAW DATA!")
                    else:
                        print("  ✓ Raw data has realistic prices")
                        
                    if first_entry.get('volume') == 0:
                        print("  ❌ ZERO VOLUME FOUND IN RAW DATA!")
                    else:
                        print(f"  ✓ Raw data has volume: {first_entry.get('volume')}")
                else:
                    print("  ❌ No historical data found!")
            else:
                print("  ❌ No 'history' key in raw data!")
        else:
            print(f"  ❌ Unexpected data type: {type(raw_data)}")
            
    except Exception as e:
        print(f"  ❌ Raw data fetch failed: {e}")
        return False
    
    # Step 2: Test parsed gold data
    print("\n2. Testing parsed gold data...")
    try:
        parsed_df = gold_api.parse_gold_data(raw_data)
        print(f"✓ Data parsed successfully")
        print(f"  Parsed data type: {type(parsed_df)}")
        
        if not parsed_df.empty:
            print(f"  DataFrame shape: {parsed_df.shape}")
            print(f"  Columns: {list(parsed_df.columns)}")
            
            # Check current price
            if not parsed_df.empty:
                current_price = parsed_df.iloc[-1]['close']
                print(f"  Current price: {current_price}")
                if current_price == 0 or str(current_price).startswith('0.00'):
                    print("  ❌ $0.00 CURRENT PRICE FOUND!")
                else:
                    print("  ✓ Current price is realistic")
                
                # Check volume
                current_volume = parsed_df.iloc[-1]['volume']
                print(f"  Current volume: {current_volume}")
                if current_volume == 0:
                    print("  ❌ ZERO VOLUME IN PARSED DATA!")
                else:
                    print("  ✓ Parsed volume is realistic")
        else:
            print("  ❌ Parsed DataFrame is empty!")
            
    except Exception as e:
        print(f"  ❌ Data parsing failed: {e}")
        return False
    
    # Step 3: Test DataInterface
    print("\n3. Testing DataInterface...")
    try:
        data_interface = DataInterface()
        gold_data = data_interface.get_asset_data('GOLD', days=30)
        print(f"✓ DataInterface returned data")
        print(f"  Data type: {type(gold_data)}")
        
        if isinstance(gold_data, dict):
            print(f"  Keys: {list(gold_data.keys())}")
            
            # Check price
            price = gold_data.get('current_price', 0)
            print(f"  Interface price: {price}")
            if price == 0 or str(price).startswith('0.00'):
                print("  ❌ $0.00 PRICE IN INTERFACE!")
            else:
                print("  ✓ Interface price is realistic")
                
            # Check volume
            volume = gold_data.get('volume', 0)
            print(f"  Interface volume: {volume}")
            if volume == 0:
                print("  ❌ ZERO VOLUME IN INTERFACE!")
            else:
                print("  ✓ Interface volume is realistic")
        else:
            print(f"  ❌ Unexpected interface data type: {type(gold_data)}")
            
    except Exception as e:
        print(f"  ❌ DataInterface failed: {e}")
        return False
    
    # Step 4: Test TradingAgentsGraph initialization
    print("\n4. Testing TradingAgentsGraph...")
    try:
        config = DEFAULT_CONFIG.copy()
        config.update({
            'llm_provider': 'openai',
            'session_id': 'test_session',
            'language': 'english'
        })
        
        graph = TradingAgentsGraph(
            selected_analysts=['Market Analyst'],
            debug=False,
            config=config
        )
        print("✓ TradingAgentsGraph initialized")
        
        # Test initial state creation
        init_state = graph.propagator.create_initial_state('GOLD', '2025-11-30')
        print("✓ Initial state created")
        
        # Check what data is in the initial state
        if 'asset_data' in init_state:
            asset_data = init_state['asset_data']
            print(f"  Asset data keys: {list(asset_data.keys())}")
            
            # Check price in asset data
            if 'current_price' in asset_data:
                price = asset_data['current_price']
                print(f"  State price: {price}")
                if price == 0 or str(price).startswith('0.00'):
                    print("  ❌ $0.00 PRICE IN INITIAL STATE!")
                else:
                    print("  ✓ State price is realistic")
            
            # Check volume in asset data
            if 'volume' in asset_data:
                volume = asset_data['volume']
                print(f"  State volume: {volume}")
                if volume == 0:
                    print("  ❌ ZERO VOLUME IN INITIAL STATE!")
                else:
                    print("  ✓ State volume is realistic")
        else:
            print("  ❌ No 'asset_data' in initial state!")
            
    except Exception as e:
        print(f"  ❌ TradingAgentsGraph failed: {e}")
        return False
    
    print("\n=== TEST COMPLETE ===")
    return True

def test_volume_values():
    """Specifically test volume values to understand what they represent"""
    print("\n=== VOLUME ANALYSIS ===")
    
    gold_api = GoldPriceAPI()
    
    try:
        raw_data = gold_api.get_gold_history()
        parsed_df = gold_api.parse_gold_data(raw_data)
        
        print("Raw volume values:")
        if 'history' in raw_data:
            for i, entry in enumerate(raw_data['history'][:5]):
                volume = entry.get('volume', 'N/A')
                print(f"  Day {i+1}: {volume}")
        
        print("\nParsed volume values:")
        if not parsed_df.empty:
            for i, (_, row) in enumerate(parsed_df.head(5).iterrows()):
                volume = row['volume']
                print(f"  Day {i+1}: {volume}")
        
        print("\nCurrent volume:")
        if not parsed_df.empty:
            current_volume = parsed_df.iloc[-1]['volume']
            print(f"  Current: {current_volume}")
        
        # Test DataInterface volume
        data_interface = DataInterface()
        interface_data = data_interface.get_asset_data('GOLD', days=5)
        interface_volume = interface_data.get('volume', 'N/A')
        print(f"  Interface: {interface_volume}")
        
    except Exception as e:
        print(f"Volume analysis failed: {e}")

if __name__ == "__main__":
    success = test_gold_data_flow()
    test_volume_values()
    
    if success:
        print("\n✅ All tests completed successfully")
    else:
        print("\n❌ Some tests failed")
