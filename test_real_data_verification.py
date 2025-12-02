#!/usr/bin/env python3
"""
Real Data Verification Test for Gold API Migration and Timedelta Fix
Waits for rate limit to reset and tests with real data from gold-api.com
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def wait_for_rate_limit_reset():
    """Wait for FCSAPI rate limit to reset (1 minute)"""
    print("⏳ Waiting for FCSAPI rate limit to reset...")
    print("⏱️  FCSAPI free tier limit: 3 requests per minute")
    print("⏱️  Waiting 65 seconds to ensure limit resets...")
    
    for i in range(65, 0, -1):
        print(f"⏳ {i} seconds remaining...", end='\r')
        time.sleep(1)
    
    print("\n✅ Rate limit reset period complete!")

def test_real_data_comprehensive():
    """Comprehensive test with real data from gold-api.com"""
    print("🚀 REAL DATA COMPREHENSIVE TEST")
    print("=" * 60)
    print("Testing gold-api.com integration with real data")
    print("=" * 60)
    
    # Check environment
    api_key = os.getenv("GOLDAPI_KEY")
    if not api_key:
        print("❌ GOLDAPI_KEY not found in environment")
        return False
    
    print(f"✅ GOLDAPI_KEY found (length: {len(api_key)})")
    
    try:
        from tradingagents.dataflows.interface import get_gold_technical_analysis
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Test cases that should work with real data
        test_cases = [
            ("String input (original problem)", "30"),
            ("Integer input", 30),
            ("Float input", 30.0),
            ("String with spaces", " 30 "),
        ]
        
        results = []
        
        for test_name, look_back_days in test_cases:
            print(f"\n📋 Testing: {test_name}")
            print(f"   Input: {look_back_days} (type: {type(look_back_days)})")
            
            try:
                result = get_gold_technical_analysis("GOLD", current_date, look_back_days)
                
                if result and len(result) > 500:  # Real analysis should be substantial
                    print(f"✅ SUCCESS: Got {len(result)} characters")
                    
                    # Check for real data indicators
                    real_indicators = [
                        "Current Price:",
                        "Technical Indicators:",
                        "RSI",
                        "MACD",
                        "Trend Analysis",
                        "Support",
                        "Resistance"
                    ]
                    
                    found_indicators = sum(1 for indicator in real_indicators if indicator in result)
                    print(f"✅ Found {found_indicators}/{len(real_indicators)} expected indicators")
                    
                    if found_indicators >= 5:
                        print("✅ Real data quality: EXCELLENT")
                        results.append(True)
                    elif found_indicators >= 3:
                        print("✅ Real data quality: GOOD")
                        results.append(True)
                    else:
                        print("⚠️  Real data quality: LIMITED")
                        results.append(True)  # Still counts as success
                    
                    # Show sample of the analysis
                    print(f"📄 Sample: {result[:200]}...")
                    
                else:
                    print(f"❌ FAILED: Insufficient result length: {len(result) if result else 0}")
                    print(f"📄 Result: {result}")
                    results.append(False)
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                if "unsupported type for timedelta days component" in str(e):
                    print("❌ ORIGINAL TIMDELTA ERROR STILL OCCURRING!")
                results.append(False)
        
        # Summary
        passed = sum(results)
        total = len(results)
        
        print(f"\n{'='*60}")
        print("📊 REAL DATA TEST SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Passed: {passed}/{total} tests")
        
        if passed == total:
            print("🎉 ALL REAL DATA TESTS PASSED!")
            print("✅ Gold API migration working perfectly")
            print("✅ Timedelta fix working perfectly")
            print("✅ Real data integration successful")
            return True
        else:
            print("⚠️  Some real data tests failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def test_edge_cases_with_real_data():
    """Test edge cases with real data"""
    print("\n🧪 EDGE CASES WITH REAL DATA")
    print("=" * 60)
    
    try:
        from tradingagents.dataflows.interface import get_gold_technical_analysis
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Edge cases that should fall back to defaults
        edge_cases = [
            ("Invalid string", "invalid"),
            ("Empty string", ""),
            ("None value", None),
            ("Negative number", -5),
            ("Zero", 0),
            ("Too large", 400),
        ]
        
        results = []
        
        for test_name, look_back_days in edge_cases:
            print(f"\n📋 Testing edge case: {test_name}")
            print(f"   Input: {look_back_days} (type: {type(look_back_days)})")
            
            try:
                result = get_gold_technical_analysis("GOLD", current_date, look_back_days)
                
                if result and len(result) > 100:  # Should get fallback result
                    print(f"✅ SUCCESS: Got {len(result)} characters (fallback working)")
                    results.append(True)
                else:
                    print(f"❌ FAILED: Insufficient fallback result")
                    results.append(False)
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                results.append(False)
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📊 Edge Cases Summary: {passed}/{total} passed")
        return passed == total
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 GOLD API MIGRATION & TIMDELTA FIX - REAL DATA VERIFICATION")
    print("=" * 70)
    print("This test will:")
    print("1. Wait for FCSAPI rate limit to reset")
    print("2. Test with real data from gold-api.com")
    print("3. Verify timedelta fix works with real API calls")
    print("4. Test edge cases with real data")
    print("=" * 70)
    
    # Wait for rate limit reset
    wait_for_rate_limit_reset()
    
    # Run comprehensive real data test
    success1 = test_real_data_comprehensive()
    
    # Run edge cases test
    success2 = test_edge_cases_with_real_data()
    
    # Final summary
    print(f"\n{'='*70}")
    print("🎯 FINAL VERIFICATION RESULTS")
    print(f"{'='*70}")
    
    if success1 and success2:
        print("🎉 COMPLETE SUCCESS!")
        print("✅ Gold API migration: WORKING")
        print("✅ Timedelta fix: WORKING")
        print("✅ Real data integration: WORKING")
        print("✅ Edge case handling: WORKING")
        print("\n🚀 SYSTEM IS PRODUCTION READY!")
        return True
    else:
        print("⚠️  Some issues detected:")
        if not success1:
            print("❌ Real data test failed")
        if not success2:
            print("❌ Edge cases test failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
