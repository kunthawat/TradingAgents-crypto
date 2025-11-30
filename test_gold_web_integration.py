#!/usr/bin/env python3
"""
Test gold data through the web application interface
"""

import os
import sys
import json
from datetime import datetime, timedelta

def test_gold_via_web_app():
    """Test gold data through the web app interface"""
    print("=== Testing Gold via Web App Interface ===")
    
    try:
        # Import the web app
        from tradingagents.dataflows.interface import get_gold_price_data
        
        # Test the interface function
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        print(f"Testing gold data from {start_date} to {end_date}")
        
        result = get_gold_price_data("GOLD", start_date, end_date)
        
        if result:
            print("✓ get_gold_price_data returned data!")
            print(f"Result length: {len(result)} characters")
            
            # Check for real prices in the result
            if "$4," in result or "$3," in result:
                print("✅ Real gold prices found in output!")
                
                # Extract some sample data
                lines = result.split('\n')
                price_lines = [line for line in lines if 'Close:' in line or 'Price:' in line]
                
                if price_lines:
                    print(f"\n--- Sample Price Data ---")
                    for line in price_lines[:5]:  # Show first 5 price lines
                        print(line.strip())
                
                return True
            else:
                print("❌ No real prices found in output")
                print(f"First 500 characters: {result[:500]}")
                return False
        else:
            print("❌ get_gold_price_data returned empty")
            return False
        
    except Exception as e:
        print(f"❌ Error testing gold via web app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gold_technical_analysis():
    """Test gold technical analysis"""
    print("\n=== Testing Gold Technical Analysis ===")
    
    try:
        from tradingagents.dataflows.interface import get_gold_technical_analysis
        
        curr_date = datetime.now().strftime("%Y-%m-%d")
        
        result = get_gold_technical_analysis("GOLD", curr_date, 30)
        
        if result:
            print("✓ get_gold_technical_analysis returned data!")
            print(f"Result length: {len(result)} characters")
            
            # Check for real prices
            if "$4," in result or "$3," in result:
                print("✅ Real gold prices found in technical analysis!")
                
                # Show first 500 characters
                print(f"\n--- Sample Technical Analysis ---")
                print(result[:500])
                
                return True
            else:
                print("❌ No real prices found in technical analysis")
                print(f"First 500 characters: {result[:500]}")
                return False
        else:
            print("❌ get_gold_technical_analysis returned empty")
            return False
        
    except Exception as e:
        print(f"❌ Error testing gold technical analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gold_market_analysis():
    """Test gold market analysis"""
    print("\n=== Testing Gold Market Analysis ===")
    
    try:
        from tradingagents.dataflows.interface import get_gold_market_analysis
        
        curr_date = datetime.now().strftime("%Y-%m-%d")
        
        result = get_gold_market_analysis("GOLD", curr_date)
        
        if result:
            print("✓ get_gold_market_analysis returned data!")
            print(f"Result length: {len(result)} characters")
            
            # Check for real prices
            if "$4," in result or "$3," in result:
                print("✅ Real gold prices found in market analysis!")
                
                # Show first 500 characters
                print(f"\n--- Sample Market Analysis ---")
                print(result[:500])
                
                return True
            else:
                print("❌ No real prices found in market analysis")
                print(f"First 500 characters: {result[:500]}")
                return False
        else:
            print("❌ get_gold_market_analysis returned empty")
            return False
        
    except Exception as e:
        print(f"❌ Error testing gold market analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests through the web app interface"""
    print("🌐 Testing Gold Data via Web App Interface")
    print("=" * 50)
    
    # Test all gold functions
    price_success = test_gold_via_web_app()
    technical_success = test_gold_technical_analysis()
    market_success = test_gold_market_analysis()
    
    print("\n🎯 Test Results:")
    print(f"Price Data Test: {'✅ PASSED' if price_success else '❌ FAILED'}")
    print(f"Technical Analysis Test: {'✅ PASSED' if technical_success else '❌ FAILED'}")
    print(f"Market Analysis Test: {'✅ PASSED' if market_success else '❌ FAILED'}")
    
    if price_success and technical_success and market_success:
        print("\n🎉 All tests passed! Gold price data is working correctly!")
        print("The web application should now show real gold prices instead of $0.00")
    else:
        print("\n⚠️  Some tests failed. The issue may still exist.")

if __name__ == "__main__":
    main()
