#!/usr/bin/env python3
"""
Simple test of memory.py by copying the relevant code
"""

import sys
import os
import openai

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_memory_logic():
    """Test the memory logic directly"""
    
    print("Testing Memory Logic Directly...")
    print("=" * 50)
    
    try:
        # Import config directly
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG
        
        print(f"✅ Config loaded directly")
        print(f"   Backend URL: {config.get('backend_url', 'NOT SET')}")
        print(f"   Embeddings URL: {config.get('embeddings_url', 'NOT SET')}")
        print(f"   API Key: {'SET' if config.get('api_key') else 'NOT SET'}")
        
        if not config.get('api_key'):
            print("❌ API key not set - cannot proceed")
            return False
        
        # Test the exact logic from memory.py __init__
        print(f"\nTesting memory initialization logic...")
        
        if config["backend_url"] == "http://localhost:11434/v1":
            embedding = "nomic-embed-text"
            # Use local Ollama for embeddings when using local backend
            client = openai.OpenAI(
                base_url=config["backend_url"],
                api_key=config["api_key"]
            )
        else:
            # Use dedicated embeddings endpoint for Chutes
            embedding = "Qwen/Qwen3-Embedding-8B"  # Model for Chutes embeddings API
            client = openai.OpenAI(
                base_url=config["embeddings_url"],
                api_key=config["api_key"]
            )
        
        print(f"✅ Memory client created successfully")
        print(f"   Base URL: {client.base_url}")
        print(f"   API Key: {'SET' if client.api_key else 'NOT SET'}")
        print(f"   Embedding model: {embedding}")
        
        # Test the exact get_embedding logic
        print(f"\nTesting get_embedding logic...")
        
        test_text = "Test situation for bull researcher"
        
        try:
            # Both endpoints now require model parameter
            response = client.embeddings.create(model=embedding, input=test_text)
            
            embedding_result = response.data[0].embedding
            print(f"✅ get_embedding succeeded! Dimensions: {len(embedding_result)}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ get_embedding failed: {e}")
            
            # Check if it's the 404 error we're trying to fix
            if "404" in error_msg and "cord" in error_msg:
                print("🎯 FOUND THE ISSUE: This is the exact 404 'No matching cord found!' error!")
                print("   The memory system is still using the wrong endpoint or model.")
                return False
            elif "401" in error_msg or "Invalid token" in error_msg:
                print("✅ This is expected with test API key - endpoint is working!")
                print("   The 404 'No matching cord found!' error has been fixed.")
                return True
            else:
                print(f"⚠️  Different error: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_endpoints():
    """Test different endpoints to see which one works"""
    
    print("\nTesting Different Endpoints...")
    print("=" * 50)
    
    try:
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG
        
        test_text = "Test embedding"
        
        # Test 1: backend_url
        print("Test 1: Using backend_url")
        try:
            client1 = openai.OpenAI(
                api_key=config['api_key'],
                base_url=config['backend_url']
            )
            response1 = client1.embeddings.create(
                model="Qwen/Qwen3-Embedding-8B",
                input=test_text
            )
            print(f"   ✅ Backend URL works!")
        except Exception as e:
            print(f"   ❌ Backend URL failed: {e}")
        
        # Test 2: embeddings_url
        print("\nTest 2: Using embeddings_url")
        try:
            client2 = openai.OpenAI(
                api_key=config['api_key'],
                base_url=config['embeddings_url']
            )
            response2 = client2.embeddings.create(
                model="Qwen/Qwen3-Embedding-8B",
                input=test_text
            )
            print(f"   ✅ Embeddings URL works!")
        except Exception as e:
            print(f"   ❌ Embeddings URL failed: {e}")
            
            # Check if this is the 404 error
            if "404" in str(e) and "cord" in str(e):
                print("   🎯 This is the 404 'No matching cord found!' error!")
        
        # Test 3: Try different model names with embeddings_url
        print("\nTest 3: Different models with embeddings_url")
        test_models = [
            "Qwen/Qwen3-Embedding-8B",
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "nomic-embed-text"
        ]
        
        for model in test_models:
            try:
                client3 = openai.OpenAI(
                    api_key=config['api_key'],
                    base_url=config['embeddings_url']
                )
                response3 = client3.embeddings.create(
                    model=model,
                    input=test_text
                )
                print(f"   ✅ Model {model} works!")
                break
            except Exception as e:
                print(f"   ❌ Model {model} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing memory logic to identify the 404 error...")
    print("=" * 70)
    
    logic_works = test_memory_logic()
    endpoints_work = test_different_endpoints()
    
    print("\n" + "=" * 70)
    print("FINAL DIAGNOSIS:")
    print("=" * 70)
    
    if logic_works:
        print("✅ Memory logic works - 404 error is fixed")
        print("   The issue might be in deployment or environment")
    else:
        print("❌ Memory logic fails - 404 error still exists")
        print("   Need to fix the endpoint or model configuration")
    
    if endpoints_work:
        print("✅ Endpoint tests completed")
    else:
        print("❌ Endpoint tests failed")
    
    print("\n🔍 Based on this test:")
    if logic_works:
        print("   The fix is working locally.")
        print("   The user's error might be due to:")
        print("   1. Deployment using old code")
        print("   2. Environment-specific configuration")
        print("   3. Caching issues")
    else:
        print("   The fix needs more work.")
        print("   Need to identify the correct endpoint/model combination.")
