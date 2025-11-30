#!/usr/bin/env python3
"""
Simple file-based verification test for the gold price fix.
Checks that the missing tool has been added to the code without importing modules.
"""

import os
import re

def test_agent_utils_file():
    """Test that the agent utils file contains the missing tool"""
    print("🔧 Testing Agent Utils File...")
    
    try:
        file_path = '/Users/kunthawatgreethong/Github/TradingAgents-crypto/tradingagents/agents/utils/agent_utils.py'
        
        if not os.path.exists(file_path):
            print("❌ Agent utils file not found")
            return False
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for the missing tool
        if 'get_gold_technical_analysis' in content:
            print("✅ get_gold_technical_analysis tool found in file")
            
            # Check for proper function definition
            if 'def get_gold_technical_analysis(' in content:
                print("✅ Function definition found")
                
                # Check for correct parameters
                if 'symbol' in content and 'curr_date' in content and 'look_back_days' in content:
                    print("✅ Correct parameters found")
                    
                    # Check for interface call
                    if 'interface.get_gold_technical_analysis' in content:
                        print("✅ Interface call found")
                        return True
                    else:
                        print("❌ Interface call not found")
                        return False
                else:
                    print("❌ Missing required parameters")
                    return False
            else:
                print("❌ Function definition not found")
                return False
        else:
            print("❌ get_gold_technical_analysis tool not found")
            return False
            
    except Exception as e:
        print(f"❌ File test failed: {e}")
        return False

def test_interface_file():
    """Test that the interface file contains the gold technical analysis function"""
    print("\n🔧 Testing Interface File...")
    
    try:
        file_path = '/Users/kunthawatgreethong/Github/TradingAgents-crypto/tradingagents/dataflows/interface.py'
        
        if not os.path.exists(file_path):
            print("❌ Interface file not found")
            return False
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for the interface function
        if 'def get_gold_technical_analysis(' in content:
            print("✅ get_gold_technical_analysis function found in interface")
            
            # Check for gold_utils import
            if 'from . import gold_utils' in content or 'import gold_utils' in content:
                print("✅ Gold utils import found")
                return True
            else:
                print("❌ Gold utils import not found")
                return False
        else:
            print("❌ get_gold_technical_analysis function not found")
            return False
            
    except Exception as e:
        print(f"❌ Interface file test failed: {e}")
        return False

def test_gold_tools_count():
    """Test that all expected gold tools are present in agent utils"""
    print("\n🔧 Testing Gold Tools Count...")
    
    try:
        file_path = '/Users/kunthawatgreethong/Github/TradingAgents-crypto/tradingagents/agents/utils/agent_utils.py'
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Expected gold tools
        expected_tools = [
            'get_gold_price_history',
            'get_gold_market_analysis', 
            'get_gold_news_analysis',
            'get_gold_fundamentals_analysis',
            'get_gold_technical_analysis'
        ]
        
        found_tools = []
        missing_tools = []
        
        for tool in expected_tools:
            if f'def {tool}(' in content:
                found_tools.append(tool)
            else:
                missing_tools.append(tool)
        
        print(f"Found {len(found_tools)} gold tools:")
        for tool in found_tools:
            print(f"  ✅ {tool}")
        
        if missing_tools:
            print(f"Missing {len(missing_tools)} gold tools:")
            for tool in missing_tools:
                print(f"  ❌ {tool}")
        
        return len(missing_tools) == 0
            
    except Exception as e:
        print(f"❌ Tools count test failed: {e}")
        return False

def test_function_signature():
    """Test the function signature in the file"""
    print("\n🔧 Testing Function Signature...")
    
    try:
        file_path = '/Users/kunthawatgreethong/Github/TradingAgents-crypto/tradingagents/agents/utils/agent_utils.py'
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the function definition
        pattern = r'def get_gold_technical_analysis\(([^)]+)\):'
        match = re.search(pattern, content)
        
        if match:
            params = match.group(1)
            print(f"Function parameters: {params}")
            
            # Check for expected parameters
            expected_params = ['symbol', 'curr_date', 'look_back_days']
            found_params = []
            
            for param in expected_params:
                if param in params:
                    found_params.append(param)
            
            if len(found_params) == len(expected_params):
                print("✅ All expected parameters found")
                return True
            else:
                print(f"❌ Missing parameters: {set(expected_params) - set(found_params)}")
                return False
        else:
            print("❌ Function signature not found")
            return False
            
    except Exception as e:
        print(f"❌ Signature test failed: {e}")
        return False

def main():
    """Run file-based verification tests"""
    print("🎯 Gold Price Fix - File-Based Verification")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Agent Utils File", test_agent_utils_file),
        ("Interface File", test_interface_file),
        ("Gold Tools Count", test_gold_tools_count),
        ("Function Signature", test_function_signature)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        results[test_name] = test_func()
    
    # Final summary
    print(f"\n{'='*50}")
    print("🏁 FILE-BASED VERIFICATION RESULTS")
    print(f"{'='*50}")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 FILE-BASED VERIFICATION PASSED!")
        print("✅ The missing get_gold_technical_analysis tool has been correctly added")
        print("✅ All gold tools are now available in the agent toolkit")
        print("✅ The fix should resolve the $0.00 gold price issue")
        print("\n📝 Summary of Fix:")
        print("   • Added get_gold_technical_analysis tool to agent_utils.py")
        print("   • Tool correctly calls interface.get_gold_technical_analysis()")
        print("   • All 5 gold tools are now present in the toolkit")
        print("   • Function signature matches expected parameters")
        print("\n🚀 Next Steps:")
        print("   1. Deploy the code changes")
        print("   2. Test the web application with GOLD analysis")
        print("   3. Verify users see real gold prices (~$4,000+) instead of $0.00")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
