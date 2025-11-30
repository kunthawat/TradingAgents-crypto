#!/usr/bin/env python3
"""
Test gold tools integration in trading graph
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gold_tools_in_toolkit():
    """Test that gold tools are properly added to Toolkit"""
    print("=== Testing Gold Tools in Toolkit ===")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        toolkit = Toolkit()
        
        # Check if gold tools exist
        gold_tools = [
            'get_gold_price_history',
            'get_gold_market_analysis', 
            'get_gold_news_analysis',
            'get_gold_fundamentals_analysis'
        ]
        
        for tool_name in gold_tools:
            if hasattr(toolkit, tool_name):
                tool_method = getattr(toolkit, tool_name)
                print(f"✓ {tool_name} - Found and callable")
            else:
                print(f"✗ {tool_name} - Missing")
        
        print()
        
    except Exception as e:
        print(f"✗ Error testing toolkit: {e}")
        import traceback
        traceback.print_exc()
        print()

def test_trading_graph_gold_tools():
    """Test that trading graph can access gold tools"""
    print("=== Testing Trading Graph Gold Tools ===")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Create a minimal config
        config = DEFAULT_CONFIG.copy()
        config.update({
            'llm_provider': 'openai',
            'backend_url': 'https://api.openai.com/v1',
            'api_key': 'test-key',
            'quick_think_llm': 'gpt-3.5-turbo',
            'deep_think_llm': 'gpt-4',
            'research_depth': 'quick',
            'language': 'english'
        })
        
        # Create graph with only market analyst for quick test
        graph = TradingAgentsGraph(
            selected_analysts=["market"],
            debug=False,
            config=config
        )
        
        print("✓ Trading graph created successfully")
        
        # Test tool nodes
        print("Testing tool nodes...")
        
        # Check market node
        market_tools = graph.tool_nodes["market"].tools
        gold_tools_in_market = [tool for tool in market_tools if "gold" in tool.name.lower()]
        print(f"✓ Market node has {len(gold_tools_in_market)} gold tools: {[tool.name for tool in gold_tools_in_market]}")
        
        # Check social node
        social_tools = graph.tool_nodes["social"].tools
        gold_tools_in_social = [tool for tool in social_tools if "gold" in tool.name.lower()]
        print(f"✓ Social node has {len(gold_tools_in_social)} gold tools: {[tool.name for tool in gold_tools_in_social]}")
        
        # Check news node
        news_tools = graph.tool_nodes["news"].tools
        gold_tools_in_news = [tool for tool in news_tools if "gold" in tool.name.lower()]
        print(f"✓ News node has {len(gold_tools_in_news)} gold tools: {[tool.name for tool in gold_tools_in_news]}")
        
        # Check fundamentals node
        fundamentals_tools = graph.tool_nodes["fundamentals"].tools
        gold_tools_in_fundamentals = [tool for tool in fundamentals_tools if "gold" in tool.name.lower()]
        print(f"✓ Fundamentals node has {len(gold_tools_in_fundamentals)} gold tools: {[tool.name for tool in gold_tools_in_fundamentals]}")
        
        print()
        
    except Exception as e:
        print(f"✗ Error testing trading graph: {e}")
        import traceback
        traceback.print_exc()
        print()

def test_gold_tool_functionality():
    """Test gold tool functionality directly"""
    print("=== Testing Gold Tool Functionality ===")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        toolkit = Toolkit()
        curr_date = datetime.now().strftime("%Y-%m-%d")
        
        # Test gold market analysis
        print("Testing get_gold_market_analysis...")
        try:
            result = toolkit.get_gold_market_analysis("GOLD", curr_date)
            print(f"✓ Gold market analysis works (length: {len(result)})")
        except Exception as e:
            print(f"✗ Gold market analysis failed: {e}")
        
        # Test gold price history
        print("Testing get_gold_price_history...")
        try:
            result = toolkit.get_gold_price_history("GOLD", curr_date, 7)
            print(f"✓ Gold price history works (length: {len(result)})")
        except Exception as e:
            print(f"✗ Gold price history failed: {e}")
        
        # Test gold news analysis
        print("Testing get_gold_news_analysis...")
        try:
            result = toolkit.get_gold_news_analysis("GOLD", curr_date, 3)
            print(f"✓ Gold news analysis works (length: {len(result)})")
        except Exception as e:
            print(f"✗ Gold news analysis failed: {e}")
        
        # Test gold fundamentals
        print("Testing get_gold_fundamentals_analysis...")
        try:
            result = toolkit.get_gold_fundamentals_analysis("GOLD", curr_date)
            print(f"✓ Gold fundamentals works (length: {len(result)})")
        except Exception as e:
            print(f"✗ Gold fundamentals failed: {e}")
        
        print()
        
    except Exception as e:
        print(f"✗ Error testing gold tool functionality: {e}")
        import traceback
        traceback.print_exc()
        print()

def main():
    """Run all integration tests"""
    print("🧪 Testing Gold Tools Integration")
    print("=" * 50)
    print()
    
    # Check environment
    print("=== Environment Check ===")
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    if rapidapi_key:
        print(f"✓ RAPIDAPI_KEY found (length: {len(rapidapi_key)})")
    else:
        print("⚠️  RAPIDAPI_KEY not found - some tests may fail")
    print()
    
    # Run tests
    test_gold_tools_in_toolkit()
    test_trading_graph_gold_tools()
    test_gold_tool_functionality()
    
    print("🎉 Gold tools integration testing finished!")

if __name__ == "__main__":
    main()
