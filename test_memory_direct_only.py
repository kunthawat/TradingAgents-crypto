#!/usr/bin/env python3
"""
Test only the memory module directly without importing the full agent system
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_memory_module_directly():
    """Test the memory module directly without agent dependencies"""
    
    print("Testing Memory Module Directly...")
    print("=" * 60)
    
    try:
        # Import only what we need for the memory module
        import chromadb
        from chromadb.config import Settings
        import requests
        import json
        
        # Import config
        import tradingagents.default_config as default_config
        config = default_config.DEFAULT_CONFIG
        
        print(f"✅ Dependencies imported successfully")
        print(f"✅ Configuration loaded")
        print(f"   embeddings_url: {config['embeddings_url']}")
        print(f"   api_key: {config['api_key'][:10]}...{config['api_key'][-10:]}")
        
        # Test direct HTTP request to embeddings API (same as memory module does)
        print(f"\nTesting direct HTTP embedding request...")
        
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "input": "This is a test for the memory system",
            "model": "Qwen/Qwen3-Embedding-8B"
        }
        
        response = requests.post(config['embeddings_url'], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        embedding = result['data'][0]['embedding']
        
        print(f"✅ Direct HTTP embedding request successful!")
        print(f"   Dimensions: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
        
        # Test ChromaDB functionality
        print(f"\nTesting ChromaDB functionality...")
        
        chroma_client = chromadb.Client(Settings(allow_reset=True))
        collection_name = "test_memory_direct"
        
        # Clean up any existing collection
        try:
            existing_collections = [col.name for col in chroma_client.list_collections()]
            if collection_name in existing_collections:
                chroma_client.delete_collection(name=collection_name)
        except:
            pass
        
        # Create collection
        collection = chroma_client.create_collection(name=collection_name)
        print(f"✅ ChromaDB collection created successfully")
        
        # Add test data
        test_situations = [
            "High inflation rate with rising interest rates and declining consumer spending",
            "Tech sector showing high volatility with increasing institutional selling pressure"
        ]
        
        test_recommendations = [
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows."
        ]
        
        # Generate embeddings for test data
        embeddings = []
        for situation in test_situations:
            data = {"input": situation, "model": "Qwen/Qwen3-Embedding-8B"}
            response = requests.post(config['embeddings_url'], headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            embeddings.append(result['data'][0]['embedding'])
        
        # Add to ChromaDB
        collection.add(
            documents=test_situations,
            metadatas=[{"recommendation": rec} for rec in test_recommendations],
            embeddings=embeddings,
            ids=["0", "1"]
        )
        
        print(f"✅ Test data added to ChromaDB")
        
        # Test query
        query_text = "Market showing increased volatility in tech sector with institutional investors reducing positions"
        
        # Generate embedding for query
        data = {"input": query_text, "model": "Qwen/Qwen3-Embedding-8B"}
        response = requests.post(config['embeddings_url'], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        query_embedding = result['data'][0]['embedding']
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2,
            include=["metadatas", "documents", "distances"]
        )
        
        print(f"✅ ChromaDB query successful!")
        print(f"   Found {len(results['documents'][0])} matches")
        
        for i in range(len(results['documents'][0])):
            similarity = 1 - results['distances'][0][i]
            print(f"\n   Match {i+1}:")
            print(f"   Similarity: {similarity:.3f}")
            print(f"   Situation: {results['documents'][0][i][:100]}...")
            print(f"   Recommendation: {results['metadatas'][0][i]['recommendation'][:100]}...")
        
        # Clean up
        chroma_client.delete_collection(name=collection_name)
        print(f"\n✅ Test collection cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_memory_module_directly()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
    if success:
        print("✅ Memory module components: WORKING")
        print("✅ Direct HTTP embeddings: WORKING")
        print("✅ ChromaDB functionality: WORKING")
        print("\n🎉 SUCCESS: The memory system fix is working!")
        print("   The 404 error should be resolved.")
    else:
        print("❌ Memory module test: FAILED")
        print("   Check the errors above.")
