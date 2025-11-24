# API Status Endpoints Guide - TradingAgents Crypto

## ✅ New Status Endpoints Added

The API now includes comprehensive status checking endpoints to monitor your analysis sessions.

## Available Endpoints

### 1. Health Check
```bash
GET http://localhost:5001/health
```
**Purpose:** Check if the service is running
**Response:**
```json
{
  "service": "TradingAgents Crypto",
  "status": "healthy", 
  "timestamp": "2025-11-24T11:03:05.123456"
}
```

### 2. All Sessions Status
```bash
GET http://localhost:5001/api/status
```
**Purpose:** Get status of all analysis sessions
**Response:**
```json
{
  "total_sessions": 2,
  "sessions": {
    "1763956992": {
      "status": "running",
      "progress": 45,
      "current_step": "Market analysis completed",
      "ticker": "BTC",
      "analysis_date": "2025-11-24"
    },
    "1763956800": {
      "status": "completed",
      "progress": 100,
      "current_step": "Analysis completed successfully!",
      "ticker": "ETH",
      "analysis_date": "2025-11-24"
    }
  }
}
```

### 3. Specific Session Status
```bash
GET http://localhost:5001/api/status?session_id=1763956992
```
**Purpose:** Get detailed status of a specific session
**Response:**
```json
{
  "session_id": "1763956992",
  "status": "running",
  "progress": 45,
  "current_step": "Market analysis completed",
  "agent_status": {
    "Market Analyst": "completed",
    "Social Analyst": "in_progress",
    "News Analyst": "pending",
    "Fundamentals Analyst": "pending",
    "Bull Researcher": "pending",
    "Bear Researcher": "pending",
    "Research Manager": "pending",
    "Trader": "pending",
    "Risky Analyst": "pending",
    "Neutral Analyst": "pending",
    "Safe Analyst": "pending",
    "Portfolio Manager": "pending"
  },
  "report_sections": {
    "market_report": true,
    "sentiment_report": false,
    "news_report": false,
    "fundamentals_report": false,
    "investment_plan": false,
    "trader_investment_plan": false,
    "final_trade_decision": false
  },
  "config": {
    "ticker": "BTC",
    "analysis_date": "2025-11-24",
    "analysts": ["fundamentals", "market", "news"]
  }
}
```

### 4. List All Sessions
```bash
GET http://localhost:5001/api/sessions
```
**Purpose:** Get a simple list of all sessions
**Response:**
```json
{
  "total_sessions": 2,
  "sessions": [
    {
      "session_id": "1763956992",
      "status": "running",
      "ticker": "BTC",
      "analysis_date": "2025-11-24",
      "created_at": "1763956992"
    },
    {
      "session_id": "1763956800",
      "status": "completed",
      "ticker": "ETH", 
      "analysis_date": "2025-11-24",
      "created_at": "1763956800"
    }
  ]
}
```

## Status Values

### Session Status
- `running` - Analysis is currently in progress
- `completed` - Analysis finished successfully
- `failed` - Analysis encountered an error

### Agent Status
- `pending` - Agent hasn't started yet
- `in_progress` - Agent is currently working
- `completed` - Agent finished successfully

### Progress
- `0-100` - Percentage of overall analysis completion
- Updated in real-time as agents complete their work

## Usage Examples

### Monitor a Running Analysis
```bash
# Start analysis
SESSION_ID=$(curl -s -X POST "http://localhost:5001/api/start_analysis" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "BTC", "analysts": ["market", "news"], "secret_pass": "your_secret_password_here"}' \
  | jq -r '.session_id')

# Monitor progress
while true; do
  curl -s "http://localhost:5001/api/status?session_id=$SESSION_ID" | jq '.progress, .current_step'
  sleep 5
done
```

### Check All Active Sessions
```bash
curl -s "http://localhost:5001/api/status" | jq '.sessions | to_entries[] | select(.value.status == "running")'
```

### Get Completed Sessions for a Ticker
```bash
curl -s "http://localhost:5001/api/sessions" | jq '.sessions[] | select(.ticker == "BTC" and .status == "completed")'
```

## Integration Examples

### Python Integration
```python
import requests
import time

def monitor_analysis(session_id, base_url="http://localhost:5001"):
    """Monitor analysis progress"""
    while True:
        response = requests.get(f"{base_url}/api/status?session_id={session_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"Progress: {data['progress']}% - {data['current_step']}")
            
            if data['status'] in ['completed', 'failed']:
                print(f"Analysis {data['status']}")
                break
        
        time.sleep(5)

# Usage
session_id = "1763956992"
monitor_analysis(session_id)
```

### JavaScript Integration
```javascript
async function monitorSession(sessionId) {
    const response = await fetch(`/api/status?session_id=${sessionId}`);
    const data = await response.json();
    
    console.log(`Progress: ${data.progress}% - ${data.current_step}`);
    
    if (data.status === 'completed') {
        console.log('Analysis completed!');
    } else if (data.status === 'failed') {
        console.log('Analysis failed!');
    }
    
    return data;
}

// Usage
monitorSession('1763956992');
```

## Error Handling

### Common HTTP Status Codes
- `200` - Success
- `404` - Session not found (for specific session queries)
- `500` - Internal server error

### Error Response Format
```json
{
  "error": "Session not found"
}
```

## Real-time Updates

For real-time updates, consider using WebSocket connections:
```javascript
const socket = io();
socket.emit('join_session', {session_id: '1763956992'});

socket.on('progress_update', (data) => {
    console.log(`Progress: ${data.progress}% - ${data.step}`);
});

socket.on('agent_status_update', (data) => {
    console.log(`${data.agent}: ${data.status}`);
});
```

## Complete API Summary

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/health` | GET | Service health check | No |
| `/api/status` | GET | All sessions status | No |
| `/api/status?session_id=<id>` | GET | Specific session status | No |
| `/api/sessions` | GET | List all sessions | No |
| `/api/start_analysis` | POST | Start new analysis | Yes (password) |

All status endpoints are now fully functional and provide comprehensive monitoring capabilities for your trading analysis sessions!
