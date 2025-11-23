#!/usr/bin/env python3
"""
Minimal test script to verify the embeddings API fix
"""

import os
from openai import OpenAI

def test_embeddings_minimal():
    """Test the embeddings API with minimal dependencies"""
    
    print("Testing Embeddings API Fix (Minimal)...")
    print("=" * 50)
    
    # Use the embeddings URL directly
    embeddings_url = "https://chutes-qwen-qwen3-embedding-8b.chutes.ai/v1/embeddings"
    api_key = os.getenv("OPENAI_API_KEY", "sk-123456")  # Use env var or test key
    
    print(f"Embeddings URL: {embeddings_url}")
    print(f"API Key: {api_key[:10]}..." if len(api_key) > 10 else "API Key: [short]")
    print()
    
    # Test embeddings with a simple text
    test_text = "This is a test for the embeddings API"
    
    try:
        # Initialize OpenAI client with embeddings URL
        client = OpenAI(
            base_url=embeddings_url,
            api_key=api_key
        )
        print("✅ OpenAI client initialized with embeddings URL")
        
        # Test embedding generation (with model parameter for Chutes)
        print("Testing embedding generation...")
        response = client.embeddings.create(
            model="Qwen/Qwen2.5-7B-Instruct",  # Use the correct model for Chutes
            input=test_text
        )
        
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
    success = test_embeddings_minimal()
    if success:
        print("\n✅ Embeddings API fix is working correctly!")
        print("The 404 error should now be resolved.")
    else:
        print("\n❌ Embeddings API fix needs more work")
