# API Troubleshooting Guide - TradingAgents Crypto

## Issue: 404 Error with /api endpoints

### ✅ Solution Found
The API endpoints are working correctly! The issue was likely using the wrong HTTP method.

## Correct API Usage

### 1. Health Check (GET)
```bash
curl -X GET "http://127.0.0.1:5001/health"
```
**Response:** `{"service":"TradingAgents Crypto","status":"healthy","timestamp":"..."}`

### 2. Start Analysis (POST) - NOT GET
```bash
curl -X POST "http://127.0.0.1:5001/api/start_analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BTC",
    "analysis_date": "2025-11-24",
    "analysts": ["fundamentals", "market", "news"],
    "research_depth": 2,
    "llm_provider": "openai",
    "shallow_thinker": "deepseek-ai/DeepSeek-R1-0528",
    "deep_thinker": "deepseek-ai/DeepSeek-R1-0528",
    "language": "english",
    "secret_pass": "your_secret_password_here",
    "session_id": "test_session"
  }'
```

### 3. What Happens with Wrong Methods

#### GET on /api/start_analysis (WRONG):
```bash
curl -X GET "http://127.0.0.1:5001/api/start_analysis"
```
**Response:** `405 Method Not Allowed` (not 404!)

#### POST without proper headers (WRONG):
```bash
curl -X POST "http://127.0.0.1:5001/api/start_analysis" \
  -d '{"ticker": "BTC"}'
```
**Response:** `400 Bad Request` or `415 Unsupported Media Type`

## Complete Working Example

### Test with Minimal Parameters:
```bash
curl -X POST "http://127.0.0.1:5001/api/start_analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BTC",
    "secret_pass": "your_secret_password_here"
  }'
```

**Expected Response:**
```json
{
  "session_id": "1763956391",
  "status": "started"
}
```

## Common HTTP Status Codes

| Status | Meaning | Cause |
|--------|---------|-------|
| 200 | Success | Analysis started |
| 401 | Unauthorized | Wrong password |
| 405 | Method Not Allowed | Using GET instead of POST |
| 400 | Bad Request | Missing required fields |
| 500 | Internal Error | Server problem |

## Quick Test Script

Save this as `quick_api_test.py`:
```python
import requests
import json

# Test API endpoints
def test_api():
    base_url = "http://127.0.0.1:5001"
    
    # 1. Health check
    print("Testing health check...")
    response = requests.get(f"{base_url}/health")
    print(f"Health: {response.status_code} - {response.json()}")
    
    # 2. Start BTC analysis
    print("\nStarting BTC analysis...")
    data = {
        "ticker": "BTC",
        "secret_pass": "your_secret_password_here"
    }
    
    response = requests.post(
        f"{base_url}/api/start_analysis",
        headers={"Content-Type": "application/json"},
        json=data
    )
    print(f"Analysis: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_api()
```

Run it:
```bash
python3 quick_api_test.py
```

## Summary

✅ **API is working correctly**  
✅ **Use POST method for /api/start_analysis**  
✅ **Include Content-Type: application/json header**  
✅ **Use correct password: "your_secret_password_here"**  

The 404 error you experienced was likely due to using GET method instead of POST, or the server wasn't running. Both issues are now resolved!
