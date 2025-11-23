#!/usr/bin/env python3
"""
Test the web application API key flow to identify the exact issue
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_web_config_flow():
    """Test how the web application handles API keys"""
    
    print("TESTING WEB APPLICATION API KEY FLOW")
    print("=" * 60)
    
    try:
        # Import the web app configuration
        from tradingagents.default_config import DEFAULT_CONFIG
        
        print("1. DEFAULT_CONFIG (from environment):")
        print(f"   - api_key: {'SET' if DEFAULT_CONFIG.get('api_key') else 'MISSING'}")
        print(f"   - embeddings_url: {DEFAULT_CONFIG.get('embeddings_url')}")
        
        # Simulate what the web app does when it receives form data
        print("\n2. Simulating Web App Form Submission:")
        
        # This is what the web app does in run_analysis_background()
        web_form_data = {
            'api_key': 'user_provided_api_key_12345',  # From the HTML form
            'backend_url': 'https://llm.chutes.ai/v1',
            'session_id': 'test_session_123'
        }
        
        # This is how the web app updates the config
        updated_config = DEFAULT_CONFIG.copy()
        updated_config.update({
            'api_key': web_form_data.get('api_key', ''),
            'backend_url': web_form_data['backend_url'],
            'session_id': web_form_data['session_id']
        })
        
        print(f"   - api_key from form: {'SET' if updated_config.get('api_key') else 'MISSING'}")
        print(f"   - api_key value: {'*' * 10}{updated_config['api_key'][-10:] if updated_config['api_key'] else 'NONE'}")
        
        # Test memory system with this config
        print("\n3. Testing Memory System with Web Config:")
        
        try:
            from tradingagents.agents.utils.memory import FinancialSituationMemory
            
            # Create memory system with web-updated config
            memory = FinancialSituationMemory("test_memory", updated_config)
            print("   ✅ Memory system created with web config")
            
            # Test embedding generation
            test_text = "Test embedding with web API key"
            try:
                embedding = memory.get_embedding(test_text)
                print(f"   ✅ Embedding generated: {len(embedding)} dimensions")
                print("   🎉 SUCCESS: Web API key flow works!")
                return True
                
            except Exception as e:
                error_msg = str(e)
                print(f"   ❌ Embedding failed: {error_msg}")
                
                if "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
                    print("   🎯 This is the original 404 'No matching cord found!' error!")
                    print("   ❌ The web API key is not being used properly")
                elif "401" in error_msg or "Invalid token" in error_msg:
                    print("   ✅ Good: Got 401 error - web API key is being used")
                    print("   ✅ The endpoint and model are correct")
                else:
                    print(f"   ⚠️  Different error: {error_msg}")
                
                return False
                
        except Exception as e:
            print(f"   ❌ Memory system creation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_vs_form_key():
    """Test environment variable vs form-provided API key"""
    
    print("\n\nTESTING ENVIRONMENT VS FORM API KEY")
    print("=" * 60)
    
    # Store original
    original_env_key = os.getenv('OPENAI_API_KEY', '')
    
    try:
        # Test 1: No environment key, no form key
        print("--- Test 1: No API Key Anywhere ---")
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        # Reload config to pick up missing env key
        import importlib
        import tradingagents.default_config
        importlib.reload(tradingagents.default_config)
        
        from tradingagents.default_config import DEFAULT_CONFIG
        config_no_key = DEFAULT_CONFIG.copy()
        
        print(f"   Environment key: {'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING'}")
        print(f"   Config key: {'SET' if config_no_key.get('api_key') else 'MISSING'}")
        
        # Test 2: Form key provided
        print("\n--- Test 2: Form API Key Provided ---")
        config_with_form_key = config_no_key.copy()
        config_with_form_key['api_key'] = 'form_provided_key_67890'
        
        print(f"   Form key: {'SET' if config_with_form_key.get('api_key') else 'MISSING'}")
        print(f"   Form key value: {'*' * 10}{config_with_form_key['api_key'][-10:]}")
        
        # Test memory system with form key
        try:
            from tradingagents.agents.utils.memory import FinancialSituationMemory
            memory = FinancialSituationMemory("test_form_key", config_with_form_key)
            print("   ✅ Memory system created with form key")
            
            # Try embedding
            embedding = memory.get_embedding("test with form key")
            print(f"   ✅ Embedding worked: {len(embedding)} dimensions")
            print("   🎉 FORM KEY WORKS!")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ Form key test failed: {error_msg}")
            
            if "401" in error_msg:
                print("   ✅ Good: Form key is being used (got 401 with test key)")
            elif "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
                print("   ❌ Still getting 404 - form key not working")
            return False
            
    except Exception as e:
        print(f"❌ Environment vs form test failed: {e}")
        return False
    
    finally:
        # Restore original
        if original_env_key:
            os.environ['OPENAI_API_KEY'] = original_env_key

if __name__ == "__main__":
    print("WEB APPLICATION API KEY FLOW DIAGNOSIS")
    print("=" * 60)
    
    web_flow_works = test_web_config_flow()
    env_vs_form_works = test_environment_vs_form_key()
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    if web_flow_works:
        print("✅ Web API key flow works correctly")
        print("   The form API key should work in the web application")
    else:
        print("❌ Web API key flow has issues")
        print("   The form API key is not being used properly")
    
    if env_vs_form_works:
        print("✅ Form API key works when provided")
        print("   The memory system can use form-provided keys")
    else:
        print("❌ Form API key doesn't work")
        print("   There's a deeper issue with API key handling")
    
    print("\n🔧 CONCLUSION:")
    if web_flow_works and env_vs_form_works:
        print("✅ The web application should work with form API keys")
        print("   If you're still getting 404 errors, check:")
        print("   1. The API key is entered correctly in the form")
        print("   2. The API key is valid and active")
        print("   3. No network issues blocking the API")
    else:
        print("❌ There's a technical issue with API key handling")
        print("   The memory system may need to be fixed")
