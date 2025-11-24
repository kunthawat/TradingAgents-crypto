# TradingAgents-Crypto API Manual 📚

> **Complete API Documentation for Multi-Agent Cryptocurrency Trading Analysis Framework**

This comprehensive manual covers all API endpoints, WebSocket events, authentication, and integration examples for the TradingAgents-Crypto framework.

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication & Security](#authentication--security)
3. [Core API Endpoints](#core-api-endpoints)
4. [WebSocket Events](#websocket-events)
5. [Configuration Guide](#configuration-guide)
6. [Code Examples](#code-examples)
7. [Error Handling](#error-handling)
8. [Deployment Options](#deployment-options)

---

## API Overview

The TradingAgents-Crypto API provides access to a sophisticated multi-agent system for cryptocurrency trading analysis. The system uses specialized AI agents to analyze market data, social sentiment, news, fundamentals, and generate comprehensive trading recommendations.

### Architecture

```
Client Application → REST API → Multi-Agent System → Analysis Results
                      ↓
                 WebSocket → Real-time Updates
```

### Available Deployments

| Deployment Type | Base URL | Features | Limitations |
|----------------|----------|----------|-------------|
| **Local Full** | `http://localhost:5000` | Complete functionality, real-time analysis, persistent sessions | Requires local setup |
| **Vercel Demo** | `https://your-app.vercel.app` | Demo responses, limited functionality | 5-minute execution limit, no persistence |

---

## Authentication & Security

### Secret Password Protection

The API requires a secret password for analysis operations to prevent unauthorized usage.

```bash
# Set environment variable
export SECRET_PASS=your_secure_password_here
```

### API Key Management

LLM provider API keys are configured through the web interface for security:

- **OpenAI**: `sk-...` keys
- **Anthropic**: `sk-ant-...` keys  
- **Google**: `AIza...` keys

### Environment Variables

```bash
# Required for financial data
FINNHUB_API_KEY=your_finnhub_api_key

# Optional for enhanced crypto data
COINGECKO_API_KEY=your_coingecko_api_key

# Security
SECRET_KEY=your_flask_secret_key
SECRET_PASS=your_analysis_password
```

---

## Core API Endpoints

### Health & Information

#### GET `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-05-10T14:30:00.000Z",
  "service": "TradingAgents Crypto"
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/health
```

#### GET `/api/info`

Get API information and capabilities.

**Response:**
```json
{
  "name": "Trading Agents Crypto",
  "environment": "Local Development",
  "mode": "Full Analysis",
  "features": [
    "Real-time analysis",
    "Multi-agent collaboration", 
    "WebSocket streaming",
    "Persistent sessions"
  ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/info
```

---

### Analysis Management

#### POST `/api/start_analysis`

Start a new cryptocurrency analysis session.

**Request Body:**
```json
{
  "secret_pass": "your_secure_password",
  "ticker": "BTC",
  "analysis_date": "2024-05-10",
  "analysts": [
    "market_analyst",
    "social_analyst", 
    "news_analyst",
    "fundamentals_analyst"
  ],
  "llm_provider": "openai",
  "shallow_thinker": "gpt-4o",
  "deep_thinker": "gpt-4o",
  "research_depth": "comprehensive",
  "language": "english"
}
```

**Response:**
```json
{
  "session_id": "1715340600",
  "status": "started"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/start_analysis \
  -H "Content-Type: application/json" \
  -d '{
    "secret_pass": "your_secure_password",
    "ticker": "BTC",
    "analysis_date": "2024-05-10",
    "analysts": ["market_analyst", "social_analyst"],
    "llm_provider": "openai",
    "shallow_thinker": "gpt-4o",
    "deep_thinker": "gpt-4o",
    "research_depth": "comprehensive"
  }'
```

#### GET `/api/status`

Get analysis status for sessions.

**Parameters:**
- `session_id` (optional): Specific session ID
- If not provided, returns all sessions

**Response (Single Session):**
```json
{
  "session_id": "1715340600",
  "status": "running",
  "progress": 65,
  "current_step": "Research team decision completed",
  "agent_status": {
    "Market Analyst": "completed",
    "Social Analyst": "completed",
    "News Analyst": "in_progress",
    "Fundamentals Analyst": "pending",
    "Bull Researcher": "pending",
    "Bear Researcher": "pending",
    "Research Manager": "pending",
    "Trader": "pending",
    "Portfolio Manager": "pending"
  },
  "report_sections": {
    "market_report": true,
    "sentiment_report": true,
    "news_report": false,
    "fundamentals_report": false,
    "investment_plan": false,
    "trader_investment_plan": false,
    "final_trade_decision": false
  },
  "config": {
    "ticker": "BTC",
    "analysis_date": "2024-05-10",
    "analysts": ["market_analyst", "social_analyst", "news_analyst", "fundamentals_analyst"]
  }
}
```

**Response (All Sessions):**
```json
{
  "total_sessions": 2,
  "sessions": {
    "1715340600": {
      "status": "completed",
      "progress": 100,
      "current_step": "Analysis completed successfully!",
      "ticker": "BTC",
      "analysis_date": "2024-05-10"
    },
    "1715340700": {
      "status": "running", 
      "progress": 45,
      "current_step": "Social sentiment analysis completed",
      "ticker": "ETH",
      "analysis_date": "2024-05-10"
    }
  }
}
```

**Examples:**
```bash
# Get specific session status
curl -X GET "http://localhost:5000/api/status?session_id=1715340600"

# Get all sessions status
curl -X GET http://localhost:5000/api/status
```

#### GET `/api/sessions`

List all analysis sessions with basic information.

**Response:**
```json
{
  "total_sessions": 2,
  "sessions": [
    {
      "session_id": "1715340700",
      "status": "running",
      "ticker": "ETH",
      "analysis_date": "2024-05-10",
      "created_at": "1715340700"
    },
    {
      "session_id": "1715340600", 
      "status": "completed",
      "ticker": "BTC",
      "analysis_date": "2024-05-10",
      "created_at": "1715340600"
    }
  ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/sessions
```

#### GET `/api/report`

Get AI-generated analysis reports.

**Parameters:**
- `session_id` (required): Session identifier
- `section` (optional): Report section (`all`, `market`, `news`, `fundamentals`, `sentiment`, `investment_plan`, `trader_plan`, `final_decision`)

**Response:**
```json
{
  "session_id": "1715340600",
  "status": "completed",
  "requested_section": "all",
  "reports": {
    "market": "# Market Analysis Report\n\n## Technical Indicators\n\n- **RSI (14)**: 65.3 (Neutral)\n- **MACD**: Bullish crossover detected\n- **Volume**: Above average, indicating strong interest\n\n## Price Action\n\nBTC is currently trading above the 50-day moving average, suggesting bullish momentum in the short to medium term...",
    "sentiment": "# Social Sentiment Analysis\n\n## Reddit Sentiment\n\n- **r/CryptoCurrency**: Positive sentiment (72%)\n- **r/Bitcoin**: Neutral to positive (68%)\n\n## Twitter Analysis\n\n- **Overall Sentiment**: Bullish (65% positive mentions)\n- **Influencer Opinions**: Mixed but leaning positive...",
    "investment_plan": "# Investment Plan\n\n## Recommendation\n\n**BUY** - Moderate confidence\n\n## Rationale\n\nBased on the comprehensive analysis of technical indicators, market sentiment, and fundamental factors, we recommend a moderate buy position...",
    "final_decision": "# Final Trading Decision\n\n## Action: BUY\n\n## Position Size: 15% of portfolio\n\n## Entry Price: $62,500 - $63,500\n\n## Stop Loss: $58,000\n\n## Take Profit: $75,000\n\n## Time Horizon: 2-4 weeks"
  },
  "metadata": {
    "ticker": "BTC",
    "analysis_date": "2024-05-10",
    "completed_at": "1715340600"
  }
}
```

**Examples:**
```bash
# Get all reports
curl -X GET "http://localhost:5000/api/report?session_id=1715340600&section=all"

# Get specific section
curl -X GET "http://localhost:5000/api/report?session_id=1715340600&section=market"

# Get final decision only
curl -X GET "http://localhost:5000/api/report?session_id=1715340600&section=final_decision"
```

---

## WebSocket Events

The API uses Socket.IO for real-time communication during analysis.

### Connection

```javascript
// Connect to WebSocket
const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to TradingAgents API');
});
```

### Events

#### `join_session`

Join an analysis session to receive real-time updates.

```javascript
socket.emit('join_session', {
  session_id: '1715340600'
});
```

#### `new_message`

Receive real-time analysis messages.

```javascript
socket.on('new_message', (data) => {
  console.log(`[${data.timestamp}] ${data.type}: ${data.content}`);
});
```

**Sample Data:**
```json
{
  "timestamp": "14:30:15",
  "type": "Analysis", 
  "content": "Market analysis completed. RSI indicates neutral momentum..."
}
```

#### `agent_status_update`

Receive agent status changes.

```javascript
socket.on('agent_status_update', (data) => {
  console.log(`${data.agent}: ${data.status}`);
});
```

**Sample Data:**
```json
{
  "agent": "Market Analyst",
  "status": "completed"
}
```

#### `progress_update`

Receive analysis progress updates.

```javascript
socket.on('progress_update', (data) => {
  console.log(`Progress: ${data.progress}% - ${data.step}`);
});
```

**Sample Data:**
```json
{
  "progress": 65,
  "step": "Research team decision completed"
}
```

#### `report_update`

Receive completed report sections.

```javascript
socket.on('report_update', (data) => {
  console.log(`Report section ${data.section} completed`);
});
```

**Sample Data:**
```json
{
  "section": "market_report",
  "content": "# Market Analysis Report\n\n## Technical Indicators..."
}
```

#### `session_state`

Receive current session state when joining.

```javascript
socket.on('session_state', (data) => {
  console.log('Current session state:', data);
});
```

---

## Configuration Guide

### Available Analysts

| Analyst | Description | Data Sources |
|---------|-------------|--------------|
| `market_analyst` | Technical analysis and price patterns | Price data, technical indicators |
| `social_analyst` | Social media sentiment analysis | Reddit, Twitter, crypto communities |
| `news_analyst` | News impact analysis | Crypto news sources, financial news |
| `fundamentals_analyst` | Project fundamentals and metrics | On-chain data, project metrics |

### LLM Providers

#### OpenAI
- **Models**: `gpt-4o`, `gpt-4o-mini`, `o1`, `o3`, `o4`
- **Endpoint**: `https://api.openai.com/v1`
- **Key Format**: `sk-proj-...`

#### Anthropic
- **Models**: `claude-3-5-haiku`, `claude-3-5-sonnet`, `claude-3-opus`
- **Endpoint**: `https://api.anthropic.com/`
- **Key Format**: `sk-ant-...`

#### Google
- **Models**: `gemini-2.0-flash`, `gemini-2.5-pro`
- **Endpoint**: `https://generativelanguage.googleapis.com/v1`
- **Key Format**: `AIza...`

### Research Depth Levels

| Level | Description | Analysis Time |
|-------|-------------|---------------|
| `basic` | Quick overview with key indicators | 2-3 minutes |
| `standard` | Comprehensive analysis with debate | 5-8 minutes |
| `comprehensive` | Deep analysis with multiple rounds | 10-15 minutes |

### Supported Cryptocurrencies

- **Major**: BTC, ETH, ADA, SOL, MATIC, AVAX, DOT
- **DeFi**: UNI, AAVE, COMP, MKR
- **Meme**: DOGE, SHIB
- **Stablecoins**: USDT, USDC, DAI

---

## Code Examples

### Python Client

```python
import requests
import socketio
import time

class TradingAgentsClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.sio = socketio.Client()
        self.setup_events()
    
    def setup_events(self):
        @self.sio.event
        def connect():
            print("Connected to TradingAgents API")
        
        @self.sio.event
        def new_message(data):
            print(f"[{data['timestamp']}] {data['type']}: {data['content']}")
        
        @self.sio.event
        def progress_update(data):
            print(f"Progress: {data['progress']}% - {data['step']}")
    
    def start_analysis(self, ticker, analysis_date, secret_pass, analysts=None):
        """Start a new analysis"""
        if analysts is None:
            analysts = ["market_analyst", "social_analyst", "news_analyst"]
        
        payload = {
            "secret_pass": secret_pass,
            "ticker": ticker,
            "analysis_date": analysis_date,
            "analysts": analysts,
            "llm_provider": "openai",
            "shallow_thinker": "gpt-4o",
            "deep_thinker": "gpt-4o",
            "research_depth": "standard"
        }
        
        response = requests.post(f"{self.base_url}/api/start_analysis", json=payload)
        return response.json()
    
    def get_status(self, session_id):
        """Get analysis status"""
        response = requests.get(f"{self.base_url}/api/status", params={"session_id": session_id})
        return response.json()
    
    def get_report(self, session_id, section="all"):
        """Get analysis report"""
        params = {"session_id": session_id, "section": section}
        response = requests.get(f"{self.base_url}/api/report", params=params)
        return response.json()
    
    def monitor_analysis(self, session_id):
        """Monitor analysis with real-time updates"""
        self.sio.connect(self.base_url)
        self.sio.emit('join_session', {'session_id': session_id})
        
        # Wait for analysis to complete
        while True:
            status = self.get_status(session_id)
            if status['status'] in ['completed', 'failed']:
                break
            time.sleep(5)
        
        self.sio.disconnect()
        return status

# Usage example
client = TradingAgentsClient()

# Start analysis
result = client.start_analysis(
    ticker="BTC",
    analysis_date="2024-05-10", 
    secret_pass="your_secure_password"
)

session_id = result['session_id']
print(f"Started analysis with session ID: {session_id}")

# Monitor with real-time updates
final_status = client.monitor_analysis(session_id)

# Get final report
if final_status['status'] == 'completed':
    report = client.get_report(session_id)
    print("Final Decision:", report['reports']['final_decision'])
```

### JavaScript Client

```javascript
class TradingAgentsClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
        this.socket = io(baseUrl);
        this.setupEvents();
    }
    
    setupEvents() {
        this.socket.on('connect', () => {
            console.log('Connected to TradingAgents API');
        });
        
        this.socket.on('new_message', (data) => {
            console.log(`[${data.timestamp}] ${data.type}: ${data.content}`);
        });
        
        this.socket.on('progress_update', (data) => {
            console.log(`Progress: ${data.progress}% - ${data.step}`);
        });
    }
    
    async startAnalysis(config) {
        const response = await fetch(`${this.baseUrl}/api/start_analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config)
        });
        
        return await response.json();
    }
    
    async getStatus(sessionId) {
        const response = await fetch(`${this.baseUrl}/api/status?session_id=${sessionId}`);
        return await response.json();
    }
    
    async getReport(sessionId, section = 'all') {
        const response = await fetch(`${this.baseUrl}/api/report?session_id=${sessionId}&section=${section}`);
        return await response.json();
    }
    
    monitorAnalysis(sessionId) {
        return new Promise((resolve, reject) => {
            this.socket.emit('join_session', { session_id: sessionId });
            
            const checkStatus = async () => {
                try {
                    const status = await this.getStatus(sessionId);
                    if (status.status === 'completed' || status.status === 'failed') {
                        this.socket.disconnect();
                        resolve(status);
                    } else {
                        setTimeout(checkStatus, 5000);
                    }
                } catch (error) {
                    reject(error);
                }
            };
            
            checkStatus();
        });
    }
}

// Usage example
const client = new TradingAgentsClient();

async function runAnalysis() {
    try {
        // Start analysis
        const result = await client.startAnalysis({
            secret_pass: 'your_secure_password',
            ticker: 'BTC',
            analysis_date: '2024-05-10',
            analysts: ['market_analyst', 'social_analyst', 'news_analyst'],
            llm_provider: 'openai',
            shallow_thinker: 'gpt-4o',
            deep_thinker: 'gpt-4o',
            research_depth: 'standard'
        });
        
        console.log(`Started analysis with session ID: ${result.session_id}`);
        
        // Monitor with real-time updates
        const finalStatus = await client.monitorAnalysis(result.session_id);
        
        // Get final report
        if (finalStatus.status === 'completed') {
            const report = await client.getReport(result.session_id);
            console.log('Final Decision:', report.reports.final_decision);
        }
        
    } catch (error) {
        console.error('Analysis failed:', error);
    }
}

runAnalysis();
```

### cURL Examples

```bash
# Start analysis
curl -X POST http://localhost:5000/api/start_analysis \
  -H "Content-Type: application/json" \
  -d '{
    "secret_pass": "your_secure_password",
    "ticker": "BTC",
    "analysis_date": "2024-05-10",
    "analysts": ["market_analyst", "social_analyst"],
    "llm_provider": "openai",
    "shallow_thinker": "gpt-4o",
    "deep_thinker": "gpt-4o",
    "research_depth": "standard"
  }'

# Check status
curl -X GET "http://localhost:5000/api/status?session_id=1715340600"

# Get all reports
curl -X GET "http://localhost:5000/api/report?session_id=1715340600&section=all"

# Get specific report section
curl -X GET "http://localhost:5000/api/report?session_id=1715340600&section=final_decision"

# List all sessions
curl -X GET http://localhost:5000/api/sessions

# Health check
curl -X GET http://localhost:5000/health
```

---

## Error Handling

### HTTP Status Codes

| Code | Description | Example Response |
|------|-------------|------------------|
| `200` | Success | Analysis completed successfully |
| `400` | Bad Request | Invalid parameters |
| `401` | Unauthorized | Invalid secret password |
| `404` | Not Found | Session not found |
| `500` | Internal Error | Server error during analysis |

### Error Response Format

```json
{
  "error": "Invalid password",
  "message": "The provided secret password is incorrect"
}
```

### Common Error Scenarios

#### Invalid Secret Password
```json
{
  "error": "Invalid password",
  "message": "The provided secret password is incorrect"
}
```

#### Session Not Found
```json
{
  "error": "Session not found",
  "message": "The specified session ID does not exist"
}
```

#### Analysis Not Completed
```json
{
  "error": "Analysis not completed yet",
  "status": "running",
  "progress": 45
}
```

#### Invalid Report Section
```json
{
  "error": "Invalid section. Must be one of: all, market, news, fundamentals, sentiment, investment_plan, trader_plan, final_decision"
}
```

### Error Handling Best Practices

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(url, method='GET', json_data=None, params=None):
    try:
        if method == 'POST':
            response = requests.post(url, json=json_data)
        else:
            response = requests.get(url, params=params)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise Exception("Invalid secret password")
        elif e.response.status_code == 404:
            raise Exception("Session not found")
        else:
            raise Exception(f"HTTP Error: {e.response.status_code}")
    
    except RequestException as e:
        raise Exception(f"Network error: {str(e)}")

# Usage
try:
    result = safe_api_call(
        "http://localhost:5000/api/start_analysis",
        method='POST',
        json_data={
            "secret_pass": "your_secure_password",
            "ticker": "BTC",
            "analysis_date": "2024-05-10"
        }
    )
except Exception as e:
    print(f"API call failed: {e}")
```

---

## Deployment Options

### Local Development Setup

1. **Clone and Install**
```bash
git clone https://github.com/yourusername/TradingAgents-crypto.git
cd TradingAgents-crypto
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
export FINNHUB_API_KEY=your_finnhub_key
export SECRET_PASS=your_secure_password
export SECRET_KEY=your_flask_secret_key
```

3. **Run Application**
```bash
python web_app.py
```

4. **Access API**
- Base URL: `http://localhost:5000`
- WebSocket: `ws://localhost:5000`

### Vercel Serverless Deployment

The Vercel deployment provides a demo version with limitations:

**Limitations:**
- 5-minute execution time limit
- No persistent storage
- Demo responses only
- No real-time WebSocket functionality

**Setup:**
1. Deploy `api/index.py` as serverless function
2. Configure environment variables in Vercel dashboard
3. Access via `https://your-app.vercel.app`

### Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "web_app.py"]
```

```bash
# Build and run
docker build -t tradingagents-crypto .
docker run -p 5000:5000 -e FINNHUB_API_KEY=your_key tradingagents-crypto
```

### Production Considerations

- **Load Balancing**: Use multiple instances for high availability
- **Database**: Consider Redis for session persistence
- **Monitoring**: Implement health checks and logging
- **Security**: Use HTTPS and secure API key management
- **Rate Limiting**: Implement API rate limiting to prevent abuse

---

## Quick Reference

### Essential Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/health` | Health check |
| `GET` | `/api/info` | API information |
| `POST` | `/api/start_analysis` | Start analysis |
| `GET` | `/api/status` | Get status |
| `GET` | `/api/sessions` | List sessions |
| `GET` | `/api/report` | Get reports |

### WebSocket Events

| Event | Direction | Purpose |
|-------|----------|---------|
| `join_session` | Client → Server | Join analysis session |
| `new_message` | Server → Client | Real-time messages |
| `progress_update` | Server → Client | Progress updates |
| `agent_status_update` | Server → Client | Agent status changes |
| `report_update` | Server → Client | Report completion |

### Configuration Templates

#### Minimal Analysis
```json
{
  "secret_pass": "your_password",
  "ticker": "BTC",
  "analysis_date": "2024-05-10",
  "analysts": ["market_analyst"],
  "llm_provider": "openai",
  "research_depth": "basic"
}
```

#### Comprehensive Analysis
```json
{
  "secret_pass": "your_password",
  "ticker": "ETH",
  "analysis_date": "2024-05-10",
  "analysts": [
    "market_analyst",
    "social_analyst", 
    "news_analyst",
    "fundamentals_analyst"
  ],
  "llm_provider": "anthropic",
  "shallow_thinker": "claude-3-5-haiku",
  "deep_thinker": "claude-3-opus",
  "research_depth": "comprehensive",
  "language": "english"
}
```

---

## Support & Troubleshooting

### Common Issues

1. **Analysis Timeout**
   - Check network connectivity
   - Verify API keys are valid
   - Consider reducing research depth

2. **WebSocket Connection Issues**
   - Ensure CORS is properly configured
   - Check firewall settings
   - Verify Socket.IO client version

3. **Memory Issues**
   - Monitor session cleanup
   - Implement session limits
   - Consider Redis for session storage

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export DEBUG=true
```

This will provide detailed logs for troubleshooting.

---

## License & Disclaimer

This API is provided for research and educational purposes. Trading decisions should not be based solely on automated analysis. Always conduct your own research and consider consulting with financial professionals.

**This is not financial advice.**

---

*Last Updated: May 2024*
*Version: 1.0.0*
