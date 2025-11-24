#!/usr/bin/env python3
"""
Test Script for the new /api/report endpoint
Tests all report retrieval functionality
"""

import requests
import json
import time

def test_report_api():
    """Test the new report API endpoint"""
    base_url = "http://127.0.0.1:5001"
    
    print("📄 TradingAgents Crypto - Report API Test")
    print("=" * 50)
    
    # First, let's check if we have any completed sessions
    print("🔍 Checking for completed sessions...")
    try:
        response = requests.get(f"{base_url}/api/sessions")
        if response.status_code == 200:
            sessions_data = response.json()
            completed_sessions = [s for s in sessions_data.get('sessions', []) if s['status'] == 'completed']
            
            if not completed_sessions:
                print("❌ No completed sessions found. Starting a new analysis...")
                # Start a simple analysis for testing
                data = {
                    "ticker": "BTC",
                    "analysis_date": "2025-11-24",
                    "analysts": ["market"],
                    "research_depth": 1,
                    "llm_provider": "openai",
                    "shallow_thinker": "deepseek-ai/DeepSeek-R1-0528",
                    "deep_thinker": "deepseek-ai/DeepSeek-R1-0528",
                    "language": "english",
                    "secret_pass": "your_secret_password_here"
                }
                
                response = requests.post(
                    f"{base_url}/api/start_analysis",
                    headers={"Content-Type": "application/json"},
                    json=data
                )
                
                if response.status_code == 200:
                    session_id = response.json().get('session_id')
                    print(f"🚀 Started analysis session: {session_id}")
                    print("⏳ Waiting for analysis to complete (this may take a few minutes)...")
                    
                    # Monitor progress
                    for i in range(60):  # Wait up to 5 minutes
                        time.sleep(5)
                        status_response = requests.get(f"{base_url}/api/status?session_id={session_id}")
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            progress = status_data.get('progress', 0)
                            status = status_data.get('status')
                            print(f"   Progress: {progress}% - Status: {status}")
                            
                            if status == 'completed':
                                print("✅ Analysis completed!")
                                completed_sessions = [{'session_id': session_id, 'ticker': 'BTC'}]
                                break
                            elif status == 'failed':
                                print("❌ Analysis failed!")
                                return
                        else:
                            print(f"❌ Status check failed: {status_response.status_code}")
                            return
                    else:
                        print("⏰ Analysis timed out")
                        return
                else:
                    print(f"❌ Failed to start analysis: {response.status_code}")
                    return
            else:
                print(f"✅ Found {len(completed_sessions)} completed session(s)")
            
            # Test the report endpoint with the first completed session
            session_id = completed_sessions[0]['session_id']
            ticker = completed_sessions[0]['ticker']
            
            print(f"\n📋 Testing report endpoint with session {session_id} ({ticker})")
            
            # Test 1: Get all reports
            print("\n1️⃣ Testing: Get all reports")
            try:
                response = requests.get(f"{base_url}/api/report?session_id={session_id}&section=all")
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    reports = data.get('reports', {})
                    print(f"   ✅ Available reports: {list(reports.keys())}")
                    for section, content in reports.items():
                        content_preview = content[:100] + "..." if len(content) > 100 else content
                        print(f"   📄 {section}: {content_preview}")
                else:
                    print(f"   ❌ Error: {response.json()}")
            except Exception as e:
                print(f"   ❌ Exception: {e}")
            
            # Test 2: Get specific sections
            sections = ['market', 'news', 'fundamentals', 'sentiment', 'investment_plan', 'trader_plan', 'final_decision']
            
            for section in sections:
                print(f"\n2️⃣ Testing: Get {section} report")
                try:
                    response = requests.get(f"{base_url}/api/report?session_id={session_id}&section={section}")
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        reports = data.get('reports', {})
                        if section in reports:
                            content = reports[section]
                            content_preview = content[:150] + "..." if len(content) > 150 else content
                            print(f"   ✅ {section}: {content_preview}")
                        else:
                            print(f"   ⚠️ {section} not available")
                    else:
                        error_data = response.json()
                        print(f"   ❌ Error: {error_data.get('error')}")
                except Exception as e:
                    print(f"   ❌ Exception: {e}")
            
            # Test 3: Error handling
            print("\n3️⃣ Testing: Error handling")
            
            # Invalid session ID
            print("   Testing invalid session ID...")
            try:
                response = requests.get(f"{base_url}/api/report?session_id=invalid_session")
                print(f"   Status: {response.status_code} - {response.json().get('error')}")
            except Exception as e:
                print(f"   Exception: {e}")
            
            # Invalid section
            print("   Testing invalid section...")
            try:
                response = requests.get(f"{base_url}/api/report?session_id={session_id}&section=invalid_section")
                print(f"   Status: {response.status_code} - {response.json().get('error')}")
            except Exception as e:
                print(f"   Exception: {e}")
            
            # Missing session_id
            print("   Testing missing session_id...")
            try:
                response = requests.get(f"{base_url}/api/report")
                print(f"   Status: {response.status_code} - {response.json().get('error')}")
            except Exception as e:
                print(f"   Exception: {e}")
            
        else:
            print(f"❌ Failed to get sessions: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n🎉 Report API Test Complete!")
    print("\n📚 Report Endpoint Usage:")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=all")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=market")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=news")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=fundamentals")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=sentiment")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=investment_plan")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=trader_plan")
    print(f"   GET {base_url}/api/report?session_id=<id>&section=final_decision")

if __name__ == "__main__":
    test_report_api()
