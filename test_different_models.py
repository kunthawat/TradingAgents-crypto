#!/usr/bin/env python3
"""
Test different model names with the embeddings API
"""

import sys
import os
import openai

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_different_model_names():
    """Test different model names to find the correct one"""
    
    # Import config to get API key and endpoint
    import tradingagents.default_config as default_config
    config = default_config.DEFAULT_CONFIG
    
    api_key = config['api_key']
    embeddings_url = config['embeddings_url']
    
    print(f"Testing different model names...")
    print(f"Endpoint: {embeddings_url}")
    print(f"API Key: {api_key[:10]}...{api_key[-10:]}")
    print("=" * 60)
    
    # Different possible model names to try
    model_names = [
        "Qwen/Qwen3-Embedding-8B",
        "Qwen3-Embedding-8B", 
        "qwen3-embedding-8b",
        "embedding-8b",
        "text-embedding-ada-002",  # Common OpenAI model
        "text-embedding-3-small",  # Newer OpenAI model
        "",  # No model parameter
    ]
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url=embeddings_url
    )
    
    test_text = "This is a test for embeddings"
    
    for model_name in model_names:
        print(f"\nTesting model: '{model_name}'")
        print("-" * 40)
        
        try:
            if model_name == "":
                # Try without model parameter
                response = client.embeddings.create(input=test_text)
            else:
                response = client.embeddings.create(
                    input=test_text,
                    model=model_name
                )
            
            embedding = response.data[0].embedding
            print(f"✅ SUCCESS!")
            print(f"   Dimensions: {len(embedding)}")
            print(f"   Model used: {response.model}")
            return model_name, True
            
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                print(f"❌ Authentication failed (401)")
                print(f"   This means the endpoint is reachable but API key is invalid")
                return model_name, "auth_error"
            elif "404" in error_msg:
                print(f"❌ Model not found (404): {error_msg}")
            elif "429" in error_msg:
                print(f"❌ Rate limited (429): {error_msg}")
            else:
                print(f"❌ Other error: {error_msg}")
    
    return None, False

def test_endpoint_access():
    """Test if the endpoint is accessible at all"""
    
    import tradingagents.default_config as default_config
    config = default_config.DEFAULT_CONFIG
    
    api_key = config['api_key']
    embeddings_url = config['embeddings_url']
    
    print(f"\nTesting endpoint accessibility...")
    print("=" * 60)
    
    try:
        import requests
        
        # Test basic endpoint access
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(embeddings_url.replace('/embeddings', '/models'), headers=headers, timeout=10)
        
        print(f"Endpoint response status: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Endpoint is accessible")
            return True
        else:
            print(f"❌ Endpoint returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    # Test endpoint accessibility first
    endpoint_works = test_endpoint_access()
    
    # Test different model names
    working_model, success = test_different_model_names()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
    if endpoint_works:
        print("✅ Endpoint is accessible")
    else:
        print("❌ Endpoint is not accessible")
    
    if success == True:
        print(f"✅ Working model found: '{working_model}'")
        print("   Update the memory.py file to use this model name")
    elif success == "auth_error":
        print("❌ Authentication error - API key may be invalid for this endpoint")
        print("   The endpoint works but the API key is not accepted")
    else:
        print("❌ No working model found")
        print("   The endpoint or model names may be incorrect")
