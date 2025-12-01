#!/usr/bin/env python3
"""
Test the market analyst tool selection and binding
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.agents.analysts.market_analyst import create_market_analyst, _detect_asset_type
from tradingagents.agents.utils.agent_utils import Toolkit

def test_market_analyst_tool_binding():
    """Test the market analyst tool binding process"""
    print("🧪 Testing Market Analyst Tool Binding")
    print("=" * 50)
    
    # Create toolkit
    toolkit = Toolkit()
    
    # Test asset detection
    asset_type = _detect_asset_type('GOLD')
    print(f"✅ Asset detection: GOLD -> {asset_type}")
    
    # Test tool selection like in market analyst
    if asset_type == 'gold':
        tools = [toolkit.get_gold_price_history, toolkit.get_gold_technical_analysis]
        print(f"✅ Selected gold tools: {[tool.name for tool in tools]}")
    
    # Test tool binding (this is where the error occurs)
    try:
        # Create a mock LLM for testing (we won't actually call it)
        class MockLLM:
            def bind_tools(self, tools):
                print(f"✅ Successfully bound {len(tools)} tools")
                print(f"   Tool names: {[tool.name for tool in tools]}")
                return self
        
        mock_llm = MockLLM()
        bound_llm = mock_llm.bind_tools(tools)
        print("✅ Tool binding successful")
        
    except Exception as e:
        print(f"❌ Tool binding failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test individual tool access
    print("\n🔍 Testing individual tool access:")
    for tool in tools:
        try:
            print(f"  - {tool.name}: {type(tool)}")
            # Test if the tool has the required attributes
            print(f"    name: {getattr(tool, 'name', 'No name')}")
            print(f"    description: {getattr(tool, 'description', 'No description')[:50]}...")
            print(f"    args: {getattr(tool, 'args', 'No args')}")
        except Exception as e:
            print(f"  - Error accessing {tool}: {e}")

def test_working_stock_tools():
    """Test how stock tools work for comparison"""
    print("\n🧪 Testing Stock Tools (Working Example)")
    print("=" * 50)
    
    toolkit = Toolkit()
    
    # Test stock tools (these work)
    if toolkit.config.get("online_tools", False):
        tools = [toolkit.get_YFin_data_online, toolkit.get_stockstats_indicators_report_online]
    else:
        tools = [toolkit.get_YFin_data, toolkit.get_stockstats_indicators_report]
    
    print(f"✅ Selected stock tools: {[tool.name for tool in tools]}")
    
    # Test tool binding
    try:
        class MockLLM:
            def bind_tools(self, tools):
                print(f"✅ Successfully bound {len(tools)} stock tools")
                return self
        
        mock_llm = MockLLM()
        bound_llm = mock_llm.bind_tools(tools)
        print("✅ Stock tool binding successful")
        
    except Exception as e:
        print(f"❌ Stock tool binding failed: {e}")

if __name__ == "__main__":
    test_market_analyst_tool_binding()
    test_working_stock_tools()
