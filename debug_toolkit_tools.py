#!/usr/bin/env python3
"""
Debug script to check what tools are actually available in the toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.agents.utils.agent_utils import Toolkit

def check_available_tools():
    """Check what tools are actually available in the toolkit"""
    print("🔍 Checking Available Tools in Toolkit")
    print("=" * 50)
    
    toolkit = Toolkit()
    
    # Get all methods from the toolkit
    all_methods = [method for method in dir(toolkit) if not method.startswith('_')]
    
    print("All available methods:")
    for method in sorted(all_methods):
        print(f"  - {method}")
    
    print("\n" + "=" * 50)
    
    # Check specifically for gold tools
    gold_tools = [method for method in all_methods if 'gold' in method.lower()]
    print("Gold-specific tools:")
    for tool in gold_tools:
        print(f"  - {tool}")
    
    print("\n" + "=" * 50)
    
    # Check if the problematic tool exists
    if hasattr(toolkit, 'get_gold_technical_analysis'):
        print("✅ get_gold_technical_analysis is available")
        
        # Try to call it
        try:
            result = toolkit.get_gold_technical_analysis('XAU', '2025-12-01', 30)
            print(f"✅ Tool call successful, result length: {len(result)}")
            print(f"   Preview: {result[:200]}...")
        except Exception as e:
            print(f"❌ Tool call failed: {e}")
    else:
        print("❌ get_gold_technical_analysis is NOT available")
    
    # Check other gold tools
    other_gold_tools = ['get_gold_price_history', 'get_gold_market_analysis']
    for tool in other_gold_tools:
        if hasattr(toolkit, tool):
            print(f"✅ {tool} is available")
        else:
            print(f"❌ {tool} is NOT available")

if __name__ == "__main__":
    check_available_tools()
