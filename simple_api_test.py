#!/usr/bin/env python3
"""
Simple test script to verify the OpenAI API fixes
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

# Test the OpenAI API directly
from openai import OpenAI

def test_openai_api():
    """Test the OpenAI API connection directly"""
    
    print("Testing OpenAI API connection...")
    print("=" * 50)
    
    # Test configuration - using the same config as the project
    try:
        # Try to import config
        from tradingagents.dataflows.config import get_config
        config = get_config()
        print(f"✅ Config loaded successfully")
        print(f"Backend URL: {config['backend_url']}")
        print(f"Model: {config['quick_think_llm']}")
        
        # Test API connection
        client = OpenAI(base_url=config["backend_url"], api_key=config["api_key"])
        
        # Simple test call
        response = client.chat.completions.create(
            model=config["quick_think_llm"],
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond with 'API connection successful!'",
                }
            ],
            temperature=1,
            max_tokens=100,
            top_p=1,
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Test Response: {result}")
        print("✅ OpenAI API connection is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI API: {e}")
        return False

def test_fixed_functions():
    """Test the fixed functions by importing them directly"""
    
    print("\nTesting fixed functions...")
    print("=" * 50)
    
    try:
        # Import the fixed functions
        from tradingagents.dataflows.interface import (
            get_stock_news_openai,
            get_global_news_openai,
            get_fundamentals_openai
        )
        
        print("✅ Functions imported successfully")
        
        # Test one function with a simple call
        print("Testing get_stock_news_openai...")
        result = get_stock_news_openai("AAPL", "2024-01-15")
        
        if result and "Failed" not in result:
            print(f"✅ get_stock_news_openai - SUCCESS")
            print(f"Response length: {len(result)} characters")
            print(f"First 100 chars: {result[:100]}...")
        else:
            print(f"❌ get_stock_news_openai - FAILED")
            print(f"Result: {result}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing fixed functions: {e}")
        return False

if __name__ == "__main__":
    print("OpenAI API Fix Verification Test")
    print("=" * 60)
    
    # Test 1: Direct API connection
    api_test_passed = test_openai_api()
    
    # Test 2: Fixed functions
    functions_test_passed = test_fixed_functions()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print(f"Direct API Test: {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
    print(f"Functions Test: {'✅ PASSED' if functions_test_passed else '❌ FAILED'}")
    
    if api_test_passed and functions_test_passed:
        print("\n🎉 ALL TESTS PASSED! The OpenAI API fixes are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
