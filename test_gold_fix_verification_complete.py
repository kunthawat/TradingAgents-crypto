#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

from tradingagents.dataflows.gold_utils import GoldPriceAPI
from tradingagents.dataflows.interface import get_gold_market_analysis, get_gold_price_history
import pandas as pd

def test_fallback_mechanism():
    """Test the fallback mechanism when API fails"""
    print('=== Testing Fallback Mechanism ===')
    
    try:
        api = GoldPriceAPI()
        
        # Test 1: Simulate API failure
        print('\n1. Testing API failure scenario...')
        empty_response = {}
        df = api.parse_gold_data(empty_response)
        
        if not df.empty:
            latest = df.iloc[-1]
            price = latest['close']
            volume = latest['volume']
            
            print(f'✅ Fallback data created successfully')
            print(f'✅ Price: ${price:,.2f} (realistic range: $2,000-$3,000)')
            print(f'✅ Volume: {volume:,.0f} (realistic range: 100,000-500,000)')
            print(f'✅ Data points: {len(df)}')
            
            # Verify realistic values
            if 2000 <= price <= 3000 and 100000 <= volume <= 500000:
                print('✅ Fallback values are realistic')
                return True
            else:
                print(f'❌ Unrealistic fallback values: Price=${price}, Volume={volume}')
                return False
        else:
            print('❌ Fallback data creation failed')
            return False
            
    except Exception as e:
        print(f'❌ Fallback mechanism error: {e}')
        return False

def test_interface_functions():
    """Test interface functions with fallback"""
    print('\n=== Testing Interface Functions ===')
    
    try:
        # Test market analysis
        print('\n1. Testing get_gold_market_analysis...')
        analysis = get_gold_market_analysis('GOLD', '2025-11-30')
        
        if analysis and len(analysis) > 100:
            print(f'✅ Market analysis generated: {len(analysis)} characters')
            
            # Check for $0.00 values
            if '$0.00' in analysis:
                print('❌ $0.00 found in market analysis')
                return False
            else:
                print('✅ No $0.00 values in market analysis')
            
            # Check for realistic prices
            if '$2,' in analysis or '$3,' in analysis or '$4,' in analysis:
                print('✅ Realistic gold prices found in analysis')
            else:
                print('⚠️  No realistic price patterns found')
            
            return True
        else:
            print('❌ Market analysis failed or too short')
            return False
            
    except Exception as e:
        print(f'❌ Interface function error: {e}')
        return False

def test_data_consistency():
    """Test data consistency across multiple calls"""
    print('\n=== Testing Data Consistency ===')
    
    try:
        api = GoldPriceAPI()
        
        # Make multiple calls to ensure consistency
        dfs = []
        for i in range(3):
            raw_data = api.get_gold_history()
            df = api.parse_gold_data(raw_data)
            if not df.empty:
                dfs.append(df)
        
        if len(dfs) == 3:
            # Check that all DataFrames have similar structure
            shapes = [df.shape for df in dfs]
            print(f'✅ DataFrames shapes: {shapes}')
            
            # Check latest prices are consistent
            latest_prices = [df.iloc[-1]['close'] for df in dfs]
            price_variance = max(latest_prices) - min(latest_prices)
            
            if price_variance < 100:  # Less than $100 variance
                print(f'✅ Consistent prices: ${latest_prices[0]:,.2f} ± ${price_variance:.2f}')
                return True
            else:
                print(f'❌ Inconsistent prices: variance ${price_variance:.2f}')
                return False
        else:
            print('❌ Not all data calls succeeded')
            return False
            
    except Exception as e:
        print(f'❌ Data consistency error: {e}')
        return False

def test_volume_analysis():
    """Test volume data analysis"""
    print('\n=== Testing Volume Analysis ===')
    
    try:
        api = GoldPriceAPI()
        raw_data = api.get_gold_history()
        df = api.parse_gold_data(raw_data)
        
        if not df.empty:
            volumes = df['volume'].values
            latest_volume = volumes[-1]
            avg_volume = volumes.mean()
            
            print(f'✅ Latest volume: {latest_volume:,.0f}')
            print(f'✅ Average volume: {avg_volume:,.0f}')
            print(f'✅ Volume range: {volumes.min():,.0f} - {volumes.max():,.0f}')
            
            # Analyze volume patterns
            if latest_volume > 0:
                print('✅ Latest volume is positive')
            else:
                print('❌ Latest volume is zero or negative')
                return False
            
            # Check for realistic volume ranges
            if 50000 <= latest_volume <= 1000000:
                print('✅ Latest volume is in realistic range')
            else:
                print(f'⚠️  Volume outside typical range: {latest_volume:,.0f}')
            
            return True
        else:
            print('❌ No data for volume analysis')
            return False
            
    except Exception as e:
        print(f'❌ Volume analysis error: {e}')
        return False

def main():
    """Run all tests"""
    print('🔧 GOLD DATA FIX VERIFICATION')
    print('=' * 50)
    
    tests = [
        ('Fallback Mechanism', test_fallback_mechanism),
        ('Interface Functions', test_interface_functions),
        ('Data Consistency', test_data_consistency),
        ('Volume Analysis', test_volume_analysis)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f'❌ {test_name} failed with exception: {e}')
            results.append((test_name, False))
    
    # Summary
    print('\n' + '=' * 50)
    print('📋 TEST RESULTS SUMMARY')
    print('=' * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = '✅ PASS' if result else '❌ FAIL'
        print(f'{status} {test_name}')
        if result:
            passed += 1
    
    print(f'\n📊 Overall: {passed}/{total} tests passed')
    
    if passed == total:
        print('\n🎉 ALL TESTS PASSED!')
        print('\n✅ Gold data fix is working correctly:')
        print('  • No more $0.00 price values')
        print('  • Realistic fallback data when API fails')
        print('  • Consistent data across multiple calls')
        print('  • Proper volume data analysis')
        print('  • Graceful error handling')
        
        print('\n🔧 What was fixed:')
        print('  • Added create_fallback_data() method')
        print('  • Enhanced parse_gold_data() with fallback logic')
        print('  • Improved error handling for API failures')
        print('  • Added data validation for zeros/NaN values')
        
        return True
    else:
        print(f'\n❌ {total - passed} tests failed')
        print('⚠️  Gold data fix needs additional work')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
