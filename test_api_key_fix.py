#!/usr/bin/env python3
"""
Test that the API key is properly loaded and embeddings work with authentication
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_api_key_loading():
    """Test that the API key is properly loaded into configuration"""
    
    print("Testing API Key Loading...")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.config import get_config
        config = get_config()
        
        print("✅ Configuration loaded successfully")
        print(f"Backend URL: {config.get('backend_url', 'NOT FOUND')}")
        print(f"Embeddings URL: {config.get('embeddings_url', 'NOT FOUND')}")
        print(f"API Key: {'SET' if config.get('api_key') else 'NOT SET'}")
        
        if 'api_key' in config and config['api_key']:
            print("✅ API key is present in configuration")
            return config['api_key']
        else:
            print("❌ API key is missing from configuration")
            print("   Make sure OPENAI_API_KEY environment variable is set")
            return None
            
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_embeddings_with_auth():
    """Test embeddings API with proper authentication"""
    
    print("\nTesting Embeddings API with Authentication...")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.config import get_config
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        
        config = get_config()
        
        if not config.get('api_key'):
            print("❌ Cannot test embeddings - API key not set")
            print("   Set OPENAI_API_KEY environment variable to test")
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
            elif "404" in error_msg and "cord" in error_msg:
                print(f"❌ Model/endpoint issue: {e}")
                print("   The model name or endpoint URL may be incorrect")
                return False
            else:
                print(f"⚠️  Other error: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_retrieval():
    """Test the full memory retrieval system"""
    
    print("\nTesting Memory Retrieval System...")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.config import get_config
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        
        config = get_config()
        
        if not config.get('api_key'):
            print("❌ Cannot test memory retrieval - API key not set")
            return False
        
        # Initialize memory
        memory = FinancialSituationMemory("test_retrieval", config)
        
        # Add some test data
        test_data = [
            ("Market is bullish with strong tech sector performance", "Buy tech stocks and increase exposure"),
            ("High inflation concerns with rising interest rates", "Focus on defensive sectors and reduce risk"),
        ]
        
        memory.add_situations(test_data)
        print("✅ Test data added to memory")
        
        # Test retrieval
        query = "Tech stocks are performing well with market optimism"
        try:
            results = memory.get_memories(query, n_matches=1)
            print(f"✅ Memory retrieval successful!")
            print(f"   Found {len(results)} matches")
            if results:
                print(f"   Similarity: {results[0]['similarity_score']:.3f}")
                print(f"   Recommendation: {results[0]['recommendation']}")
            return True
        except Exception as e:
            print(f"❌ Memory retrieval failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    api_key = test_api_key_loading()
    embeddings_work = test_embeddings_with_auth()
    memory_works = test_memory_retrieval()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    
    if api_key:
        print(f"✅ API key loaded: {'*' * 10}{api_key[-10:] if len(api_key) > 10 else api_key}")
    else:
        print("❌ API key not loaded - set OPENAI_API_KEY environment variable")
    
    if embeddings_work:
        print("✅ Embeddings API working with authentication")
    else:
        print("❌ Embeddings API not working")
    
    if memory_works:
        print("✅ Memory retrieval system working")
    else:
        print("❌ Memory retrieval system not working")
    
    if api_key and embeddings_work and memory_works:
        print("\n🎉 SUCCESS: All systems working!")
        print("The 404 'No matching cord found!' error should be resolved.")
    else:
        print("\n❌ Issues remain - check the errors above")
