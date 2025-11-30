#!/usr/bin/env python3
"""
Final verification test for gold price fix.
Tests the complete end-to-end flow from agent tools to real gold prices.
"""

import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.append('/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_gold_technical_analysis_tool():
    """Test the newly added get_gold_technical_analysis tool"""
    print("🔧 Testing Gold Technical Analysis Tool...")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        # Create toolkit instance
        toolkit = Toolkit()
        
        # Test the technical analysis tool
        result = toolkit.get_gold_technical_analysis("GOLD", "2025-11-30", 30)
        
        print("✅ Tool executed successfully")
        print(f"Result length: {len(result)} characters")
        
        # Check for real prices (not $0.00)
        if "$0.00" in result:
            print("❌ Still contains $0.00 values")
            return False
        elif "$4," in result or "$3," in result:
            print("✅ Contains real gold prices ($4,000+ range)")
            return True
        else:
            print("⚠️  Price format unclear, checking for any dollar values...")
            if "$" in result and "0.00" not in result:
                print("✅ Contains non-zero dollar values")
                return True
            else:
                print("❌ No clear price values found")
                return False
                
    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        return False

def test_interface_gold_technical_analysis():
    """Test the interface function directly"""
    print("\n🔧 Testing Interface Gold Technical Analysis...")
    
    try:
        import tradingagents.dataflows.interface as interface
        
        # Test the interface function
        result = interface.get_gold_technical_analysis("GOLD", "2025-11-30", 30)
        
        print("✅ Interface function executed successfully")
        print(f"Result length: {len(result)} characters")
        
        # Check for real prices
        if "$0.00" in result:
            print("❌ Still contains $0.00 values")
            return False
        elif "$4," in result or "$3," in result:
            print("✅ Contains real gold prices ($4,000+ range)")
            return True
        else:
            print("⚠️  Price format unclear")
            return False
            
    except Exception as e:
        print(f"❌ Interface test failed: {e}")
        return False

def test_gold_utils_direct():
    """Test gold utilities directly"""
    print("\n🔧 Testing Gold Utils Direct...")
    
    try:
        from tradingagents.dataflows.gold_utils import get_gold_technical_analysis
        
        # Test the gold utils function
        result = get_gold_technical_analysis("GOLD", "2025-11-30", 30)
        
        print("✅ Gold utils function executed successfully")
        print(f"Result length: {len(result)} characters")
        
        # Check for real prices
        if "$0.00" in result:
            print("❌ Still contains $0.00 values")
            return False
        elif "$4," in result or "$3," in result:
            print("✅ Contains real gold prices ($4,000+ range)")
            return True
        else:
            print("⚠️  Price format unclear")
            return False
            
    except Exception as e:
        print(f"❌ Gold utils test failed: {e}")
        return False

def test_complete_agent_tool_flow():
    """Test the complete flow from agent toolkit to real prices"""
    print("\n🔄 Testing Complete Agent Tool Flow...")
    
    try:
        # Test all gold tools in the toolkit
        toolkit = Toolkit()
        
        tools_to_test = [
            ("get_gold_technical_analysis", ("GOLD", "2025-11-30", 30)),
            ("get_gold_market_analysis", ("GOLD", "2025-11-30")),
            ("get_gold_price_history", ("GOLD", "2025-11-30", 30)),
            ("get_gold_news_analysis", ("GOLD", "2025-11-30", 7)),
            ("get_gold_fundamentals_analysis", ("GOLD", "2025-11-30"))
        ]
        
        results = {}
        for tool_name, args in tools_to_test:
            print(f"  Testing {tool_name}...")
            try:
                tool_func = getattr(toolkit, tool_name)
                result = tool_func(*args)
                results[tool_name] = {
                    "success": True,
                    "has_real_prices": "$4," in result or "$3," in result,
                    "has_zero_prices": "$0.00" in result,
                    "length": len(result)
                }
                print(f"    ✅ {tool_name}: {len(result)} chars")
            except Exception as e:
                results[tool_name] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"    ❌ {tool_name}: {e}")
        
        # Summary
        successful_tools = sum(1 for r in results.values() if r.get("success", False))
        tools_with_real_prices = sum(1 for r in results.values() if r.get("has_real_prices", False))
        tools_with_zero_prices = sum(1 for r in results.values() if r.get("has_zero_prices", False))
        
        print(f"\n📊 Tool Test Summary:")
        print(f"  Total tools tested: {len(tools_to_test)}")
        print(f"  Successful executions: {successful_tools}")
        print(f"  Tools with real prices: {tools_with_real_prices}")
        print(f"  Tools with $0.00 prices: {tools_with_zero_prices}")
        
        return successful_tools == len(tools_to_test) and tools_with_real_prices > 0 and tools_with_zero_prices == 0
        
    except Exception as e:
        print(f"❌ Complete flow test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🎯 Final Gold Price Fix Verification")
    print("=" * 50)
    
    # Check environment
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        print("❌ RAPIDAPI_KEY not found in environment")
        return False
    
    print(f"✅ RAPIDAPI_KEY found: {api_key[:10]}...")
    
    # Run tests
    tests = [
        ("Gold Utils Direct", test_gold_utils_direct),
        ("Interface Function", test_interface_gold_technical_analysis),
        ("Agent Tool", test_gold_technical_analysis_tool),
        ("Complete Flow", test_complete_agent_tool_flow)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        results[test_name] = test_func()
    
    # Final summary
    print(f"\n{'='*50}")
    print("🏁 FINAL VERIFICATION RESULTS")
    print(f"{'='*50}")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Gold price fix is working correctly!")
        print("✅ Users will now see real gold prices instead of $0.00")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Fix may need additional work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
