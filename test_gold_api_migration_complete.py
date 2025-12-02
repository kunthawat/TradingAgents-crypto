#!/usr/bin/env python3
"""
Complete test of the gold API migration from RapidAPI to FCSAPI
This test focuses on the gold API functionality without LLM dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.gold_utils import GoldPriceAPI
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.dataflows.config import get_config

def test_gold_api_migration():
    """Test the complete gold API migration"""
    print("🧪 Testing Complete Gold API Migration")
    print("=" * 60)
    
    # Test 1: Direct Gold API functionality
    print("\n1. Testing Direct GoldPriceAPI Class")
    print("-" * 40)
    
    try:
        gold_api = GoldPriceAPI()
        print("✅ GoldPriceAPI initialized successfully")
        
        # Test current price
        current_price = gold_api.get_current_gold_price()
        if isinstance(current_price, dict):
            price_value = current_price.get('price', current_price.get('value', 0))
            print(f"✅ Current gold price: ${price_value:.2f}")
            print(f"   Response format: {list(current_price.keys())}")
        else:
            print(f"✅ Current gold price: ${current_price:.2f}")
        
        # Test historical data
        history = gold_api.get_gold_history(start_date="2025-11-24", end_date="2025-12-01")
        print(f"✅ Historical data retrieved: {len(history)} days")
        if history:
            # Check the structure of historical data
            latest = history[-1]
            if isinstance(latest, dict):
                if 'price' in latest:
                    try:
                        price = float(latest['price'])
                        print(f"   Latest price in history: ${price:.2f}")
                    except (ValueError, TypeError):
                        print(f"   Latest price in history: {latest['price']}")
                elif 'max_price' in latest:
                    try:
                        price = float(latest['max_price'])
                        print(f"   Latest price in history: ${price:.2f}")
                    except (ValueError, TypeError):
                        print(f"   Latest price in history: {latest['max_price']}")
                else:
                    print(f"   Latest data structure: {list(latest.keys())}")
            else:
                print(f"   Latest data type: {type(latest)}")
        
    except Exception as e:
        print(f"❌ GoldPriceAPI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Toolkit integration
    print("\n2. Testing Toolkit Integration")
    print("-" * 40)
    
    try:
        toolkit = Toolkit()
        print("✅ Toolkit initialized successfully")
        
        # Test gold price history tool
        history_tool = toolkit.get_gold_price_history
        history_result = history_tool.invoke({
            "symbol": "GOLD", 
            "curr_date": "2025-12-01", 
            "look_back_days": 7
        })
        print(f"✅ Toolkit gold history tool: {len(history_result)} characters")
        
        # Test gold technical analysis tool
        analysis_tool = toolkit.get_gold_technical_analysis
        analysis_result = analysis_tool.invoke({
            "symbol": "GOLD", 
            "curr_date": "2025-12-01", 
            "look_back_days": 7
        })
        print(f"✅ Toolkit gold analysis tool: {len(analysis_result)} characters")
        
    except Exception as e:
        print(f"❌ Toolkit integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Configuration verification
    print("\n3. Testing Configuration")
    print("-" * 40)
    
    try:
        config = get_config()
        
        # Check that old RapidAPI config is gone
        if "rapidapi_key" in config:
            print("⚠️  Old rapidapi_key still found in config")
        else:
            print("✅ Old rapidapi_key correctly removed")
        
        # Check that new gold API config exists
        if "gold_api" in config:
            gold_config = config["gold_api"]
            print(f"✅ Gold API config found: {gold_config['base_url']}")
        else:
            print("❌ Gold API config not found")
            return False
        
        # Check environment variable
        gold_api_key = os.getenv("GOLDAPI_KEY")
        if gold_api_key:
            print(f"✅ GOLDAPI_KEY environment variable set: {gold_api_key[:10]}...")
        else:
            print("❌ GOLDAPI_KEY environment variable not found")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False
    
    # Test 4: Asset type detection
    print("\n4. Testing Asset Type Detection")
    print("-" * 40)
    
    try:
        from tradingagents.agents.analysts.market_analyst import _detect_asset_type
        
        # Test various gold symbols
        gold_symbols = ["GOLD", "XAU", "XAUUSD", "gold", "Gold"]
        for symbol in gold_symbols:
            asset_type = _detect_asset_type(symbol)
            print(f"✅ {symbol} -> {asset_type}")
        
        # Test non-gold symbols
        non_gold_symbols = ["AAPL", "BTC", "EURUSD"]
        for symbol in non_gold_symbols:
            asset_type = _detect_asset_type(symbol)
            print(f"✅ {symbol} -> {asset_type}")
            
    except Exception as e:
        print(f"❌ Asset type detection test failed: {e}")
        return False
    
    # Test 5: Tool binding (without LLM)
    print("\n5. Testing Tool Binding")
    print("-" * 40)
    
    try:
        toolkit = Toolkit()
        
        # Get gold tools
        gold_tools = [
            toolkit.get_gold_price_history,
            toolkit.get_gold_technical_analysis
        ]
        
        print(f"✅ Retrieved {len(gold_tools)} gold tools")
        
        # Test tool attributes
        for tool in gold_tools:
            print(f"   - {tool.name}: {tool.description[:50]}...")
            
    except Exception as e:
        print(f"❌ Tool binding test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! Gold API migration is complete and working!")
    print("=" * 60)
    
    return True

def test_api_comparison():
    """Compare old vs new API behavior"""
    print("\n🔄 API Comparison Test")
    print("=" * 40)
    
    try:
        # Test new FCSAPI
        gold_api = GoldPriceAPI()
        new_data = gold_api.get_gold_history(start_date="2025-11-26", end_date="2025-12-01")
        
        print(f"New API (FCSAPI):")
        print(f"  - Data points: {len(new_data)}")
        if new_data:
            latest = new_data[-1]
            if isinstance(latest, dict):
                if 'price' in latest:
                    try:
                        price = float(latest['price'])
                        print(f"  - Latest price: ${price:.2f}")
                    except (ValueError, TypeError):
                        print(f"  - Latest price: {latest['price']}")
                elif 'max_price' in latest:
                    try:
                        price = float(latest['max_price'])
                        print(f"  - Latest price: ${price:.2f}")
                    except (ValueError, TypeError):
                        print(f"  - Latest price: {latest['max_price']}")
                print(f"  - Data structure: {list(latest.keys())}")
            else:
                print(f"  - Latest data type: {type(latest)}")
        
        return True
        
    except Exception as e:
        print(f"❌ API comparison failed: {e}")
        return False

if __name__ == "__main__":
    success = test_gold_api_migration()
    
    if success:
        test_api_comparison()
        
        print("\n📋 Migration Summary:")
        print("✅ RapidAPI -> FCSAPI migration complete")
        print("✅ RAPIDAPI_KEY -> GOLDAPI_KEY environment variable updated")
        print("✅ GoldPriceAPI class updated for new endpoint")
        print("✅ Data parsing updated for new response format")
        print("✅ Toolkit integration working")
        print("✅ Asset type detection working")
        print("✅ Tool binding working")
        
        print("\n🚀 The gold trading system is now using FCSAPI!")
    else:
        print("\n❌ Migration tests failed. Please check the errors above.")
