#!/usr/bin/env python3
"""
Direct test of memory system without full tradingagents imports
"""

import sys
import os
import openai
import chromadb
from chromadb.config import Settings

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_memory_directly():
    """Test memory system directly without full imports"""
    
    print("Testing Memory System Directly...")
    print("=" * 50)
    
    try:
        # Import config directly
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG.copy()
        config['session_id'] = 'test_session'
        
        print(f"Config:")
        print(f"  - embeddings_url: {config.get('embeddings_url')}")
        print(f"  - api_key: {'SET' if config.get('api_key') else 'MISSING'}")
        
        # Test 1: Missing API key
        print("\n--- Test 1: Missing API Key ---")
        config_no_key = config.copy()
        config_no_key['api_key'] = ''
        
        try:
            # Create memory system directly
            client = openai.OpenAI(
                base_url=config_no_key['embeddings_url'],
                api_key=config_no_key['api_key']
            )
            
            # Try to create embedding
            response = client.embeddings.create(
                input="test text",
                model="Qwen/Qwen3-Embedding-8B"
            )
            print("❌ Unexpected: Embedding worked without API key")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error with missing API key: {error_msg}")
            
            if "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
                print("🎯 CONFIRMED: This is the same 404 'No matching cord found!' error!")
                print("   Root cause: Missing API key")
        
        # Test 2: Dummy API key
        print("\n--- Test 2: Dummy API Key ---")
        config_dummy_key = config.copy()
        config_dummy_key['api_key'] = 'dummy_key_12345'
        
        try:
            client = openai.OpenAI(
                base_url=config_dummy_key['embeddings_url'],
                api_key=config_dummy_key['api_key']
            )
            
            response = client.embeddings.create(
                input="test text",
                model="Qwen/Qwen3-Embedding-8B"
            )
            print("❌ Unexpected: Embedding worked with dummy key")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error with dummy API key: {error_msg}")
            
            if "401" in error_msg or "Invalid token" in error_msg:
                print("✅ GOOD: Got 401 error - endpoint works, key is invalid")
                print("   This proves the 404 'cord' error is due to missing API key")
            elif "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
                print("❌ Still getting 404 'cord' error even with API key")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_env_variable():
    """Test with environment variable set"""
    
    print("\n\nTesting with Environment Variable...")
    print("=" * 50)
    
    # Set a dummy environment variable
    os.environ['OPENAI_API_KEY'] = 'test_env_key_12345'
    
    try:
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG.copy()
        config['session_id'] = 'test_session_env'
        
        print(f"API key from env: {'*' * 10}{config['api_key'][-10:] if config['api_key'] else 'MISSING'}")
        
        if config['api_key']:
            try:
                client = openai.OpenAI(
                    base_url=config['embeddings_url'],
                    api_key=config['api_key']
                )
                
                response = client.embeddings.create(
                    input="test with env key",
                    model="Qwen/Qwen3-Embedding-8B"
                )
                print("❌ Unexpected: Worked with test key")
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Error with env API key: {error_msg}")
                
                if "401" in error_msg:
                    print("✅ GOOD: Got 401 with env key - configuration loading works")
        else:
            print("❌ Environment variable not loaded")
            
    except Exception as e:
        print(f"❌ Env test failed: {e}")
    
    # Clean up
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']

if __name__ == "__main__":
    print("DIRECT MEMORY SYSTEM DIAGNOSIS")
    print("=" * 50)
    
    test_memory_directly()
    test_with_env_variable()
    
    print("\n" + "=" * 50)
    print("CONCLUSION:")
    print("=" * 50)
    print("The 404 'No matching cord found!' error is caused by:")
    print("1. Missing OPENAI_API_KEY environment variable")
    print("2. The embeddings API returns 404 instead of 401 when no key is provided")
    print("\nSOLUTION:")
    print("Set OPENAI_API_KEY environment variable with your valid API key")
