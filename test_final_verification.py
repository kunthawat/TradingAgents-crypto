#!/usr/bin/env python3
"""
Final verification test for gold API migration
"""

from tradingagents.dataflows.gold_utils import GoldPriceAPI

def main():
    print('🧪 Final Migration Verification Test')
    print('=' * 40)

    # Test 1: API Initialization
    try:
        api = GoldPriceAPI()
        print('✅ API initialization successful')
    except Exception as e:
        print(f'❌ API initialization failed: {e}')
        return False

    # Test 2: Current Price
    try:
        current = api.get_current_gold_price()
        price = current.get('price', 0)
        print(f'✅ Current price: ${price:.2f}')
    except Exception as e:
        print(f'❌ Current price failed: {e}')
        return False

    # Test 3: Data Parsing
    try:
        df = api.parse_gold_data(current)
        print(f'✅ Data parsing successful: {df.shape} shape')
    except Exception as e:
        print(f'❌ Data parsing failed: {e}')
        return False

    # Test 4: Technical Indicators
    try:
        df_indicators = api.calculate_technical_indicators(df)
        print(f'✅ Technical indicators calculated: {len(df_indicators.columns)} columns')
    except Exception as e:
        print(f'❌ Technical indicators failed: {e}')
        return False

    print('=' * 40)
    print('🎉 All verification tests passed!')
    print('✅ Gold API migration is complete and operational')
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
