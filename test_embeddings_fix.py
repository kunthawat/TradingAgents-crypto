#!/usr/bin/env python3
"""
Test script to verify the embeddings API fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.agents.utils.memory import FinancialSituationMemory
from tradingagents.dataflows.config import get_config

def test_embeddings():
    """Test the embeddings functionality"""
    
    print("Testing Embeddings API Fix...")
    print("=" * 50)
    
    # Get config to verify setup
    config = get_config()
    print(f"Backend URL: {config['backend_url']}")
    print(f"Embeddings URL: {config['embeddings_url']}")
    print(f"Model: {config['quick_think_llm']}")
    print()
    
    # Test embeddings with a simple text
    test_text = "This is a test for the embeddings API"
    
    try:
        # Initialize memory system
        memory = FinancialSituationMemory("test", config)
        print("✅ Memory system initialized successfully")
        
        # Test embedding generation
        print("Testing embedding generation...")
        embedding = memory.get_embedding(test_text)
        
        if embedding and len(embedding) > 0:
            print(f"✅ Embedding generated successfully")
            print(f"Embedding dimensions: {len(embedding)}")
            print(f"First 5 values: {embedding[:5]}")
        else:
            print("❌ Embedding generation failed - empty result")
            return False
            
        # Test memory storage and retrieval
        print("\nTesting memory storage and retrieval...")
        
        # Add test data
        test_data = [
            (
                "Market volatility increased with tech stocks declining",
                "Consider defensive positions and reduce tech exposure"
            ),
            (
                "Federal Reserve signals interest rate hikes",
                "Review bond portfolio duration and interest rate sensitivity"
            )
        ]
        
        memory.add_situations(test_data)
        print("✅ Test data added to memory")
        
        # Test memory retrieval
        query = "Tech stocks are falling and interest rates are rising"
        matches = memory.get_memories(query, n_matches=2)
        
        if matches and len(matches) > 0:
            print(f"✅ Memory retrieval successful")
            print(f"Found {len(matches)} matches")
            for i, match in enumerate(matches, 1):
                print(f"  Match {i}: {match['similarity_score']:.2f} similarity")
        else:
            print("❌ Memory retrieval failed")
            return False
            
        print("\n🎉 All embeddings tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_embeddings()
    if success:
        print("\n✅ Embeddings fix is working correctly!")
    else:
        print("\n❌ Embeddings fix needs more work")
