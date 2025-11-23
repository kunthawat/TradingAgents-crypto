#!/usr/bin/env python3
"""
Debug the exact memory logic to see which path it takes
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def debug_memory_logic():
    """Debug exactly which path the memory logic takes"""
    
    print("Debugging Memory Logic...")
    print("=" * 50)
    
    try:
        # Import config directly
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG
        
        print(f"Configuration values:")
        print(f"   backend_url: {config['backend_url']}")
        print(f"   embeddings_url: {config['embeddings_url']}")
        print(f"   api_key set: {'Yes' if config['api_key'] else 'No'}")
        
        # Test the exact condition from memory.py
        print(f"\nTesting the condition:")
        print(f"   config['backend_url'] == 'http://localhost:11434/v1'")
        print(f"   '{config['backend_url']}' == 'http://localhost:11434/v1'")
        print(f"   Result: {config['backend_url'] == 'http://localhost:11434/v1'}")
        
        if config["backend_url"] == "http://localhost:11434/v1":
            print(f"\n📍 Taking LOCALHOST path:")
            embedding = "nomic-embed-text"
            base_url = config["backend_url"]
            print(f"   embedding: {embedding}")
            print(f"   base_url: {base_url}")
        else:
            print(f"\n📍 Taking CHUTES path:")
            embedding = "Qwen/Qwen3-Embedding-8B"
            base_url = config["embeddings_url"]
            print(f"   embedding: {embedding}")
            print(f"   base_url: {base_url}")
        
        # Test what URL would actually be used
        print(f"\n🎯 Final configuration:")
        print(f"   URL that will be used: {base_url}")
        print(f"   Model that will be used: {embedding}")
        
        # Test the actual API call
        import openai
        
        print(f"\nTesting API call to: {base_url}")
        client = openai.OpenAI(
            base_url=base_url,
            api_key=config['api_key']
        )
        
        try:
            response = client.embeddings.create(model=embedding, input="test")
            print(f"✅ SUCCESS: API call worked!")
            print(f"   Embedding dimensions: {len(response.data[0].embedding)}")
        except Exception as e:
            error_msg = str(e)
            print(f"❌ API call failed: {e}")
            
            if "404" in error_msg and "cord" in error_msg:
                print(f"🎯 This is the original 404 'No matching cord found!' error!")
                print(f"   This means we're still hitting the wrong endpoint.")
            elif "401" in error_msg or "Invalid token" in error_msg:
                print(f"✅ This is expected - endpoint is working but auth failed")
                print(f"   The 404 error has been fixed!")
            else:
                print(f"⚠️  Different error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Debugging the exact memory logic path...")
    print("=" * 70)
    
    debug_memory_logic()
    
    print("\n" + "=" * 70)
    print("CONCLUSION:")
    print("=" * 70)
    print("If the test above shows:")
    print("✅ 'Taking CHUTES path' and gets 401 error -> Fix is working")
    print("❌ 'Taking CHUTES path' and gets 404 error -> Still broken")
    print("❌ 'Taking LOCALHOST path' -> Wrong configuration detected")
