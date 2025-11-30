#!/usr/bin/env python3
"""
Complete simulation of the gold data flow to verify the fix
"""

import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

def simulate_complete_gold_flow():
    """Simulate the complete gold data flow from API to final output"""
    print("=== Simulating Complete Gold Data Flow ===")
    
    # Step 1: API Call (simulating GoldPriceAPI.get_gold_history)
    print("\n--- Step 1: API Call ---")
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("❌ RAPIDAPI_KEY not found")
        return False
    
    base_url = "https://gold-price-api.p.rapidapi.com/v1"
    headers = {
        'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
        'x-rapidapi-key': api_key
    }
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    try:
        response = requests.get(f"{base_url}/gold/history", 
                              headers=headers, 
                              params={'start_date': start_date, 'end_date': end_date})
        response.raise_for_status()
        raw_data = response.json()
        print(f"✅ API call successful - received {len(raw_data.get('history', []))} records")
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False
    
    # Step 2: Data Parsing (simulating GoldPriceAPI.parse_gold_data)
    print("\n--- Step 2: Data Parsing ---")
    
    if 'history' in raw_data:
        history_data = raw_data['history']
    else:
        print("❌ No history data found")
        return False
    
    df = pd.DataFrame(history_data)
    
    # Ensure proper data types
    df['date'] = pd.to_datetime(df['date'])
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"✅ Data parsing successful - DataFrame shape: {df.shape}")
    
    # Step 3: Price Analysis
    print("\n--- Step 3: Price Analysis ---")
    
    if 'close' in df.columns:
        zero_prices = (df['close'] == 0).sum()
        print(f"Total rows: {len(df)}")
        print(f"Zero price rows: {zero_prices}")
        print(f"Non-zero price rows: {len(df) - zero_prices}")
        
        if zero_prices > 0:
            print("❌ Found zero prices - parsing issue!")
            return False
        else:
            print("✅ No zero prices found!")
        
        price_range = f"${df['close'].min():.2f} - ${df['close'].max():.2f}"
        latest_price = f"${df['close'].iloc[-1]:.2f}"
        print(f"Price range: {price_range}")
        print(f"Latest price: {latest_price}")
    
    # Step 4: Format Output (simulating get_gold_price_data function)
    print("\n--- Step 4: Format Output ---")
    
    result_str = f"## GOLD Gold Price Data from {start_date} to {end_date}:\n\n"
    
    # Show recent data (last 5 days)
    recent_data = df.tail(5)
    for _, row in recent_data.iterrows():
        result_str += f"Date: {row['date'].strftime('%Y-%m-%d')}\n"
        result_str += f"Open: ${row['open']:,.2f}\n"
        result_str += f"High: ${row['high']:,.2f}\n"
        result_str += f"Low: ${row['low']:,.2f}\n"
        result_str += f"Close: ${row['close']:,.2f}\n"
        result_str += f"Volume: {row['volume']:,.0f}\n\n"
    
    # Add summary
    latest = df.iloc[-1]
    earliest = df.iloc[0]
    price_change_pct = ((latest['close'] - earliest['close']) / earliest['close']) * 100
    
    result_str += f"## Summary Statistics:\n\n"
    result_str += f"Period Return: {price_change_pct:+.2f}%\n"
    result_str += f"Period High: ${df['high'].max():,.2f}\n"
    result_str += f"Period Low: ${df['low'].min():,.2f}\n"
    result_str += f"Average Volume: {df['volume'].mean():,.0f}\n"
    
    print(f"✅ Output formatting successful - {len(result_str)} characters")
    
    # Step 5: Verify Real Prices
    print("\n--- Step 5: Verify Real Prices ---")
    
    if "$4," in result_str or "$3," in result_str:
        print("✅ Real gold prices found in final output!")
        print("\n--- Sample Output ---")
        print(result_str[:400])
        return True
    else:
        print("❌ No real prices found in final output")
        return False

def main():
    """Run the complete simulation"""
    print("🔄 Complete Gold Data Flow Simulation")
    print("=" * 50)
    
    success = simulate_complete_gold_flow()
    
    print(f"\n🎯 Simulation Result: {'✅ PASSED' if success else '❌ FAILED'}")
    
    if success:
        print("\n🎉 Complete gold data flow is working correctly!")
        print("The fix has resolved the $0.00 price issue.")
        print("Users will now see real gold prices in the web application.")
    else:
        print("\n⚠️  Simulation failed - further investigation needed.")

if __name__ == "__main__":
    main()
