#!/usr/bin/env python3
"""
Test script to verify the HTML fixes are working correctly.
This script checks that the HTML file is properly formatted and doesn't have
references to removed elements that would cause JavaScript errors.
"""

import re
from pathlib import Path

def test_html_file():
    """Test the HTML file for common issues."""
    html_file = Path('templates/index.html')
    
    if not html_file.exists():
        print("❌ HTML file not found")
        return False
    
    content = html_file.read_text()
    
    # Test 1: Check for removed API key references
    api_key_refs = re.findall(r"document\.getElementById\(['\"]api_key['\"]", content)
    if api_key_refs:
        print(f"❌ Found {len(api_key_refs)} references to removed 'api_key' element")
        return False
    else:
        print("✅ No references to removed 'api_key' element")
    
    # Test 2: Check for removed backend URL references
    backend_url_refs = re.findall(r"document\.getElementById\(['\"]backend_url['\"]", content)
    if backend_url_refs:
        print(f"❌ Found {len(backend_url_refs)} references to removed 'backend_url' element")
        return False
    else:
        print("✅ No references to removed 'backend_url' element")
    
    # Test 3: Check for secret password field
    secret_pass_refs = re.findall(r"document\.getElementById\(['\"]secret_pass['\"]", content)
    if secret_pass_refs:
        print(f"✅ Found {len(secret_pass_refs)} references to 'secret_pass' element")
    else:
        print("❌ No references to 'secret_pass' element found")
        return False
    
    # Test 4: Check for analysis date field
    analysis_date_refs = re.findall(r"document\.getElementById\(['\"]analysis_date['\"]", content)
    if analysis_date_refs:
        print(f"✅ Found {len(analysis_date_refs)} references to 'analysis_date' element")
    else:
        print("❌ No references to 'analysis_date' element found")
        return False
    
    # Test 5: Check for language field
    language_refs = re.findall(r"document\.getElementById\(['\"]language['\"]", content)
    if language_refs:
        print(f"✅ Found {len(language_refs)} references to 'language' element")
    else:
        print("❌ No references to 'language' element found")
        return False
    
    # Test 6: Check for form submission handler
    form_submit_refs = re.findall(r"document\.getElementById\(['\"]analysisForm['\"]", content)
    if form_submit_refs:
        print(f"✅ Found {len(form_submit_refs)} references to 'analysisForm' element")
    else:
        print("❌ No references to 'analysisForm' element found")
        return False
    
    # Test 7: Check for date default setting
    date_default_pattern = r"new Date\(\)\.toISOString\(\)\.split\('T'\)\[0\]"
    if re.search(date_default_pattern, content):
        print("✅ Found date default setting code")
    else:
        print("❌ No date default setting code found")
        return False
    
    # Test 8: Check for zai-org/GLM-4.6 model
    if 'zai-org/GLM-4.6' in content:
        print("✅ Found zai-org/GLM-4.6 model option")
    else:
        print("❌ zai-org/GLM-4.6 model option not found")
        return False
    
    # Test 9: Check for Thai language option
    if 'Thai (ไทย)' in content:
        print("✅ Found Thai language option")
    else:
        print("❌ Thai language option not found")
        return False
    
    # Test 10: Check for password validation
    if 'secret_pass' in content and 'Please enter the secret password' in content:
        print("✅ Found password validation code")
    else:
        print("❌ Password validation code not found")
        return False
    
    print("\n🎉 All HTML tests passed! The fixes should resolve the JavaScript errors.")
    return True

def test_endpoint_structure():
    """Test that the expected endpoints are mentioned in the JavaScript."""
    html_file = Path('templates/index.html')
    content = html_file.read_text()
    
    # Check for the correct API endpoint
    if '/api/start_analysis' in content:
        print("✅ Found correct API endpoint: /api/start_analysis")
        return True
    else:
        print("❌ API endpoint /api/start_analysis not found")
        return False

def main():
    """Run all tests."""
    print("🔍 Testing HTML Fixes\n")
    print("=" * 50)
    
    tests = [
        test_html_file,
        test_endpoint_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The HTML fixes should resolve the JavaScript issues.")
        print("\n📋 Summary of fixes applied:")
        print("✅ Removed references to deleted API key field")
        print("✅ Removed references to deleted backend URL field")
        print("✅ Fixed analysis date default setting")
        print("✅ Verified password validation is present")
        print("✅ Confirmed language selection is working")
        print("✅ Verified zai-org/GLM-4.6 model is included")
        print("✅ Confirmed API endpoint is correct")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
