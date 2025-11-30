#!/usr/bin/env python3
"""
Test complete GOLD → RapidAPI → real prices flow
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.interface import get_asset_data, detect_asset_type
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def test_asset_detection():
    """Test asset detection for GOLD symbols"""
    print("=== Testing Asset Detection ===")
    
    test_symbols = ['GOLD', 'XAU', 'BTC', 'ETH', 'AAPL']
    
    for symbol in test_symbols:
        asset_type = detect_asset_type(symbol)
        print(f"{symbol} → {asset_type}")
    
    print()

def test_gold_tools():
    """Test gold tools directly"""
    print("=== Testing Gold Tools Directly ===")
    
    toolkit = Toolkit()
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
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
        
        # Test gold news analysis
        print("Testing get_gold_news_analysis...")
        result = toolkit.get_gold_news_analysis("GOLD", curr_date, 3)
        print(f"✓ Gold news analysis result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
        # Test gold fundamentals
        print("Testing get_gold_fundamentals_analysis...")
        result = toolkit.get_gold_fundamentals_analysis("GOLD", curr_date)
        print(f"✓ Gold fundamentals result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
    except Exception as e:
        print(f"✗ Error testing gold tools: {e}")
        import traceback
        traceback.print_exc()
        print()

def test_interface_functions():
    """Test interface functions"""
    print("=== Testing Interface Functions ===")
    
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Test get_asset_data
        print("Testing get_asset_data for GOLD...")
        result = get_asset_data("GOLD", curr_date, 7)
        print(f"✓ Asset data result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
        # Test get_gold_market_analysis directly
        print("Testing get_gold_market_analysis directly...")
        result = get_gold_market_analysis("GOLD", curr_date)
        print(f"✓ Gold market analysis result length: {len(result)}")
        print(f"First 200 chars: {result[:200]}...")
        print()
        
    except Exception as e:
        print(f"✗ Error testing interface functions: {e}")
        import traceback
        traceback.print_exc()
        print()

def test_trading_graph():
    """Test trading graph with gold"""
    print("=== Testing Trading Graph with GOLD ===")
    
    try:
        # Create a minimal config
        config = DEFAULT_CONFIG.copy()
        config.update({
            'llm_provider': 'openai',
            'backend_url': 'https://api.openai.com/v1',
            'api_key': os.getenv('OPENAI_API_KEY', 'test-key'),
            'quick_think_llm': 'gpt-3.5-turbo',
            'deep_think_llm': 'gpt-4',
            'research_depth': 'quick',
            'language': 'english'
        })
        
        # Create graph with only market analyst for quick test
        graph = TradingAgentsGraph(
            selected_analysts=["market"],
            debug=True,
            config=config
        )
        
        print("✓ Trading graph created successfully")
        
        # Test tool nodes
        print("Testing tool nodes...")
        market_tools = graph.tool_nodes["market"].tools
        gold_tools = [tool for tool in market_tools if "gold" in tool.name.lower()]
        print(f"✓ Found {len(gold_tools)} gold tools in market node: {[tool.name for tool in gold_tools]}")
        
        social_tools = graph.tool_nodes["social"].tools
        gold_tools = [tool for tool in social_tools if "gold" in tool.name.lower()]
        print(f"✓ Found {len(gold_tools)} gold tools in social node: {[tool.name for tool in gold_tools]}")
        
        news_tools = graph.tool_nodes["news"].tools
        gold_tools = [tool for tool in news_tools if "gold" in tool.name.lower()]
        print(f"✓ Found {len(gold_tools)} gold tools in news node: {[tool.name for tool in gold_tools]}")
        
        fundamentals_tools = graph.tool_nodes["fundamentals"].tools
        gold_tools = [tool for tool in fundamentals_tools if "gold" in tool.name.lower()]
        print(f"✓ Found {len(gold_tools)} gold tools in fundamentals node: {[tool.name for tool in gold_tools]}")
        
        print()
        
    except Exception as e:
        print(f"✗ Error testing trading graph: {e}")
        import traceback
        traceback.print_exc()
        print()

def main():
    """Run all tests"""
    print("🧪 Testing Complete GOLD → RapidAPI → Real Prices Flow")
    print("=" * 60)
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
    test_asset_detection()
    test_gold_tools()
    test_interface_functions()
    test_trading_graph()
    
    print("🎉 Complete flow testing finished!")

if __name__ == "__main__":
    main()
