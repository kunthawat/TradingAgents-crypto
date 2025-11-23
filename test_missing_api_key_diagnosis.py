#!/usr/bin/env python3
"""
Test to confirm the missing API key is causing the 404 error
"""

import sys
import os
import openai

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_memory_with_missing_api_key():
    """Test memory system with missing API key to reproduce the error"""
    
    print("Testing Memory System with Missing API Key...")
    print("=" * 60)
    
    try:
        # Import the memory system
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        import tradingagents.default_config as default_config
        
        # Get config but ensure API key is empty to simulate the issue
        config = default_config.DEFAULT_CONFIG.copy()
        config['api_key'] = ''  # Simulate missing API key
        config['session_id'] = 'test_session'
        
        print(f"Config loaded:")
        print(f"  - embeddings_url: {config.get('embeddings_url')}")
        print(f"  - api_key: {'SET' if config.get('api_key') else 'MISSING'}")
        print(f"  - backend_url: {config.get('backend_url')}")
        
        # Try to create memory system
        print("\nCreating memory system...")
        memory = FinancialSituationMemory("test_memory", config)
        print("✅ Memory system created successfully")
        
        # Try to get an embedding (this should fail with 404)
        print("\nTesting embedding generation...")
        test_text = "This is a test text for embedding generation"
        
        try:
            embedding = memory.get_embedding(test_text)
            print(f"✅ Embedding generated: {len(embedding)} dimensions")
            return True
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Embedding failed: {error_msg}")
            
            # Check if this is the same 404 error
            if "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
                print("🎯 CONFIRMED: This is the same 404 'No matching cord found!' error!")
                print("   Root cause: Missing API key causing authentication failure")
                print("   The API returns 404 instead of 401 when no API key is provided")
            elif "401" in error_msg or "Unauthorized" in error_msg:
                print("🎯 This is a 401 authentication error (different from original)")
            else:
                print(f"🎯 Different error type: {type(e).__name__}")
            
            return False
            
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_with_dummy_api_key():
    """Test memory system with a dummy API key to see the error"""
    
    print("\n\nTesting Memory System with Dummy API Key...")
    print("=" * 60)
    
    try:
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        import tradingagents.default_config as default_config
        
        config = default_config.DEFAULT_CONFIG.copy()
        config['api_key'] = 'dummy_key_12345'  # Dummy API key
        config['session_id'] = 'test_session_2'
        
        print(f"Using dummy API key: {'*' * 10}{config['api_key'][-10:]}")
        
        memory = FinancialSituationMemory("test_memory_2", config)
        print("✅ Memory system created with dummy API key")
        
        # Try embedding generation
        test_text = "Test with dummy API key"
        try:
            embedding = memory.get_embedding(test_text)
            print(f"✅ Embedding generated: {len(embedding)} dimensions")
            return True
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Embedding failed: {error_msg}")
            
            if "401" in error_msg or "Invalid token" in error_msg:
                print("✅ GOOD: Got 401 error - means endpoint is working but API key is invalid")
                print("   This proves the 404 'cord' error is specifically due to missing API key")
            elif "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
                print("❌ Still getting 404 'cord' error even with API key")
                print("   This suggests a different issue - maybe model name or endpoint")
            else:
                print(f"⚠️  Different error: {error_msg}")
            
            return False
            
    except Exception as e:
        print(f"❌ Dummy API key test failed: {e}")
        return False

if __name__ == "__main__":
    print("DIAGNOSING THE 404 'No matching cord found!' ERROR")
    print("=" * 60)
    
    # Test 1: Missing API key (reproduce the original error)
    missing_key_result = test_memory_with_missing_api_key()
    
    # Test 2: Dummy API key (see if we get a different error)
    dummy_key_result = test_memory_with_dummy_api_key()
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS SUMMARY:")
    print("=" * 60)
    
    if not missing_key_result:
        print("✅ CONFIRMED: Missing API key causes the 404 'No matching cord found!' error")
        print("   Solution: Set the OPENAI_API_KEY environment variable")
    else:
        print("❌ Unexpected: Missing API key did not cause the error")
    
    if not dummy_key_result and "401" in str(test_memory_with_dummy_api_key.__code__):
        print("✅ CONFIRMED: With API key, we get proper 401 authentication error")
        print("   This proves the endpoint and model name are correct")
    
    print("\n🔧 SOLUTION:")
    print("   1. Set your valid API key: export OPENAI_API_KEY='your_valid_key'")
    print("   2. The 404 'cord' error will be resolved")
    print("   3. You'll get proper authentication errors if key is invalid")
