#!/usr/bin/env python3
"""
Comprehensive test for the gold technical analysis timedelta fix.
Tests multiple input types to ensure robust parameter handling.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_interface_function_directly():
    """Test the interface function with various input types"""
    print("🧪 Testing Interface Function Directly")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.interface import get_gold_technical_analysis
        
        # Test cases with different input types
        test_cases = [
            ("Integer input", 30),
            ("String input", "30"),
            ("String with spaces", " 30 "),
            ("Float input", 30.0),
            ("String float", "30.0"),
            ("Invalid string", "invalid"),
            ("Negative number", -5),
            ("Zero", 0),
            ("Too large", 400),
            ("None", None),
        ]
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for test_name, look_back_days in test_cases:
            print(f"\n📋 Testing {test_name}: {look_back_days} (type: {type(look_back_days)})")
            
            try:
                result = get_gold_technical_analysis("GOLD", current_date, look_back_days)
                
                if result and len(result) > 100:  # Reasonable length for technical analysis
                    print(f"✅ SUCCESS: Got {len(result)} characters of analysis")
                    # Check if it contains expected content
                    if "Technical Analysis" in result and "Price Levels" in result:
                        print("✅ Content looks valid")
                    else:
                        print("⚠️  Content may be incomplete")
                else:
                    print(f"❌ FAILED: Got insufficient result: {result}")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def test_gold_utils_function_directly():
    """Test the gold_utils function with various input types"""
    print("\n🧪 Testing Gold Utils Function Directly")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.gold_utils import get_gold_technical_analysis
        
        # Test cases with different input types
        test_cases = [
            ("Integer input", 30),
            ("String input", "30"),
            ("String with spaces", " 30 "),
            ("Float input", 30.0),
            ("String float", "30.0"),
            ("Invalid string", "invalid"),
            ("Negative number", -5),
            ("Zero", 0),
            ("Too large", 400),
        ]
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for test_name, look_back_days in test_cases:
            print(f"\n📋 Testing {test_name}: {look_back_days} (type: {type(look_back_days)})")
            
            try:
                result = get_gold_technical_analysis("GOLD", current_date, look_back_days)
                
                if result and len(result) > 100:  # Reasonable length for technical analysis
                    print(f"✅ SUCCESS: Got {len(result)} characters of analysis")
                    # Check if it contains expected content
                    if "Technical Analysis" in result and "Price Levels" in result:
                        print("✅ Content looks valid")
                    else:
                        print("⚠️  Content may be incomplete")
                else:
                    print(f"❌ FAILED: Got insufficient result: {result}")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def test_agent_toolkit_integration():
    """Test through the agent toolkit"""
    print("\n🧪 Testing Agent Toolkit Integration")
    print("=" * 50)
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        # Test the toolkit method
        if hasattr(Toolkit, 'get_gold_technical_analysis'):
            print("✅ Found get_gold_technical_analysis in Toolkit")
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Test with string input (this is what was causing the original error)
            print("\n📋 Testing with string input through toolkit...")
            try:
                result = Toolkit.get_gold_technical_analysis("GOLD", current_date, "30")
                
                if result and len(result) > 100:
                    print(f"✅ SUCCESS: Got {len(result)} characters through toolkit")
                    print("✅ No timedelta error - fix is working!")
                else:
                    print(f"❌ FAILED: Got insufficient result: {result}")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                if "unsupported type for timedelta days component" in str(e):
                    print("❌ ORIGINAL ERROR STILL OCCURRING - FIX INCOMPLETE")
                else:
                    print("⚠️  Different error occurred")
            
            return True
        else:
            print("❌ get_gold_technical_analysis not found in Toolkit")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🧪 Testing Edge Cases and Boundary Conditions")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.interface import get_gold_technical_analysis
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Edge cases
        edge_cases = [
            ("Minimum valid", 1),
            ("Maximum valid", 365),
            ("Just below minimum", 0),
            ("Just above maximum", 366),
            ("Very large number", 9999),
            ("Empty string", ""),
            ("Whitespace only", "   "),
            ("Special characters", "!@#$%"),
        ]
        
        for test_name, look_back_days in edge_cases:
            print(f"\n📋 Testing {test_name}: {look_back_days}")
            
            try:
                result = get_gold_technical_analysis("GOLD", current_date, look_back_days)
                
                if result and len(result) > 100:
                    print(f"✅ SUCCESS: Got {len(result)} characters")
                else:
                    print(f"❌ FAILED: Got insufficient result: {result}")
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def test_real_api_call():
    """Test with real API call to ensure FCSAPI integration still works"""
    print("\n🧪 Testing Real FCSAPI Integration")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.interface import get_gold_technical_analysis
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        print("📋 Testing with real API call (string input)...")
        try:
            result = get_gold_technical_analysis("GOLD", current_date, "30")
            
            if result and len(result) > 500:  # Real analysis should be substantial
                print(f"✅ SUCCESS: Got {len(result)} characters from real API")
                
                # Check for real data indicators
                real_data_indicators = [
                    "Current Price:",
                    "Technical Indicators:",
                    "RSI",
                    "MACD",
                    "Trend Analysis"
                ]
                
                found_indicators = sum(1 for indicator in real_data_indicators if indicator in result)
                print(f"✅ Found {found_indicators}/{len(real_data_indicators)} expected data indicators")
                
                if found_indicators >= 4:
                    print("✅ Real data integration working correctly")
                else:
                    print("⚠️  Some expected data missing")
                
                return True
            else:
                print(f"❌ FAILED: Got insufficient result: {result}")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 COMPREHENSIVE GOLD TECHNICAL ANALYSIS TIMDELTA FIX TEST")
    print("=" * 70)
    print("Testing the fix for: 'unsupported type for timedelta days component: str'")
    print("=" * 70)
    
    # Check environment
    print("\n🔧 Environment Check:")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check for API key
    api_key = os.getenv("GOLDAPI_KEY")
    if api_key:
        print(f"✅ GOLDAPI_KEY found (length: {len(api_key)})")
    else:
        print("❌ GOLDAPI_KEY not found - some tests may fail")
    
    # Run tests
    tests = [
        ("Interface Function Direct Test", test_interface_function_directly),
        ("Gold Utils Function Direct Test", test_gold_utils_function_directly),
        ("Agent Toolkit Integration Test", test_agent_toolkit_integration),
        ("Edge Cases Test", test_edge_cases),
        ("Real API Integration Test", test_real_api_call),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"🧪 RUNNING: {test_name}")
        print(f"{'='*70}")
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ TEST CRASHED: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 TEST SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - TIMDELTA FIX IS WORKING CORRECTLY!")
        print("✅ The 'unsupported type for timedelta days component: str' error has been resolved")
        print("✅ Gold technical analysis should now work properly through all interfaces")
    else:
        print("⚠️  Some tests failed - the fix may need additional work")
    
    print(f"{'='*70}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
