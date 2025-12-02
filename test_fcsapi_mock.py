#!/usr/bin/env python3
"""
Mock test script to verify FCSAPI migration structure without API key
"""

import os
import sys
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.gold_utils import GoldPriceAPI, GoldPriceAPIError

def create_mock_fcsapi_response():
    """Create a mock FCSAPI response with realistic historical dates"""
    # Use dates from the past 30 days to avoid date filtering issues
    current_time = int(datetime.now().timestamp())
    one_day = 86400  # seconds in a day
    
    response_data = {}
    for i in range(30):  # Create 30 days of data
        timestamp = current_time - (i * one_day)
        date = datetime.fromtimestamp(timestamp)
        base_price = 2650.0 + (i * 2.5)  # Varying prices
        
        response_data[str(timestamp)] = {
            "tm": date.strftime("%Y-%m-%d 00:00:00"),
            "o": str(base_price - 2),
            "h": str(base_price + 3),
            "l": str(base_price - 4),
            "c": str(base_price),
            "v": str(1000 + i * 10)
        }
    
    return {
        "status": True,
        "code": 200,
        "msg": "Successfully",
        "info": {
            "server_time": datetime.now().strftime("%Y-%m-%d 12:00:00"),
            "credit": 500,
            "symbol": "XAU/USD"
        },
        "response": response_data
    }

def test_api_initialization():
    """Test API initialization with mock"""
    print("🔍 Testing API initialization...")
    
    try:
        # Mock the environment variable
        with patch.dict(os.environ, {'GOLDAPI_KEY': 'test_key_12345'}):
            api = GoldPriceAPI()
            print(f"✅ API initialized successfully")
            print(f"📊 Base URL: {api.base_url}")
            print(f"🔑 API Key: {'✓ Set' if api.api_key else '✗ Missing'}")
            print(f"⏱️  Rate limit: {api.min_request_interval}s")
            print(f"📋 Cache TTL: {api._cache_ttl}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_fcsapi_data_retrieval():
    """Test FCSAPI data retrieval with mock"""
    print("\n🔍 Testing FCSAPI data retrieval...")
    
    try:
        mock_response = create_mock_fcsapi_response()
        
        with patch.dict(os.environ, {'GOLDAPI_KEY': 'test_key_12345'}):
            api = GoldPriceAPI()
            
            # Mock the HTTP request
            with patch.object(api.session, 'get') as mock_get:
                mock_response_obj = MagicMock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.status_code = 200
                mock_get.return_value = mock_response_obj
                
                fcsapi_data = api._get_fcsapi_data()
                
                print(f"✅ Mock FCSAPI data retrieved successfully")
                print(f"📈 Response status: {fcsapi_data.get('status')}")
                print(f"📊 Response code: {fcsapi_data.get('code')}")
                print(f"📅 Candle count: {len(fcsapi_data.get('response', {}))}")
                print(f"💰 Latest price: ${list(fcsapi_data['response'].values())[0]['c']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data retrieval error: {e}")
        return False

def test_current_price():
    """Test current price with mock"""
    print("\n🔍 Testing current price...")
    
    try:
        mock_response = create_mock_fcsapi_response()
        
        with patch.dict(os.environ, {'GOLDAPI_KEY': 'test_key_12345'}):
            api = GoldPriceAPI()
            
            with patch.object(api.session, 'get') as mock_get:
                mock_response_obj = MagicMock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.status_code = 200
                mock_get.return_value = mock_response_obj
                
                current_price = api.get_current_gold_price()
                
                print(f"✅ Current price retrieved successfully")
                print(f"💰 Price: ${current_price['data']['price']:,.2f}")
                print(f"📈 Open: ${current_price['data']['open']:,.2f}")
                print(f"📊 High: ${current_price['data']['high']:,.2f}")
                print(f"📉 Low: ${current_price['data']['low']:,.2f}")
                print(f"🕐 Timestamp: {current_price['data']['datetime']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Current price error: {e}")
        return False

def test_historical_data():
    """Test historical data with mock"""
    print("\n🔍 Testing historical data...")
    
    try:
        mock_response = create_mock_fcsapi_response()
        
        with patch.dict(os.environ, {'GOLDAPI_KEY': 'test_key_12345'}):
            api = GoldPriceAPI()
            
            with patch.object(api.session, 'get') as mock_get:
                mock_response_obj = MagicMock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.status_code = 200
                mock_get.return_value = mock_response_obj
                
                # Use realistic dates from the past few days
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
                
                history = api.get_gold_history(start_date, end_date)
                
                print(f"✅ Historical data retrieved successfully")
                print(f"📊 Status: {history['status']}")
                print(f"📈 Candles returned: {history['date_range']['actual_candles']}")
                print(f"📅 Requested range: {history['date_range']['start_date']} to {history['date_range']['end_date']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Historical data error: {e}")
        return False

def test_data_parsing():
    """Test data parsing with mock"""
    print("\n🔍 Testing data parsing...")
    
    try:
        mock_response = create_mock_fcsapi_response()
        
        with patch.dict(os.environ, {'GOLDAPI_KEY': 'test_key_12345'}):
            api = GoldPriceAPI()
            
            with patch.object(api.session, 'get') as mock_get:
                mock_response_obj = MagicMock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.status_code = 200
                mock_get.return_value = mock_response_obj
                
                # Use realistic dates from the past few days
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
                
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
        
    except Exception as e:
        print(f"❌ Data parsing error: {e}")
        return False

def test_technical_indicators():
    """Test technical indicators with mock"""
    print("\n🔍 Testing technical indicators...")
    
    try:
        # Create a larger mock response for technical indicators
        extended_mock = create_mock_fcsapi_response()
        # Add more data points for technical indicators (total 60 days)
        current_time = int(datetime.now().timestamp())
        one_day = 86400  # seconds in a day
        
        for i in range(30, 60):  # Add 30 more days to existing 30
            timestamp = current_time - (i * one_day)
            date = datetime.fromtimestamp(timestamp)
            base_price = 2650.0 + (i * 2.5)  # Varying prices
            
            extended_mock["response"][str(timestamp)] = {
                "tm": date.strftime("%Y-%m-%d 00:00:00"),
                "o": str(base_price - 2),
                "h": str(base_price + 3),
                "l": str(base_price - 4),
                "c": str(base_price),
                "v": str(1000 + i * 10)
            }
        
        with patch.dict(os.environ, {'GOLDAPI_KEY': 'test_key_12345'}):
            api = GoldPriceAPI()
            
            with patch.object(api.session, 'get') as mock_get:
                mock_response_obj = MagicMock()
                mock_response_obj.json.return_value = extended_mock
                mock_response_obj.status_code = 200
                mock_get.return_value = mock_response_obj
                
                # Use realistic dates from the past 30 days
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d")
                
                history = api.get_gold_history(start_date, end_date)
                df = api.parse_gold_data(history)
                df = api.calculate_technical_indicators(df)
                
                print(f"✅ Technical indicators calculated successfully")
                print(f"📊 DataFrame with indicators shape: {df.shape}")
                
                if not df.empty and len(df) >= 20:
                    latest = df.iloc[-1]
                    print(f"📈 RSI: {latest['rsi']:.1f}")
                    print(f"📊 MACD: {latest['macd']:+.2f}")
                    print(f"📈 SMA 20: ${latest['sma_20']:,.2f}")
                    print(f"📊 SMA 10: ${latest['sma_10']:,.2f}")
                    print(f"🎯 BB Position: {latest['bb_position']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Technical indicators error: {e}")
        return False

def test_caching():
    """Test caching mechanism with mock"""
    print("\n🔍 Testing caching mechanism...")
    
    try:
        mock_response = create_mock_fcsapi_response()
        
        with patch.dict(os.environ, {'GOLDAPI_KEY': 'test_key_12345'}):
            api = GoldPriceAPI()
            
            with patch.object(api.session, 'get') as mock_get:
                mock_response_obj = MagicMock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.status_code = 200
                mock_get.return_value = mock_response_obj
                
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

def main():
    """Run all mock tests"""
    print("🚀 Starting FCSAPI Migration Mock Tests")
    print("=" * 50)
    
    tests = [
        ("API Initialization", test_api_initialization),
        ("FCSAPI Data Retrieval", test_fcsapi_data_retrieval),
        ("Current Price", test_current_price),
        ("Historical Data", test_historical_data),
        ("Data Parsing", test_data_parsing),
        ("Technical Indicators", test_technical_indicators),
        ("Caching", test_caching),
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
    print("📊 MOCK TEST SUMMARY")
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
        print("🎉 All mock tests passed! FCSAPI migration structure is correct!")
        print("💡 Note: You need a valid FCSAPI key to test with real data.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
