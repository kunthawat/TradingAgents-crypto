#!/usr/bin/env python3
"""
Detailed test to check what's in the TradingAgentsGraph initial state
"""

import sys
import os
sys.path.insert(0, '.')
os.environ['PYTHONPATH'] = '.'

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def test_initial_state():
    """Test what's in the initial state"""
    
    print("=== DETAILED INITIAL STATE TEST ===")
    
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
        
        print(f"✓ Initial state created successfully")
        print(f"  State type: {type(init_state)}")
        print(f"  State keys: {list(init_state.keys())}")
        
        # Check each key in detail
        for key, value in init_state.items():
            print(f"\n  {key}:")
            if isinstance(value, dict):
                print(f"    Type: dict, Keys: {list(value.keys())}")
                # Show some details for important keys
                if key == 'messages' and value:
                    print(f"    Messages count: {len(value)}")
                    if len(value) > 0:
                        print(f"    First message type: {type(value[0])}")
                elif key == 'asset_data':
                    print(f"    Asset data content: {value}")
                else:
                    print(f"    Sample value: {str(value)[:100]}...")
            else:
                print(f"    Type: {type(value)}, Value: {str(value)[:100]}...")
        
        # Specifically check if there's any gold data
        print(f"\n=== GOLD DATA SEARCH ===")
        gold_found = False
        for key, value in init_state.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if 'gold' in str(subvalue).lower() or '4191' in str(subvalue):
                        print(f"  Found gold data in {key}.{subkey}: {subvalue}")
                        gold_found = True
            elif 'gold' in str(value).lower() or '4191' in str(value):
                print(f"  Found gold data in {key}: {value}")
                gold_found = True
        
        if not gold_found:
            print("  ❌ No gold data found in initial state!")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_initial_state()
    
    if success:
        print("\n✅ Initial state test completed")
    else:
        print("\n❌ Initial state test failed")
