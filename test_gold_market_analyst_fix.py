#!/usr/bin/env python3
"""
Test the gold market analyst fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.agents.analysts.market_analyst import _detect_asset_type
from tradingagents.agents.utils.agent_utils import Toolkit

def test_asset_detection():
    """Test asset type detection"""
    print("🧪 Testing Asset Type Detection")
    print("=" * 40)
    
    test_cases = [
        ('XAU', 'gold'),
        ('GOLD', 'gold'),
        ('XAUUSD', 'gold'),
        ('BTC', 'crypto'),
        ('ETH', 'crypto'),
        ('AAPL', 'stock'),
        ('GOOGL', 'stock'),
        ('UNKNOWN', 'stock'),
    ]
    
    for symbol, expected in test_cases:
        result = _detect_asset_type(symbol)
        status = "✅" if result == expected else "❌"
        print(f"{status} {symbol} -> {result} (expected: {expected})")
    
    print()

def test_gold_tools():
    """Test that gold tools are available in toolkit"""
    print("🧪 Testing Gold Tools Availability")
    print("=" * 40)
    
    toolkit = Toolkit()
    
    gold_tools = [
        'get_gold_price_history',
        'get_gold_technical_analysis',
        'get_gold_market_analysis',
        'get_gold_news_analysis',
        'get_gold_fundamentals_analysis'
    ]
    
    for tool_name in gold_tools:
        if hasattr(toolkit, tool_name):
            tool = getattr(toolkit, tool_name)
            print(f"✅ {tool_name} - Available")
            print(f"   Description: {tool.description[:100]}...")
        else:
            print(f"❌ {tool_name} - Missing")
    
    print()

def test_gold_tool_functionality():
    """Test actual gold tool functionality"""
    print("🧪 Testing Gold Tool Functionality")
    print("=" * 40)
    
    toolkit = Toolkit()
    
    try:
        # Test gold price history
        result = toolkit.get_gold_price_history('XAU', '2025-01-01', 30)
        if result and len(result) > 0:
            print("✅ get_gold_price_history - Working")
            print(f"   Result length: {len(result)} characters")
        else:
            print("❌ get_gold_price_history - Failed or empty result")
    except Exception as e:
        print(f"❌ get_gold_price_history - Error: {e}")
    
    try:
        # Test gold technical analysis
        result = toolkit.get_gold_technical_analysis('XAU', '2025-01-01', 30)
        if result and len(result) > 0:
            print("✅ get_gold_technical_analysis - Working")
            print(f"   Result length: {len(result)} characters")
        else:
            print("❌ get_gold_technical_analysis - Failed or empty result")
    except Exception as e:
        print(f"❌ get_gold_technical_analysis - Error: {e}")
    
    print()

def main():
    print("🔧 Gold Market Analyst Fix Verification")
    print("=" * 50)
    
    test_asset_detection()
    test_gold_tools()
    test_gold_tool_functionality()
    
    print("=" * 50)
    print("🎉 Gold market analyst fix verification complete!")

if __name__ == "__main__":
    main()
