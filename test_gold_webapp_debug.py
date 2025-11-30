#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

from tradingagents.dataflows.gold_utils import GoldPriceAPI
from tradingagents.dataflows.interface import get_gold_market_analysis

def test_gold_pipeline():
    print('=== Testing Gold Data Pipeline ===')
    
    # Test 1: Direct API call
    try:
        api = GoldPriceAPI()
        raw_data = api.get_gold_history()
        if raw_data and 'history' in raw_data:
            first_entry = raw_data['history'][0]
            price = first_entry.get('close', 0)
            volume = first_entry.get('volume', 0)
            print(f'✅ Raw API - Price: ${price}, Volume: {volume}')
            
            if price == 0:
                print('❌ $0.00 found in raw API data!')
                return False
        else:
            print('❌ Raw API failed - no history data')
            return False
    except Exception as e:
        print(f'❌ Raw API error: {e}')
        return False
    
    # Test 2: Interface function
    try:
        analysis = get_gold_market_analysis('GOLD', '2025-11-30')
        if analysis and len(analysis) > 50:
            if '$0.00' in analysis:
                print('❌ $0.00 found in market analysis')
                print('Sample:', analysis[:200])
                return False
            else:
                print('✅ No $0.00 in market analysis')
            print(f'✅ Analysis length: {len(analysis)} characters')
        else:
            print('❌ Market analysis failed - too short')
            return False
    except Exception as e:
        print(f'❌ Market analysis error: {e}')
        return False
    
    print('✅ Gold pipeline test passed')
    return True

def test_webapp_integration():
    print('\n=== Testing WebApp Integration ===')
    
    try:
        # Import webapp
        from web_app import app
        
        # Test health endpoint
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                print('✅ Health endpoint working')
            else:
                print(f'❌ Health endpoint failed: {response.status_code}')
                return False
        
        print('✅ WebApp integration test passed')
        return True
        
    except Exception as e:
        print(f'❌ WebApp integration error: {e}')
        return False

if __name__ == '__main__':
    success = True
    success &= test_gold_pipeline()
    success &= test_webapp_integration()
    
    if success:
        print('\n🎉 All tests passed - No $0.00 issues found!')
    else:
        print('\n❌ Tests failed - $0.00 issues detected!')
        sys.exit(1)
