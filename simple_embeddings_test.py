#!/usr/bin/env python3
"""
Simple test script to verify the embeddings API fix without full agent imports
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.config import get_config
from openai import OpenAI

def test_embeddings_directly():
    """Test the embeddings API directly"""
    
    print("Testing Embeddings API Fix (Direct)...")
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
        # Initialize OpenAI client with embeddings URL
        client = OpenAI(
            base_url=config["embeddings_url"],
            api_key=config.get("api_key", "sk-123456")  # Use a test key
        )
        print("✅ OpenAI client initialized with embeddings URL")
        
        # Test embedding generation
        print("Testing embedding generation...")
        response = client.embeddings.create(input=test_text)
        
        if response and response.data and len(response.data) > 0:
            embedding = response.data[0].embedding
            print(f"✅ Embedding generated successfully")
            print(f"Embedding dimensions: {len(embedding)}")
            print(f"First 5 values: {embedding[:5]}")
            return True
        else:
            print("❌ Embedding generation failed - empty response")
            return False
            
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_embeddings_directly()
    if success:
        print("\n✅ Embeddings API fix is working correctly!")
    else:
        print("\n❌ Embeddings API fix needs more work")
