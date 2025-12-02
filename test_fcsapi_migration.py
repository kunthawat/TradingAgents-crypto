#!/usr/bin/env python3
"""
Test script to verify FCSAPI migration from RapidAPI
"""

import os
import sys
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.gold_utils import GoldPriceAPI, GoldPriceAPIError

def test_fcsapi_connection():
    """Test basic FCSAPI connection and authentication"""
    print("🔍 Testing FCSAPI connection...")
    
    try:
        api = GoldPriceAPI()
        print(f"✅ API initialized successfully")
        print(f"📊 Base URL: {api.base_url}")
        print(f"🔑 API Key: {'✓ Set' if api.api_key else '✗ Missing'}")
        
        # Test getting the 300-candle dataset
        fcsapi_data = api._get_fcsapi_data()
        print(f"✅ Successfully retrieved FCSAPI data")
        print(f"📈 Response status: {fcsapi_data.get('status')}")
        print(f"📊 Response code: {fcsapi_data.get('code')}")
        print(f"📅 Candle count: {len(fcsapi_data.get('response', {}))}")
        
        return True
        
    except GoldPriceAPIError as e:
        print(f"❌ FCSAPI Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_current_price():
    """Test getting current gold price"""
    print("\n🔍 Testing current gold price...")
    
    try:
        api = GoldPriceAPI()
        current_price = api.get_current_gold_price()
        
        print(f"✅ Current price retrieved successfully")
        print(f"💰 Price: ${current_price['data']['price']:,.2f}")
        print(f"📈 Open: ${current_price['data']['open']:,.2f}")
        print(f"📊 High: ${current_price['data']['high']:,.2f}")
        print(f"📉 Low: ${current_price['data']['low']:,.2f}")
        print(f"🕐 Timestamp: {current_price['data']['datetime']}")
        
        return True
        
    except GoldPriceAPIError as e:
        print(f"❌ Current price error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_historical_data():
    """Test getting historical gold data"""
    print("\n🔍 Testing historical gold data...")
    
    try:
        api = GoldPriceAPI()
        
        # Test last 30 days
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        print(f"📅 Requesting data from {start_date} to {end_date}")
        
        history = api.get_gold_history(start_date, end_date)
        
        print(f"✅ Historical data retrieved successfully")
        print(f"📊 Status: {history['status']}")
        print(f"📈 Candles returned: {history['date_range']['actual_candles']}")
        print(f"📅 Requested range: {history['date_range']['start_date']} to {history['date_range']['end_date']}")
        
        return True
        
    except GoldPriceAPIError as e:
        print(f"❌ Historical data error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_data_parsing():
    """Test data parsing to DataFrame"""
    print("\n🔍 Testing data parsing...")
    
    try:
        api = GoldPriceAPI()
        
        # Get historical data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        history = api.get_gold_history(start_date, end_date)
        df = api.parse_gold_data(history)
        
        print(f"✅ Data parsed successfully")
        print(f"📊 DataFrame shape: {df.shape}")
        print(f"📈 Columns: {list(df.columns)}")
        
        if not df.empty:
            latest = df.iloc[-1]
            print(f"💰 Latest close: ${latest['close']:,.2f}")
            print(f"📊 Latest volume: {latest['volume']:,.0f}")
            print(f"📈 Price range: ${latest['price_range']:,.2f}")
            print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
        
        return True
        
    except GoldPriceAPIError as e:
        print(f"❌ Data parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_technical_indicators():
    """Test technical indicators calculation"""
    print("\n🔍 Testing technical indicators...")
    
    try:
        api = GoldPriceAPI()
        
        # Get and parse data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=50)).strftime("%Y-%m-%d")  # Need 50 days for SMA_50
        
        history = api.get_gold_history(start_date, end_date)
        df = api.parse_gold_data(history)
        df = api.calculate_technical_indicators(df)
        
        print(f"✅ Technical indicators calculated successfully")
        print(f"📊 DataFrame with indicators shape: {df.shape}")
        
        if not df.empty and len(df) >= 50:
            latest = df.iloc[-1]
            print(f"📈 RSI: {latest['rsi']:.1f}")
            print(f"📊 MACD: {latest['macd']:+.2f}")
            print(f"📈 SMA 20: ${latest['sma_20']:,.2f}")
            print(f"📊 SMA 50: ${latest['sma_50']:,.2f}")
            print(f"🎯 BB Position: {latest['bb_position']:.2f}")
        
        return True
        
    except GoldPriceAPIError as e:
        print(f"❌ Technical indicators error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_caching():
    """Test caching mechanism"""
    print("\n🔍 Testing caching mechanism...")
    
    try:
        api = GoldPriceAPI()
        
        # First request - should hit API
        print("📡 First request (should hit API)...")
        start_time = datetime.now()
        fcsapi_data1 = api._get_fcsapi_data()
        first_request_time = (datetime.now() - start_time).total_seconds()
        
        # Second request - should use cache
        print("📋 Second request (should use cache)...")
        start_time = datetime.now()
        fcsapi_data2 = api._get_fcsapi_data()
        second_request_time = (datetime.now() - start_time).total_seconds()
        
        print(f"⏱️  First request time: {first_request_time:.2f}s")
        print(f"⚡ Second request time: {second_request_time:.2f}s")
        print(f"🚀 Speedup: {first_request_time/second_request_time:.1f}x")
        
        # Verify data is the same
        if fcsapi_data1 == fcsapi_data2:
            print("✅ Caching working correctly - identical data returned")
        else:
            print("❌ Caching issue - different data returned")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Caching test error: {e}")
        return False

def test_date_filtering():
    """Test date filtering functionality"""
    print("\n🔍 Testing date filtering...")
    
    try:
        api = GoldPriceAPI()
        
        # Test different date ranges
        test_cases = [
            ("Last 7 days", 7),
            ("Last 30 days", 30),
            ("Last 90 days", 90),
        ]
        
        for description, days in test_cases:
            print(f"📅 Testing {description}...")
            
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            try:
                history = api.get_gold_history(start_date, end_date)
                df = api.parse_gold_data(history)
                
                print(f"   ✅ {description}: {len(df)} candles retrieved")
                
            except GoldPriceAPIError as e:
                if "older than available data" in str(e):
                    print(f"   ⚠️  {description}: {e}")
                else:
                    print(f"   ❌ {description}: {e}")
                    return False
        
        return True
        
    except Exception as e:
        print(f"❌ Date filtering test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting FCSAPI Migration Tests")
    print("=" * 50)
    
    # Check environment variable
    if not os.getenv("GOLDAPI_KEY"):
        print("❌ GOLDAPI_KEY environment variable not set!")
        print("Please set your FCSAPI key in the .env file:")
        print("GOLDAPI_KEY=your_fcsapi_key_here")
        return False
    
    tests = [
        ("FCSAPI Connection", test_fcsapi_connection),
        ("Current Price", test_current_price),
        ("Historical Data", test_historical_data),
        ("Data Parsing", test_data_parsing),
        ("Technical Indicators", test_technical_indicators),
        ("Caching", test_caching),
        ("Date Filtering", test_date_filtering),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! FCSAPI migration successful!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
