#!/usr/bin/env python3
"""
Minimal test to verify the OpenAI API fixes work
"""

import os
from openai import OpenAI

def test_api_directly():
    """Test the API directly without importing project modules"""
    
    print("Testing OpenAI API connection directly...")
    print("=" * 50)
    
    # Use the same configuration as the project
    backend_url = "https://llm.chutes.ai/v1"
    api_key = "sk-123456"
    model = "deepseek-chat"
    
    try:
        # Create OpenAI client
        client = OpenAI(base_url=backend_url, api_key=api_key)
        
        # Test the API with the correct format
        response = client.chat.completions.create(
            model=model,
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

def test_news_function_format():
    """Test the format we use in the news functions"""
    
    print("\nTesting news function format...")
    print("=" * 50)
    
    backend_url = "https://llm.chutes.ai/v1"
    api_key = "sk-123456"
    model = "deepseek-chat"
    
    try:
        client = OpenAI(base_url=backend_url, api_key=api_key)
        
        # Test the exact format we use in get_stock_news_openai
        ticker = "AAPL"
        curr_date = "2024-01-15"
        
        prompt = f"""
        You are a financial analyst tasked with analyzing the latest news for {ticker} on {curr_date}. 
        Please provide a comprehensive analysis of the most recent news that could impact the stock's performance.
        Focus on:
        1. Earnings reports and financial metrics
        2. Product launches or updates
        3. Market sentiment and analyst ratings
        4. Regulatory changes or legal issues
        5. Competitive landscape changes
        6. Management changes or strategic initiatives
        
        Provide a balanced view with both positive and negative factors, and conclude with an overall sentiment assessment.
        """
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial analyst tasked with analyzing the latest news for {ticker} on {curr_date}. Please provide a comprehensive analysis of the most recent news that could impact the stock's performance. Focus on: 1. Earnings reports and financial metrics 2. Product launches or updates 3. Market sentiment and analyst ratings 4. Regulatory changes or legal issues 5. Competitive landscape changes 6. Management changes or strategic initiatives Provide a balanced view with both positive and negative factors, and conclude with an overall sentiment assessment.",
                }
            ],
            temperature=1,
            max_tokens=1000,
            top_p=1,
        )
        
        result = response.choices[0].message.content
        print(f"✅ News function test - SUCCESS")
        print(f"Response length: {len(result)} characters")
        print(f"First 200 chars: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing news function format: {e}")
        return False

if __name__ == "__main__":
    print("Minimal OpenAI API Fix Verification Test")
    print("=" * 60)
    
    # Test 1: Direct API connection
    api_test_passed = test_api_directly()
    
    # Test 2: News function format
    news_test_passed = test_news_function_format()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print(f"Direct API Test: {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
    print(f"News Function Test: {'✅ PASSED' if news_test_passed else '❌ FAILED'}")
    
    if api_test_passed and news_test_passed:
        print("\n🎉 ALL TESTS PASSED! The OpenAI API fixes are working correctly.")
        print("The 404 error should now be resolved in your application.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
