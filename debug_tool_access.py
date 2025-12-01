#!/usr/bin/env python3
"""
Debug script to check how to properly access tools from the toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.agents.utils.agent_utils import Toolkit

def check_tool_access():
    """Check how to properly access tools from the toolkit"""
    print("🔍 Checking Tool Access Methods")
    print("=" * 50)
    
    toolkit = Toolkit()
    
    # Check how stock tools are accessed (these work)
    print("Stock tools access:")
    try:
        yfin_tool = toolkit.get_YFin_data
        print(f"  get_YFin_data type: {type(yfin_tool)}")
        print(f"  get_YFin_data name: {getattr(yfin_tool, 'name', 'No name attr')}")
    except Exception as e:
        print(f"  get_YFin_data error: {e}")
    
    try:
        stockstats_tool = toolkit.get_stockstats_indicators_report
        print(f"  get_stockstats_indicators_report type: {type(stockstats_tool)}")
        print(f"  get_stockstats_indicators_report name: {getattr(stockstats_tool, 'name', 'No name attr')}")
    except Exception as e:
        print(f"  get_stockstats_indicators_report error: {e}")
    
    print("\nGold tools access:")
    try:
        gold_price_tool = toolkit.get_gold_price_history
        print(f"  get_gold_price_history type: {type(gold_price_tool)}")
        print(f"  get_gold_price_history name: {getattr(gold_price_tool, 'name', 'No name attr')}")
    except Exception as e:
        print(f"  get_gold_price_history error: {e}")
    
    try:
        gold_tech_tool = toolkit.get_gold_technical_analysis
        print(f"  get_gold_technical_analysis type: {type(gold_tech_tool)}")
        print(f"  get_gold_technical_analysis name: {getattr(gold_tech_tool, 'name', 'No name attr')}")
    except Exception as e:
        print(f"  get_gold_technical_analysis error: {e}")
    
    print("\nCrypto tools access:")
    try:
        crypto_price_tool = toolkit.get_crypto_price_history
        print(f"  get_crypto_price_history type: {type(crypto_price_tool)}")
        print(f"  get_crypto_price_history name: {getattr(crypto_price_tool, 'name', 'No name attr')}")
    except Exception as e:
        print(f"  get_crypto_price_history error: {e}")

if __name__ == "__main__":
    check_tool_access()
