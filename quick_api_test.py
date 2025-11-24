#!/usr/bin/env python3
"""
Quick API Test Script for TradingAgents Crypto
Tests all API endpoints including status checking
"""

import requests
import json
import time

def test_api():
    """Test all API endpoints"""
    base_url = "http://127.0.0.1:5001"
    
    print("🤖 TradingAgents Crypto - Complete API Test")
    print("=" * 60)
    
    # 1. Health check
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # 2. Check all sessions status
    print("\n📊 Checking all sessions...")
    try:
        response = requests.get(f"{base_url}/api/status")
        print(f"✅ All Sessions: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Sessions status failed: {e}")
    
    # 3. List all sessions
    print("\n📋 Listing all sessions...")
    try:
        response = requests.get(f"{base_url}/api/sessions")
        print(f"✅ Sessions List: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Sessions list failed: {e}")
    
    # 4. Start BTC analysis
    print("\n🚀 Starting BTC analysis...")
    data = {
        "ticker": "BTC",
        "analysis_date": "2025-11-24",
        "analysts": ["fundamentals", "market", "news"],
        "research_depth": 2,
        "llm_provider": "openai",
        "shallow_thinker": "deepseek-ai/DeepSeek-R1-0528",
        "deep_thinker": "deepseek-ai/DeepSeek-R1-0528",
        "language": "english",
        "secret_pass": "your_secret_password_here"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/start_analysis",
            headers={"Content-Type": "application/json"},
            json=data
        )
        print(f"✅ Analysis Started: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('session_id')
            print(f"\n📋 Session ID: {session_id}")
            print(f"🌐 Monitor at: {base_url}/analysis?session={session_id}")
            
            # 5. Check specific session status
            print(f"\n🔍 Checking session {session_id} status...")
            time.sleep(1)  # Wait a moment for session to initialize
            
            try:
                response = requests.get(f"{base_url}/api/status?session_id={session_id}")
                print(f"✅ Session Status: {response.status_code}")
                status_data = response.json()
                print(f"   Status: {status_data.get('status')}")
                print(f"   Progress: {status_data.get('progress')}%")
                print(f"   Current Step: {status_data.get('current_step')}")
                print(f"   Ticker: {status_data.get('config', {}).get('ticker')}")
                
                # Show agent statuses
                agent_status = status_data.get('agent_status', {})
                completed_agents = [agent for agent, status in agent_status.items() if status == 'completed']
                if completed_agents:
                    print(f"   Completed Agents: {', '.join(completed_agents)}")
                
            except Exception as e:
                print(f"❌ Session status check failed: {e}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
    
    # 6. Final sessions overview
    print("\n📊 Final sessions overview...")
    try:
        response = requests.get(f"{base_url}/api/sessions")
        if response.status_code == 200:
            sessions_data = response.json()
            print(f"✅ Total Sessions: {sessions_data.get('total_sessions')}")
            for session in sessions_data.get('sessions', []):
                print(f"   - Session {session['session_id']}: {session['status']} ({session['ticker']})")
    except Exception as e:
        print(f"❌ Final overview failed: {e}")
    
    # 7. Test report endpoint (will show error if analysis not completed)
    print("\n📄 Testing report endpoint...")
    try:
        response = requests.get(f"{base_url}/api/report?session_id={session_id}")
        print(f"✅ Report Test: {response.status_code}")
        if response.status_code == 200:
            report_data = response.json()
            print(f"   Available reports: {list(report_data.get('reports', {}).keys())}")
        else:
            error_data = response.json()
            print(f"   Expected error (analysis not completed): {error_data.get('error')}")
    except Exception as e:
        print(f"❌ Report test failed: {e}")
    
    print("\n🎉 Complete API Test Finished!")
    print("\n📚 Available Endpoints:")
    print(f"   GET  {base_url}/health")
    print(f"   GET  {base_url}/api/status")
    print(f"   GET  {base_url}/api/status?session_id=<id>")
    print(f"   GET  {base_url}/api/sessions")
    print(f"   GET  {base_url}/api/report?session_id=<id>&section=<section>")
    print(f"   POST {base_url}/api/start_analysis")
    
    print("\n📄 Report Sections:")
    print("   all, market, news, fundamentals, sentiment, investment_plan, trader_plan, final_decision")

if __name__ == "__main__":
    test_api()
