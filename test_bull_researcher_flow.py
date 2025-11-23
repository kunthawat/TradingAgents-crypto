#!/usr/bin/env python3
"""
Test the exact flow that bull_researcher uses to identify the issue
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_bull_researcher_exact_flow():
    """Test the exact flow that bull_researcher.py uses"""
    
    print("Testing Bull Researcher Exact Flow...")
    print("=" * 50)
    
    try:
        # Import exactly as bull_researcher does
        from tradingagents.dataflows.config import get_config
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        
        # Get config exactly as bull_researcher would
        config = get_config()
        
        print(f"✅ Config loaded successfully")
        print(f"   Backend URL: {config.get('backend_url', 'NOT SET')}")
        print(f"   Embeddings URL: {config.get('embeddings_url', 'NOT SET')}")
        print(f"   API Key: {'SET' if config.get('api_key') else 'NOT SET'}")
        
        if not config.get('api_key'):
            print("❌ API key not set - cannot proceed")
            return False
        
        # Create memory exactly as bull_researcher does
        memory = FinancialSituationMemory("bull_memory", config)
        print("✅ Memory created successfully")
        
        # Test the exact call that's failing
        curr_situation = "Test situation for bull researcher"
        print(f"Testing get_memories with: '{curr_situation}'")
        
        try:
            # This is the exact line that's failing in bull_researcher.py line 19
            past_memories = memory.get_memories(curr_situation, n_matches=2)
            print(f"✅ get_memories succeeded! Found {len(past_memories)} memories")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ get_memories failed: {e}")
            
            # Let's debug the exact embedding call
            print("\nDebugging the embedding call...")
            try:
                query_embedding = memory.get_embedding(curr_situation)
                print(f"✅ get_embedding succeeded! Dimensions: {len(query_embedding)}")
                return True
            except Exception as embed_error:
                print(f"❌ get_embedding failed: {embed_error}")
                
                # Check what URL the memory client is actually using
                print(f"\nDebugging client configuration:")
                print(f"   Client base URL: {memory.client.base_url}")
                print(f"   Client API key: {'SET' if memory.client.api_key else 'NOT SET'}")
                print(f"   Embedding model: {memory.embedding}")
                
                return False
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_client_directly():
    """Test the memory client directly to see what's happening"""
    
    print("\nTesting Memory Client Directly...")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.config import get_config
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        import openai
        
        config = get_config()
        
        # Create memory to get the client
        memory = FinancialSituationMemory("debug_memory", config)
        
        print(f"Memory client details:")
        print(f"   Base URL: {memory.client.base_url}")
        print(f"   API Key: {'SET' if memory.client.api_key else 'NOT SET'}")
        print(f"   Embedding model: {memory.embedding}")
        
        # Test the client directly
        test_text = "Test embedding"
        print(f"\nTesting direct client call with: '{test_text}'")
        
        try:
            response = memory.client.embeddings.create(
                model=memory.embedding,
                input=test_text
            )
            print(f"✅ Direct client call succeeded!")
            print(f"   Embedding dimensions: {len(response.data[0].embedding)}")
            return True
            
        except Exception as e:
            print(f"❌ Direct client call failed: {e}")
            
            # Let's try with different URLs to see what works
            print(f"\nTesting different endpoints...")
            
            # Test with backend_url
            try:
                backend_client = openai.OpenAI(
                    api_key=config['api_key'],
                    base_url=config['backend_url']
                )
                response = backend_client.embeddings.create(
                    model=memory.embedding,
                    input=test_text
                )
                print(f"✅ Backend URL call succeeded!")
                return True
            except Exception as backend_error:
                print(f"❌ Backend URL call failed: {backend_error}")
            
            # Test with embeddings_url
            try:
                embeddings_client = openai.OpenAI(
                    api_key=config['api_key'],
                    base_url=config['embeddings_url']
                )
                response = embeddings_client.embeddings.create(
                    model=memory.embedding,
                    input=test_text
                )
                print(f"✅ Embeddings URL call succeeded!")
                return True
            except Exception as embeddings_error:
                print(f"❌ Embeddings URL call failed: {embeddings_error}")
            
            return False
        
    except Exception as e:
        print(f"❌ Client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing the exact bull_researcher flow to identify the 404 error...")
    print("=" * 70)
    
    flow_works = test_bull_researcher_exact_flow()
    client_works = test_memory_client_directly()
    
    print("\n" + "=" * 70)
    print("FINAL DIAGNOSIS:")
    print("=" * 70)
    
    if flow_works:
        print("✅ Bull researcher flow works - issue might be elsewhere")
    else:
        print("❌ Bull researcher flow fails - this is the issue")
    
    if client_works:
        print("✅ Memory client works - configuration is correct")
    else:
        print("❌ Memory client fails - configuration issue detected")
    
    if not flow_works or not client_works:
        print("\n🔍 The issue has been identified in the memory system.")
        print("   Need to fix the memory client configuration.")
    else:
        print("\n🤔 The issue might be in a different part of the system.")
        print("   Need to investigate further.")
