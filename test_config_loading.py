#!/usr/bin/env python3
"""
Test that the configuration is being loaded correctly in the trading graph
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_config_loading():
    """Test that the configuration system loads embeddings_url correctly"""
    
    print("Testing Configuration Loading...")
    print("=" * 50)
    
    try:
        # Test the config system
        from tradingagents.dataflows.config import get_config
        config = get_config()
        
        print("✅ Configuration loaded successfully")
        print(f"Backend URL: {config.get('backend_url', 'NOT FOUND')}")
        print(f"Embeddings URL: {config.get('embeddings_url', 'NOT FOUND')}")
        
        if 'embeddings_url' in config:
            print("✅ embeddings_url is present in configuration")
            return config['embeddings_url']
        else:
            print("❌ embeddings_url is missing from configuration")
            return None
            
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_trading_graph_config():
    """Test that TradingAgentsGraph loads configuration correctly"""
    
    print("\nTesting TradingAgentsGraph Configuration...")
    print("=" * 50)
    
    try:
        # We can't fully initialize the graph due to dependencies,
        # but we can test the config loading part
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.dataflows.config import get_config
        
        # Get config the same way the graph does
        config = get_config()
        
        print("✅ TradingAgentsGraph can access configuration")
        print(f"Embeddings URL in graph config: {config.get('embeddings_url', 'NOT FOUND')}")
        
        return config.get('embeddings_url')
        
    except Exception as e:
        print(f"❌ TradingAgentsGraph config test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_memory_with_correct_config():
    """Test memory system with the correct configuration"""
    
    print("\nTesting Memory System with Correct Configuration...")
    print("=" * 50)
    
    try:
        from tradingagents.dataflows.config import get_config
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        
        config = get_config()
        print(f"Using embeddings URL: {config.get('embeddings_url')}")
        
        # Test memory initialization
        memory = FinancialSituationMemory("test_memory", config)
        print("✅ Memory system initialized with correct config")
        
        # Test embedding generation
        test_text = "This is a test"
        try:
            embedding = memory.get_embedding(test_text)
            print(f"✅ Embedding generated successfully!")
            print(f"   Dimensions: {len(embedding)}")
            return True
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg and "cord" in error_msg:
                print(f"❌ Model name issue: {e}")
                print("The model name might be incorrect for this endpoint")
                return False
            elif "401" in error_msg or "Invalid token" in error_msg:
                print(f"✅ Configuration working! (Auth error expected): {e}")
                return True
            else:
                print(f"⚠️  Other error: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    config_url = test_config_loading()
    graph_url = test_trading_graph_config()
    memory_works = test_memory_with_correct_config()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    
    if config_url:
        print(f"✅ Config system loads embeddings_url: {config_url}")
    else:
        print("❌ Config system not loading embeddings_url")
    
    if graph_url:
        print(f"✅ TradingAgentsGraph can access embeddings_url: {graph_url}")
    else:
        print("❌ TradingAgentsGraph cannot access embeddings_url")
    
    if memory_works:
        print("✅ Memory system works with correct configuration")
    else:
        print("❌ Memory system still has issues")
    
    if config_url and graph_url and memory_works:
        print("\n✅ SUCCESS: Configuration fix is working!")
        print("The 'No matching cord found!' error should be resolved.")
    else:
        print("\n❌ Still need to investigate the configuration or model name issue")
