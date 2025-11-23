#!/usr/bin/env python3
"""
Simple test to check if API key is loaded in configuration
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_config_directly():
    """Test configuration directly without importing dataflows"""
    
    print("Testing Configuration Directly...")
    print("=" * 50)
    
    try:
        # Import default config directly
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG
        
        print("✅ Default configuration loaded successfully")
        print(f"Backend URL: {config.get('backend_url', 'NOT FOUND')}")
        print(f"Embeddings URL: {config.get('embeddings_url', 'NOT FOUND')}")
        print(f"API Key: {'SET' if config.get('api_key') else 'NOT SET'}")
        
        if 'api_key' in config and config['api_key']:
            print("✅ API key is present in configuration")
            print(f"   API Key (last 10): {'*' * 10}{config['api_key'][-10:] if len(config['api_key']) > 10 else config['api_key']}")
            return config['api_key']
        else:
            print("❌ API key is missing from configuration")
            print("   Make sure OPENAI_API_KEY environment variable is set")
            print(f"   Current OPENAI_API_KEY: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
            return None
            
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_memory_directly():
    """Test memory system with direct configuration"""
    
    print("\nTesting Memory System Directly...")
    print("=" * 50)
    
    try:
        # Import directly
        import tradingagents.default_config as default_config
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        
        config = default_config.DEFAULT_CONFIG
        
        if not config.get('api_key'):
            print("❌ Cannot test memory - API key not set")
            return False
        
        print(f"Using embeddings URL: {config.get('embeddings_url')}")
        print(f"Using model: Qwen/Qwen3-Embedding-8B")
        
        # Test memory initialization
        memory = FinancialSituationMemory("test_memory", config)
        print("✅ Memory system initialized with API key")
        
        # Test embedding generation
        test_text = "This is a test for embeddings API"
        try:
            embedding = memory.get_embedding(test_text)
            print(f"✅ Embedding generated successfully!")
            print(f"   Dimensions: {len(embedding)}")
            print(f"   First 5 values: {embedding[:5]}")
            return True
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                print(f"❌ Authentication failed: {e}")
                print("   The API key may be invalid or expired")
                return False
            elif "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
                print(f"❌ Model/endpoint issue: {e}")
                print("   The model name or endpoint URL may be incorrect")
                return False
            else:
                print(f"⚠️  Other error: {e}")
                import traceback
                traceback.print_exc()
                return False
        
    except Exception as e:
        print(f"❌ Memory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    api_key = test_config_directly()
    memory_works = test_memory_directly()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    
    if api_key:
        print(f"✅ API key loaded: {'*' * 10}{api_key[-10:] if len(api_key) > 10 else api_key}")
    else:
        print("❌ API key not loaded - set OPENAI_API_KEY environment variable")
    
    if memory_works:
        print("✅ Memory system working")
    else:
        print("❌ Memory system not working")
    
    if api_key and memory_works:
        print("\n🎉 SUCCESS: Configuration and memory system working!")
        print("The 404 'No matching cord found!' error should be resolved.")
    else:
        print("\n❌ Issues remain - check the errors above")
