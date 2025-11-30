#!/usr/bin/env python3
"""
Test the interface function directly
"""

import sys
sys.path.insert(0, '.')
from tradingagents.dataflows.gold_utils import GoldPriceAPI
from tradingagents.dataflows.interface import get_gold_price_data
from datetime import datetime

# Test the gold utils directly
print('=== Testing Gold Utils Directly ===')
api = GoldPriceAPI()
raw_data = api.get_gold_history()
df = api.parse_gold_data(raw_data)

if not df.empty:
    print(f'✓ Gold utils working: {len(df)} rows')
    print(f'Price range: ${df.close.min():.2f} - ${df.close.max():.2f}')
    
    # Test the interface function
    result = get_gold_price_data('GOLD', datetime.now().strftime('%Y-%m-%d'), 30)
    print(f'Interface result length: {len(result)}')
    
    # Check for issues
    has_zero_prices = '$0.00' in result
    has_realistic_prices = '$4,' in result or '$3,' in result
    
    print(f'Contains $0.00: {has_zero_prices}')
    print(f'Contains realistic prices: {has_realistic_prices}')
    print(f'First 500 chars: {result[:500]}...')
    
    if has_zero_prices and not has_realistic_prices:
        print('❌ ISSUE FOUND: Interface returning $0.00!')
    elif has_realistic_prices:
        print('✅ Interface working correctly!')
    else:
        print('⚠️  Unclear result from interface')
else:
    print('❌ Gold utils failed')
