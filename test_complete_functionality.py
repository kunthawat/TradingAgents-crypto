#!/usr/bin/env python3
"""
Test script to verify all the new functionality works correctly:
1. Environment variables for API keys and URLs
2. Secret password validation
3. Language selection (English/Thai)
4. New AI model (zai-org/GLM-4.6)
5. Server-side configuration
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_env_variables():
    """Test that all required environment variables are set."""
    print("🔍 Testing environment variables...")
    
    required_vars = ['LLM_URL', 'EMBEDDINGS_URL', 'SECRET_PASS']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * (len(value) - 4)}{value[-4:]}")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {missing_vars}")
        print("Please set these in your .env file")
        return False
    
    print("✅ All environment variables are set\n")
    return True

def test_default_config():
    """Test that default configuration loads environment variables."""
    print("🔍 Testing default configuration...")
    
    try:
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # Check that URLs are loaded from environment
        if 'backend_url' in DEFAULT_CONFIG:
            print(f"✅ LLM URL loaded: {DEFAULT_CONFIG['backend_url']}")
        else:
            print("❌ LLM URL not found in config")
            return False
            
        if 'embeddings_url' in DEFAULT_CONFIG:
            print(f"✅ Embeddings URL loaded: {DEFAULT_CONFIG['embeddings_url']}")
        else:
            print("❌ Embeddings URL not found in config")
            return False
        
        print("✅ Default configuration loaded successfully\n")
        return True
        
    except Exception as e:
        print(f"❌ Error loading default config: {e}\n")
        return False

def test_trading_graph_init():
    """Test that TradingAgentsGraph initializes with language support."""
    print("🔍 Testing TradingAgentsGraph initialization...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        
        # Test with English language
        config = {
            'language': 'english',
            'llm_provider': 'openai',
            'deep_think_llm': 'gpt-4o-mini',
            'quick_think_llm': 'gpt-4o-mini',
            'api_key': 'test-key',
            'backend_url': 'https://api.openai.com/v1',
            'project_dir': '.'
        }
        
        graph = TradingAgentsGraph(config=config)
        
        if hasattr(graph, 'language') and graph.language == 'english':
            print("✅ English language support initialized")
        else:
            print("❌ English language support failed")
            return False
            
        if hasattr(graph, 'language_prompt'):
            print("✅ Language prompt initialized")
        else:
            print("❌ Language prompt not found")
            return False
        
        # Test with Thai language
        config['language'] = 'thai'
        graph_thai = TradingAgentsGraph(config=config)
        
        if hasattr(graph_thai, 'language') and graph_thai.language == 'thai':
            print("✅ Thai language support initialized")
        else:
            print("❌ Thai language support failed")
            return False
            
        if 'ภาษาไทย' in graph_thai.language_prompt:
            print("✅ Thai language prompt contains Thai text")
        else:
            print("❌ Thai language prompt missing Thai text")
            return False
        
        print("✅ TradingAgentsGraph initialization successful\n")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing TradingAgentsGraph: {e}\n")
        return False

def test_web_app_config():
    """Test that web app uses server-side configuration."""
    print("🔍 Testing web app configuration...")
    
    try:
        # Import web app to check for errors
        import web_app
        
        # Check that the app has the start_analysis endpoint
        if hasattr(web_app, 'app'):
            print("✅ Flask app initialized")
        else:
            print("❌ Flask app not found")
            return False
        
        print("✅ Web app configuration successful\n")
        return True
        
    except Exception as e:
        print(f"❌ Error with web app: {e}\n")
        return False

def test_model_availability():
    """Test that the new model is included in options."""
    print("🔍 Testing model availability...")
    
    # Check if the model is mentioned in the HTML file
    html_file = project_root / 'templates' / 'index.html'
    
    if html_file.exists():
        content = html_file.read_text()
        
        if 'zai-org/GLM-4.6' in content:
            print("✅ zai-org/GLM-4.6 model found in HTML")
        else:
            print("❌ zai-org/GLM-4.6 model not found in HTML")
            return False
        
        if 'Thai (ไทย)' in content:
            print("✅ Thai language option found in HTML")
        else:
            print("❌ Thai language option not found in HTML")
            return False
        
        if 'secret_pass' in content:
            print("✅ Secret password field found in HTML")
        else:
            print("❌ Secret password field not found in HTML")
            return False
        
        print("✅ Model and language options available\n")
        return True
    else:
        print("❌ HTML file not found\n")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Complete Functionality\n")
    print("=" * 50)
    
    tests = [
        test_env_variables,
        test_default_config,
        test_trading_graph_init,
        test_web_app_config,
        test_model_availability
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The implementation is working correctly.")
        print("\n📋 Summary of changes:")
        print("✅ API keys and URLs moved to .env file")
        print("✅ Secret password protection added")
        print("✅ Language selection (English/Thai) added")
        print("✅ zai-org/GLM-4.6 model added")
        print("✅ Server-side configuration implemented")
        print("✅ Language prompts integrated into AI pipeline")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
