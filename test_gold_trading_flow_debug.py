#!/usr/bin/env python3
"""
Test the actual gold trading flow to find where the error occurs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.agents.analysts.market_analyst import create_market_analyst
from tradingagents.dataflows.config import get_config

def test_gold_trading_flow():
    """Test the actual gold trading flow"""
    print("🧪 Testing Gold Trading Flow")
    print("=" * 50)
    
    try:
        # Setup
        config = get_config()
        toolkit = Toolkit()
        
        # Create a mock LLM
        class MockLLM:
            def bind_tools(self, tools):
                print(f"✅ LLM bound {len(tools)} tools: {[tool.name for tool in tools]}")
                return self
            
            def invoke(self, messages):
                print("✅ LLM invoked successfully")
                # Return a mock result
                class MockResult:
                    content = "Mock market analysis"
                    tool_calls = []
                return MockResult()
        
        mock_llm = MockLLM()
        
        # Create market analyst
        market_analyst = create_market_analyst(mock_llm, toolkit)
        print("✅ Market analyst created successfully")
        
        # Test state like in the actual flow
        test_state = {
            "trade_date": "2025-12-01",
            "company_of_interest": "GOLD",
            "messages": []
        }
        
        print(f"✅ Test state: {test_state}")
        
        # Call the market analyst
        result = market_analyst(test_state)
        print("✅ Market analyst executed successfully")
        print(f"   Result keys: {list(result.keys())}")
        
    except Exception as e:
        print(f"❌ Error in gold trading flow: {e}")
        import traceback
        traceback.print_exc()

def test_with_real_llm():
    """Test with a real LLM if available"""
    print("\n🧪 Testing with Real LLM (if available)")
    print("=" * 50)
    
    try:
        from langchain_openai import ChatOpenAI
        
        # Check if we have API key
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  No OPENAI_API_KEY found, skipping real LLM test")
            return
        
        # Setup
        config = get_config()
        toolkit = Toolkit()
        
        # Create real LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        # Create market analyst
        market_analyst = create_market_analyst(llm, toolkit)
        print("✅ Market analyst created with real LLM")
        
        # Test state
        test_state = {
            "trade_date": "2025-12-01",
            "company_of_interest": "GOLD",
            "messages": []
        }
        
        # Call the market analyst
        result = market_analyst(test_state)
        print("✅ Market analyst executed with real LLM")
        print(f"   Result keys: {list(result.keys())}")
        
    except ImportError:
        print("⚠️  langchain_openai not available, skipping real LLM test")
    except Exception as e:
        print(f"❌ Error with real LLM: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gold_trading_flow()
    test_with_real_llm()
