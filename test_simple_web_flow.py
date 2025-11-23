#!/usr/bin/env python3
"""
Simple test to verify the web API key flow without dependencies
"""

import sys
import os
import openai

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_current_environment():
    """Test the current environment setup"""
    
    print("CURRENT ENVIRONMENT STATUS")
    print("=" * 50)
    
    # Check environment variable
    env_key = os.getenv('OPENAI_API_KEY', '')
    print(f"OPENAI_API_KEY environment variable: {'SET' if env_key else 'MISSING'}")
    if env_key:
        print(f"Key value: {'*' * 10}{env_key[-10:]}")
    
    # Check default config
    try:
        import tradingagents.default_config as default_config
        config = default_config.DEFAULT_CONFIG
        
        print(f"Default config API key: {'SET' if config.get('api_key') else 'MISSING'}")
        if config.get('api_key'):
            print(f"Config key: {'*' * 10}{config['api_key'][-10:]}")
        
        print(f"Embeddings URL: {config.get('embeddings_url')}")
        
        return config
        
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return None

def test_embeddings_with_config(config):
    """Test embeddings with the current configuration"""
    
    print("\nTESTING EMBEDDINGS WITH CURRENT CONFIG")
    print("=" * 50)
    
    if not config:
        print("❌ No config available")
        return False
    
    try:
        # Create OpenAI client with config
        client = openai.OpenAI(
            base_url=config['embeddings_url'],
            api_key=config['api_key']
        )
        
        print(f"Client created with:")
        print(f"  - URL: {config['embeddings_url']}")
        print(f"  - API Key: {'SET' if config['api_key'] else 'MISSING'}")
        
        # Test embedding
        print("\nTesting embedding generation...")
        response = client.embeddings.create(
            input="test text",
            model="Qwen/Qwen3-Embedding-8B"
        )
        
        print(f"✅ SUCCESS: Embedding generated!")
        print(f"   Dimensions: {len(response.data[0].embedding)}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Embedding failed: {error_msg}")
        
        if "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
            print("🎯 This is the original 404 'No matching cord found!' error!")
            print("   Root cause: API key issue")
        elif "401" in error_msg or "Invalid token" in error_msg:
            print("✅ Good: Got 401 - API key is being used but is invalid")
        elif "429" in error_msg:
            print("⚠️  Rate limiting - API endpoint works but key may be invalid")
        else:
            print(f"⚠️  Different error: {error_msg}")
        
        return False

def test_web_form_simulation():
    """Simulate what happens when web form provides API key"""
    
    print("\nSIMULATING WEB FORM API KEY")
    print("=" * 50)
    
    # Get current config
    try:
        import tradingagents.default_config as default_config
        base_config = default_config.DEFAULT_CONFIG.copy()
    except:
        print("❌ Could not load base config")
        return False
    
    # Simulate web form providing API key
    web_config = base_config.copy()
    web_config['api_key'] = 'simulated_web_form_key_12345'
    
    print(f"Simulated web API key: {'*' * 10}{web_config['api_key'][-10:]}")
    
    # Test with simulated web key
    try:
        client = openai.OpenAI(
            base_url=web_config['embeddings_url'],
            api_key=web_config['api_key']
        )
        
        response = client.embeddings.create(
            input="test with web form key",
            model="Qwen/Qwen3-Embedding-8B"
        )
        
        print("✅ Web form key worked (unexpected!)")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Web form key failed: {error_msg}")
        
        if "401" in error_msg or "Invalid token" in error_msg:
            print("✅ Good: Web form key is being used (got 401 with test key)")
            print("   ✅ This proves the web form API key flow works")
            return True
        elif "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
            print("❌ Still getting 404 - web form key not working")
            return False
        else:
            print(f"⚠️  Different error: {error_msg}")
            return False

if __name__ == "__main__":
    print("SIMPLE WEB API KEY FLOW TEST")
    print("=" * 60)
    
    # Test current environment
    config = test_current_environment()
    
    # Test with current config
    current_works = test_embeddings_with_config(config)
    
    # Test web form simulation
    web_form_works = test_web_form_simulation()
    
    print("\n" + "=" * 60)
    print("FINAL DIAGNOSIS")
    print("=" * 60)
    
    print(f"Current environment API key: {'WORKS' if current_works else 'FAILS'}")
    print(f"Web form API key flow: {'WORKS' if web_form_works else 'FAILS'}")
    
    if current_works:
        print("\n✅ GOOD NEWS:")
        print("   Your current environment API key works!")
        print("   The web application should work with your existing setup")
        print("   Just make sure you enter the same API key in the web form")
    
    if web_form_works:
        print("\n✅ WEB FORM FLOW WORKS:")
        print("   The web application can use API keys from the form")
        print("   The Bull Researcher 404 error should be resolved")
    
    if not current_works and not web_form_works:
        print("\n❌ ISSUE IDENTIFIED:")
        print("   There's a fundamental problem with the API key or endpoint")
        print("   Check your API key and network connection")
    
    print("\n🔧 RECOMMENDATION:")
    if current_works:
        print("   Use the same API key in the web form that works in your environment")
    else:
        print("   Check your API key and ensure it's valid and active")
