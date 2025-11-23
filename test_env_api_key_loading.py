#!/usr/bin/env python3
"""
Test to verify that API key is loaded correctly from .env file
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_env_loading():
    """Test that .env file is loaded and API key is available"""
    
    print("Testing .env file loading...")
    print("=" * 50)
    
    try:
        # Import the updated config
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG
        
        # Check if API key is loaded
        api_key = config.get('api_key', '')
        
        if api_key:
            print(f"✅ API key loaded successfully!")
            print(f"   Key length: {len(api_key)} characters")
            print(f"   Key preview: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else api_key[10:]}")
            
            # Check if it matches expected format
            if api_key.startswith('cpk_'):
                print("✅ API key format looks correct (starts with 'cpk_')")
            else:
                print("⚠️  API key format might be incorrect (doesn't start with 'cpk_')")
            
            return True
        else:
            print("❌ API key not loaded - empty string")
            print("   Check that .env file exists and contains OPENAI_API_KEY")
            return False
            
    except Exception as e:
        print(f"❌ Error testing .env loading: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_env_access():
    """Test direct environment variable access"""
    
    print("\nTesting direct environment access...")
    print("=" * 50)
    
    # Check if dotenv was loaded
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv is available")
        
        # Try to load .env explicitly
        result = load_dotenv()
        if result:
            print("✅ .env file loaded successfully")
        else:
            print("⚠️  .env file not found or empty")
        
        # Check environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"✅ OPENAI_API_KEY found in environment")
            print(f"   Length: {len(api_key)} characters")
        else:
            print("❌ OPENAI_API_KEY not found in environment")
            
        return bool(api_key)
        
    except ImportError:
        print("❌ python-dotenv not available")
        return False
    except Exception as e:
        print(f"❌ Error with direct env access: {e}")
        return False

if __name__ == "__main__":
    config_test = test_env_loading()
    direct_test = test_direct_env_access()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    
    if config_test:
        print("✅ Configuration loading works - API key is available")
    else:
        print("❌ Configuration loading failed - API key not available")
    
    if direct_test:
        print("✅ Direct environment access works")
    else:
        print("❌ Direct environment access failed")
    
    if config_test and direct_test:
        print("\n🎉 SUCCESS: .env file loading is working!")
        print("   The API key should now be available to the trading system.")
    else:
        print("\n❌ ISSUES FOUND: Check .env file and loading mechanism")
