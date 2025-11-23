#!/usr/bin/env python3
"""
Test memory system directly without going through dataflows package
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_memory_isolated():
    """Test memory system in isolation"""
    
    print("Testing Memory System in Isolation...")
    print("=" * 50)
    
    try:
        # Import config directly
        import tradingagents.default_config as default_config
        
        # Import memory directly
        sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto/tradingagents/agents/utils')
        import memory
        
        config = default_config.DEFAULT_CONFIG
        
        print(f"✅ Config loaded directly")
        print(f"   Backend URL: {config.get('backend_url', 'NOT SET')}")
        print(f"   Embeddings URL: {config.get('embeddings_url', 'NOT SET')}")
        print(f"   API Key: {'SET' if config.get('api_key') else 'NOT SET'}")
        
        if not config.get('api_key'):
            print("❌ API key not set - cannot proceed")
            return False
        
        # Create memory directly
        memory_instance = memory.FinancialSituationMemory("bull_memory", config)
        print("✅ Memory created successfully")
        
        # Check what URL the memory client is actually using
        print(f"\nMemory client details:")
        print(f"   Base URL: {memory_instance.client.base_url}")
        print(f"   API Key: {'SET' if memory_instance.client.api_key else 'NOT SET'}")
        print(f"   Embedding model: {memory_instance.embedding}")
        
        # Test the exact call that's failing
        curr_situation = "Test situation for bull researcher"
        print(f"\nTesting get_memories with: '{curr_situation}'")
        
        try:
            # This is the exact line that's failing in bull_researcher.py line 19
            past_memories = memory_instance.get_memories(curr_situation, n_matches=2)
            print(f"✅ get_memories succeeded! Found {len(past_memories)} memories")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ get_memories failed: {e}")
            
            # Let's debug the exact embedding call
            print("\nDebugging the embedding call...")
            try:
                query_embedding = memory_instance.get_embedding(curr_situation)
                print(f"✅ get_embedding succeeded! Dimensions: {len(query_embedding)}")
                return True
            except Exception as embed_error:
                print(f"❌ get_embedding failed: {embed_error}")
                
                # Check if it's the 404 error we're trying to fix
                if "404" in str(embed_error) and "cord" in str(embed_error):
                    print("🎯 FOUND THE ISSUE: This is the exact 404 'No matching cord found!' error!")
                    print("   The memory system is still using the wrong endpoint or model.")
                    return False
                else:
                    print("   This is a different error - might be authentication related")
                    return True  # Different error means the 404 is fixed
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_with_different_configs():
    """Test memory with different configuration scenarios"""
    
    print("\nTesting Memory with Different Configurations...")
    print("=" * 50)
    
    try:
        import tradingagents.default_config as default_config
        sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto/tradingagents/agents/utils')
        import memory
        
        config = default_config.DEFAULT_CONFIG
        
        # Test 1: Current configuration
        print("Test 1: Current configuration")
        try:
            memory1 = memory.FinancialSituationMemory("test1", config)
            print(f"   ✅ Memory created with URL: {memory1.client.base_url}")
            print(f"   ✅ Using model: {memory1.embedding}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # Test 2: Force backend_url instead of embeddings_url
        print("\nTest 2: Using backend_url instead of embeddings_url")
        config_backend_only = config.copy()
        config_backend_only.pop('embeddings_url', None)
        try:
            memory2 = memory.FinancialSituationMemory("test2", config_backend_only)
            print(f"   ✅ Memory created with URL: {memory2.client.base_url}")
            print(f"   ✅ Using model: {memory2.embedding}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # Test 3: Test with different model names
        print("\nTest 3: Testing different model names")
        test_models = [
            "Qwen/Qwen3-Embedding-8B",
            "text-embedding-ada-002",
            "text-embedding-3-small"
        ]
        
        for model in test_models:
            try:
                # Temporarily modify the memory instance to test different models
                memory_test = memory.FinancialSituationMemory("test_model", config)
                original_model = memory_test.embedding
                memory_test.embedding = model
                
                print(f"   Testing model: {model}")
                response = memory_test.client.embeddings.create(
                    model=model,
                    input="test"
                )
                print(f"   ✅ Model {model} works!")
                
            except Exception as e:
                print(f"   ❌ Model {model} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing memory system in isolation to identify the 404 error...")
    print("=" * 70)
    
    isolated_works = test_memory_isolated()
    config_works = test_memory_with_different_configs()
    
    print("\n" + "=" * 70)
    print("FINAL DIAGNOSIS:")
    print("=" * 70)
    
    if isolated_works:
        print("✅ Memory system works in isolation")
        print("   The issue might be in the configuration loading or deployment")
    else:
        print("❌ Memory system fails in isolation")
        print("   This confirms the issue is in the memory system itself")
    
    if config_works:
        print("✅ Configuration tests completed")
    else:
        print("❌ Configuration tests failed")
    
    print("\n🔍 Next steps:")
    if not isolated_works:
        print("   1. Fix the memory system configuration")
        print("   2. Ensure correct endpoint and model are used")
    else:
        print("   1. Check deployment environment")
        print("   2. Verify running code matches local code")
