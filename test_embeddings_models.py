#!/usr/bin/env python3
"""
Test different model names for Chutes embeddings API
"""

from openai import OpenAI

def test_different_models():
    """Test different model names to find the correct one"""
    
    print("Testing Different Model Names for Chutes Embeddings...")
    print("=" * 60)
    
    embeddings_url = "https://chutes-qwen-qwen3-embedding-8b.chutes.ai/v1/embeddings"
    api_key = "sk-123456"  # Test key
    
    # Possible model names to test
    model_candidates = [
        "Qwen/Qwen2.5-7B-Instruct",  # Current (not working)
        "qwen/qwen2.5-7b-instruct",  # Lowercase
        "Qwen2.5-7B-Instruct",       # Without Qwen/
        "qwen2.5-7b-instruct",       # Lowercase without Qwen/
        "embedding-model",           # Generic
        "default",                   # Default
        "text-embedding-ada-002",    # OpenAI style
        "text-embedding-3-small",    # OpenAI style
    ]
    
    client = OpenAI(
        base_url=embeddings_url,
        api_key=api_key
    )
    
    test_text = "This is a test"
    
    for model in model_candidates:
        print(f"\nTesting model: '{model}'")
        try:
            response = client.embeddings.create(model=model, input=test_text)
            print(f"✅ SUCCESS with model: '{model}'")
            print(f"   Embedding dimensions: {len(response.data[0].embedding)}")
            return model  # Return the first working model
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg and "cord" in error_msg:
                print(f"❌ Model not found: '{model}'")
            elif "401" in error_msg or "Invalid token" in error_msg:
                print(f"✅ Model found! (Auth error expected): '{model}'")
                return model
            else:
                print(f"⚠️  Other error with '{model}': {error_msg}")
    
    print(f"\n❌ No working model found among {len(model_candidates)} candidates")
    return None

def test_without_model():
    """Test without model parameter"""
    
    print(f"\n" + "=" * 60)
    print("Testing WITHOUT model parameter...")
    print("=" * 60)
    
    embeddings_url = "https://chutes-qwen-qwen3-embedding-8b.chutes.ai/v1/embeddings"
    api_key = "sk-123456"
    
    client = OpenAI(
        base_url=embeddings_url,
        api_key=api_key
    )
    
    try:
        response = client.embeddings.create(input="This is a test")
        print("✅ SUCCESS without model parameter!")
        print(f"   Embedding dimensions: {len(response.data[0].embedding)}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg and "cord" in error_msg:
            print("❌ Model parameter required")
        elif "401" in error_msg or "Invalid token" in error_msg:
            print("✅ Works without model! (Auth error expected)")
            return True
        else:
            print(f"⚠️  Other error: {error_msg}")
    
    return False

if __name__ == "__main__":
    working_model = test_different_models()
    works_without_model = test_without_model()
    
    print(f"\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    
    if working_model:
        print(f"✅ Working model found: '{working_model}'")
    else:
        print("❌ No working model found")
    
    if works_without_model:
        print("✅ Works without model parameter")
    else:
        print("❌ Model parameter is required")
    
    print(f"\nRecommendation for memory.py fix:")
    if working_model:
        print(f"Use model: '{working_model}'")
    elif works_without_model:
        print("Remove model parameter entirely")
    else:
        print("Need to contact API provider for correct model name")
