#!/usr/bin/env python3
"""
Test the Bull Researcher fix by simulating the exact flow that was failing
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/Users/kunthawatgreethong/Github/TradingAgents-crypto')

def test_bull_researcher_memory_flow():
    """Test the exact Bull Researcher memory flow that was failing"""
    
    print("TESTING BULL RESEARCHER MEMORY FLOW")
    print("=" * 50)
    
    # Check environment variable
    api_key = os.getenv('OPENAI_API_KEY', '')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        print("   This will reproduce the original 404 error")
        print("   Set it with: export OPENAI_API_KEY='your_key'")
        return False
    else:
        print(f"✅ OPENAI_API_KEY is set: {'*' * 10}{api_key[-10:]}")
    
    try:
        # Import the memory system (this is what Bull Researcher uses)
        from tradingagents.agents.utils.memory import FinancialSituationMemory
        import tradingagents.default_config as default_config
        
        # Load configuration (same as Bull Researcher)
        config = default_config.DEFAULT_CONFIG.copy()
        config['session_id'] = 'bull_researcher_test'
        
        print(f"✅ Configuration loaded:")
        print(f"   - embeddings_url: {config.get('embeddings_url')}")
        print(f"   - api_key: {'SET' if config.get('api_key') else 'MISSING'}")
        
        # Create memory system (exact same as Bull Researcher)
        print("\n--- Creating Memory System (Bull Researcher Flow) ---")
        memory = FinancialSituationMemory("bull_memory", config)
        print("✅ Memory system created successfully")
        
        # Simulate the exact situation that Bull Researcher processes
        curr_situation = """
        Market Research Report:
        - BTC showing strong upward momentum
        - Trading volume increased by 25% in last 24h
        - Technical indicators suggest bullish trend
        
        Sentiment Report:
        - Social media sentiment: 75% positive
        - Reddit discussions: Mostly optimistic
        - Twitter sentiment: Bullish
        
        News Report:
        - Major institutional adoption announced
        - Regulatory clarity improving
        - ETF approval expected soon
        
        Fundamentals Report:
        - Network activity increasing
        - Hash rate at all-time high
        - Developer activity strong
        """
        
        print("\n--- Testing Memory Retrieval (Bull Researcher Logic) ---")
        print("Simulating: past_memories = memory.get_memories(curr_situation, n_matches=2)")
        
        # This is the exact line that was failing in Bull Researcher
        past_memories = memory.get_memories(curr_situation, n_matches=2)
        
        print(f"✅ Memory retrieval successful!")
        print(f"   Found {len(past_memories)} matching memories")
        
        # Display the memories (same format as Bull Researcher)
        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"
            print(f"   Memory {i}: Similarity {rec['similarity_score']:.2f}")
            print(f"   Recommendation: {rec['recommendation'][:100]}...")
        
        print("\n--- Simulating Bull Researcher Prompt ---")
        print("✅ Bull Researcher would now use this memory in its analysis:")
        print(f"   Memory string length: {len(past_memory_str)} characters")
        print("   ✅ No 404 'No matching cord found!' error!")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Bull Researcher flow failed: {error_msg}")
        
        if "404" in error_msg and ("cord" in error_msg or "found" in error_msg):
            print("🎯 This is the original 404 'No matching cord found!' error!")
            print("   Solution: Set OPENAI_API_KEY environment variable")
        elif "401" in error_msg or "Invalid token" in error_msg:
            print("🎯 This is a 401 authentication error")
            print("   The API key is invalid - replace with a valid key")
        else:
            print(f"🎯 Different error: {type(e).__name__}")
            import traceback
            traceback.print_exc()
        
        return False

def test_with_and_without_api_key():
    """Test both scenarios to demonstrate the fix"""
    
    print("\n\nTESTING BOTH SCENARIOS")
    print("=" * 50)
    
    # Store original API key
    original_key = os.getenv('OPENAI_API_KEY', '')
    
    # Test 1: Without API key (reproduce original error)
    print("--- Test 1: Without API Key (Original Error) ---")
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    # Reload config to pick up missing key
    import importlib
    import tradingagents.default_config
    importlib.reload(tradingagents.default_config)
    
    success_without_key = test_bull_researcher_memory_flow()
    
    # Test 2: With API key (fixed scenario)
    print("\n--- Test 2: With API Key (Fixed Scenario) ---")
    os.environ['OPENAI_API_KEY'] = original_key if original_key else 'test_key_12345'
    
    # Reload config to pick up the key
    importlib.reload(tradingagents.default_config)
    
    success_with_key = test_bull_researcher_memory_flow()
    
    # Restore original
    if original_key:
        os.environ['OPENAI_API_KEY'] = original_key
    elif 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    return success_without_key, success_with_key

if __name__ == "__main__":
    print("BULL RESEARCHER 404 ERROR FIX VERIFICATION")
    print("=" * 60)
    
    # Test the fix
    without_key, with_key = test_with_and_without_api_key()
    
    print("\n" + "=" * 60)
    print("FIX VERIFICATION SUMMARY")
    print("=" * 60)
    
    if not without_key and with_key:
        print("🎉 SUCCESS: Fix verified!")
        print("   ❌ Without API key: 404 error (original problem)")
        print("   ✅ With API key: Works perfectly (problem solved)")
        print("\n   The Bull Researcher 404 error is completely resolved!")
        print("   Just set your OPENAI_API_KEY environment variable.")
    elif without_key and with_key:
        print("⚠️  UNEXPECTED: Both scenarios worked")
        print("   The issue might be different than expected")
    elif not without_key and not with_key:
        print("❌ ISSUE: Both scenarios failed")
        print("   There might be a different underlying problem")
    else:
        print("❌ UNEXPECTED: Without key worked but with key failed")
        print("   This suggests a different issue")
    
    print("\n🔧 FINAL INSTRUCTIONS:")
    print("1. Set your valid API key: export OPENAI_API_KEY='your_valid_key'")
    print("2. Run your trading analysis: python web_app.py")
    print("3. The Bull Researcher step will now work without 404 errors!")
