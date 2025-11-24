# TradingAgents API Usage Guide - Port 5000

## Quick Start

Your TradingAgents application is now configured to run on **port 5000** for both web interface and API access.

## Docker Commands

### Build and Run
```bash
# Build the Docker image
docker build -t tradingagents .

# Run on port 5000
docker run -p 5000:5000 tradingagents

# Run with environment variables (optional)
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=your_openai_key \
  -e SECRET_PASS=your_secret_password \
  tradingagents
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python web_app.py

# Or run the test script
python test_api_port_5000.py
```

## API Endpoints

### Base URL
```
http://localhost:5000
```

### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-05-10T10:30:00",
  "service": "TradingAgents Crypto"
}
```

### 2. API Information
```bash
GET /api/info
```

**Response:**
```json
{
  "name": "Trading Agents Crypto",
  "environment": "Development",
  "mode": "Full Analysis",
  "features": ["Real-time analysis", "Multiple analysts", "WebSocket support"]
}
```

### 3. Start BTC Analysis
```bash
POST /api/start_analysis
```

**Request Body:**
```json
{
  "ticker": "BTC",
  "analysis_date": "2024-05-10",
  "llm_provider": "openai",
  "shallow_thinker": "gpt-4o-mini",
  "deep_thinker": "gpt-4o",
  "research_depth": "comprehensive",
  "analysts": ["market", "news", "social", "fundamentals"],
  "secret_pass": "your_secret_password"
}
```

**Response:**
```json
{
  "session_id": "uuid-string-here",
  "status": "started"
}
```

### 4. Check Analysis Status
```bash
GET /api/status/{session_id}
```

**Response:**
```json
{
  "messages": [
    {
      "timestamp": "10:30:15",
      "type": "System",
      "content": "Initializing analysis for BTC..."
    }
  ],
  "agent_status": {
    "Market Analyst": "completed",
    "News Analyst": "in_progress",
    "Social Analyst": "pending",
    "Fundamentals Analyst": "pending"
  },
  "report_sections": {
    "market_report": "Market analysis shows...",
    "sentiment_report": null,
    "news_report": null,
    "fundamentals_report": null,
    "investment_plan": null,
    "trader_investment_plan": null,
    "final_trade_decision": null
  },
  "progress": 45,
  "current_step": "News analysis in progress",
  "status": "running"
}
```

## Complete API Workflow Example

### Step 1: Start BTC Analysis
```bash
curl -X POST http://localhost:5000/api/start_analysis \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BTC",
    "analysis_date": "2024-05-10",
    "llm_provider": "openai",
    "shallow_thinker": "gpt-4o-mini",
    "deep_thinker": "gpt-4o",
    "research_depth": "comprehensive",
    "analysts": ["market", "news", "social", "fundamentals"],
    "secret_pass": "your_secret_password"
  }'
```

### Step 2: Get Session ID from Response
```json
{
  "session_id": "abc123-def456-ghi789",
  "status": "started"
}
```

### Step 3: Monitor Progress
```bash
# Check status every 30 seconds
curl http://localhost:5000/api/status/abc123-def456-ghi789
```

### Step 4: Get Final Results
When `status` is `"completed"` and `progress` is `100`, the `report_sections` will contain:

```json
{
  "report_sections": {
    "market_report": "Detailed market analysis...",
    "sentiment_report": "Social sentiment analysis...",
    "news_report": "News impact analysis...",
    "fundamentals_report": "Fundamental analysis...",
    "investment_plan": "Research team recommendation...",
    "trader_investment_plan": "Trading strategy...",
    "final_trade_decision": "Final trading decision: BUY/SELL/HOLD with reasoning..."
  }
}
```

## Configuration Options

### Analyst Types
- `"market"` - Market Analyst (price trends, technical analysis)
- `"news"` - News Analyst (news impact analysis)
- `"social"` - Social Analyst (social media sentiment)
- `"fundamentals"` - Fundamentals Analyst (fundamental analysis)

### Research Depth
- `"quick"` - Fast analysis (2-3 minutes)
- `"comprehensive"` - Full analysis (5-10 minutes)

### LLM Providers
- `"openai"` - OpenAI GPT models
- `"anthropic"` - Anthropic Claude models
- `"google"` - Google Gemini models

## Environment Variables

```bash
# Required for API access
SECRET_PASS=your_secret_password_here

# Required for analysis
OPENAI_API_KEY=sk-your-openai-key-here

# Optional
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
ENVIRONMENT=production
```

## Web Interface

Access the full web interface at:
```
http://localhost:5000
```

Features:
- Real-time analysis progress
- Interactive charts
- Historical analysis results
- Configuration management

## Troubleshooting

### Connection Refused
```bash
# Check if server is running
lsof -i :5000

# Start server manually
python web_app.py
```

### API Key Issues
```bash
# Check environment variables
docker exec -it container_name env | grep API

# Set proper environment variables
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=your_key \
  -e SECRET_PASS=your_password \
  tradingagents
```

### Analysis Fails
```bash
# Check logs
docker logs container_name

# Test API connectivity
python test_api_port_5000.py
```

## Testing

Run the comprehensive test suite:
```bash
python test_api_port_5000.py
```

This will test:
- Health endpoint
- API info endpoint
- Analysis endpoint
- Session status endpoint
- Web interface accessibility

## Production Deployment

For production deployment, consider:
1. Use environment variables for all secrets
2. Enable HTTPS with reverse proxy (nginx/traefik)
3. Set up proper logging and monitoring
4. Use container orchestration (Kubernetes/Docker Swarm)
5. Implement rate limiting and authentication

## Support

If you encounter issues:
1. Check the test script output
2. Review Docker logs
3. Verify environment variables
4. Ensure port 5000 is available
5. Check API key validity
