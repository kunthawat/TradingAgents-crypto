#!/usr/bin/env python3
"""
Test script to verify the OpenAI API fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.interface import (
    get_stock_news_openai,
    get_global_news_openai,
    get_fundamentals_openai
)
from tradingagents.dataflows.config import get_config

def test_api_functions():
    """Test the fixed API functions"""
    
    print("Testing OpenAI API fixes...")
    print("=" * 50)
    
    # Get config to verify setup
    config = get_config()
    print(f"Backend URL: {config['backend_url']}")
    print(f"Model: {config['quick_think_llm']}")
    print()
    
    # Test each function
    test_cases = [
        ("Stock News", lambda: get_stock_news_openai("AAPL", "2024-01-15")),
        ("Global News", lambda: get_global_news_openai("2024-01-15")),
        ("Fundamentals", lambda: get_fundamentals_openai("AAPL", "2024-01-15"))
    ]
    
    for test_name, test_func in test_cases:
        print(f"Testing {test_name}...")
        try:
            result = test_func()
            if result and "Failed" not in result:
                print(f"✅ {test_name} - SUCCESS")
                print(f"Response length: {len(result)} characters")
                print(f"First 100 chars: {result[:100]}...")
            else:
                print(f"❌ {test_name} - FAILED")
                print(f"Result: {result}")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
        print("-" * 30)
    
    print("Test completed!")

if __name__ == "__main__":
    test_api_functions()
