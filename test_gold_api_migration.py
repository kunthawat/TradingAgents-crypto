#!/usr/bin/env python3
"""
Test script to verify FCSAPI migration works correctly
"""

import os
import sys
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.gold_utils import GoldPriceAPI, GoldPriceAPIError

def test_current_price():
    """Test current gold price endpoint"""
    print("🧪 Testing current gold price endpoint...")
    
    try:
        api = GoldPriceAPI()
        response = api.get_current_gold_price()
        
        print(f"✅ Current price response: {response}")
        
        # Verify response structure
        if isinstance(response, dict) and 'price' in response:
            print(f"✅ Current gold price: ${response['price']:.2f}")
            return True
        else:
            print(f"❌ Unexpected response format: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing current price: {e}")
        return False

def test_historical_data():
    """Test historical gold data endpoint"""
    print("\n🧪 Testing historical gold data endpoint...")
    
    try:
        api = GoldPriceAPI()
        
        # Test with last 7 days
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        response = api.get_gold_history(start_date, end_date)
        
        print(f"✅ Historical data response type: {type(response)}")
        print(f"✅ Historical data length: {len(response) if isinstance(response, list) else 'N/A'}")
        
        if isinstance(response, list) and len(response) > 0:
            print(f"✅ Sample data point: {response[0]}")
            return True
        else:
            print(f"❌ Unexpected response format: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing historical data: {e}")
        return False

def test_data_parsing():
    """Test data parsing functionality"""
    print("\n🧪 Testing data parsing...")
    
    try:
        api = GoldPriceAPI()
        
        # Test parsing current price response
        current_response = api.get_current_gold_price()
        df_current = api.parse_gold_data(current_response)
        
        print(f"✅ Parsed current price DataFrame shape: {df_current.shape}")
        print(f"✅ Columns: {list(df_current.columns)}")
        
        # Test parsing historical response
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        
        hist_response = api.get_gold_history(start_date, end_date)
        df_hist = api.parse_gold_data(hist_response)
        
        print(f"✅ Parsed historical DataFrame shape: {df_hist.shape}")
        print(f"✅ Sample row:\n{df_hist.head(1).to_string()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing data parsing: {e}")
        return False

def test_technical_indicators():
    """Test technical indicators calculation"""
    print("\n🧪 Testing technical indicators...")
    
    try:
        api = GoldPriceAPI()
        
        # Get some data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        
        response = api.get_gold_history(start_date, end_date)
        df = api.parse_gold_data(response)
        
        # Calculate indicators
        df_with_indicators = api.calculate_technical_indicators(df)
        
        print(f"✅ DataFrame with indicators shape: {df_with_indicators.shape}")
        print(f"✅ Indicator columns: {[col for col in df_with_indicators.columns if col in ['sma_10', 'rsi', 'macd']]}")
        
        # Check if indicators were calculated
        if 'sma_10' in df_with_indicators.columns:
            print(f"✅ SMA_10 calculated: {df_with_indicators['sma_10'].iloc[-1]:.2f}")
        if 'rsi' in df_with_indicators.columns:
            print(f"✅ RSI calculated: {df_with_indicators['rsi'].iloc[-1]:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing technical indicators: {e}")
        return False

def test_caching():
    """Test caching functionality"""
    print("\n🧪 Testing caching...")
    
    try:
        api = GoldPriceAPI()
        
        # First request
        print("Making first request...")
        start_time = datetime.now()
        response1 = api.get_current_gold_price()
        first_request_time = (datetime.now() - start_time).total_seconds()
        
        # Second request (should use cache)
        print("Making second request (should use cache)...")
        start_time = datetime.now()
        response2 = api.get_current_gold_price()
        second_request_time = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ First request time: {first_request_time:.2f}s")
        print(f"✅ Second request time: {second_request_time:.2f}s")
        
        if second_request_time < first_request_time:
            print("✅ Caching appears to be working (second request faster)")
        else:
            print("⚠️  Caching may not be working as expected")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing caching: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🧪 Testing error handling...")
    
    try:
        # Test with invalid API key
        os.environ['GOLDAPI_KEY'] = 'invalid_key'
        api_invalid = GoldPriceAPI()
        
        try:
            api_invalid.get_current_gold_price()
            print("❌ Should have failed with invalid API key")
            return False
        except GoldPriceAPIError as e:
            print(f"✅ Correctly caught API error: {e}")
        
        # Restore valid API key
        os.environ.pop('GOLDAPI_KEY', None)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing error handling: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Gold API Migration Tests")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv('GOLDAPI_KEY'):
        print("❌ GOLDAPI_KEY environment variable not found!")
        print("Please set GOLDAPI_KEY environment variable to run tests.")
        return False
    
    tests = [
        test_current_price,
        test_historical_data,
        test_data_parsing,
        test_technical_indicators,
        test_caching,
        test_error_handling
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gold API migration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
