# TradingAgents Crypto - Complete API Usage Guide

## Overview
Yes, this application **fully supports API** for analyzing BTC and other cryptocurrencies. The API provides comprehensive trading analysis using multiple AI agents.

## API Endpoints

### 1. Start BTC Analysis
**Endpoint:** `POST /api/start_analysis`

**URL:** `http://localhost:5001/api/start_analysis` (or your deployed URL)

### 2. Request Format

#### Headers:
```
Content-Type: application/json
```

#### Body Parameters:
```json
{
  "ticker": "BTC",
  "analysis_date": "2025-11-24",
  "analysts": ["fundamentals", "market", "news"],
  "research_depth": 2,
  "llm_provider": "openai",
  "shallow_thinker": "deepseek-ai/DeepSeek-R1-0528",
  "deep_thinker": "deepseek-ai/DeepSeek-R1-0528",
  "language": "english",
  "secret_pass": "your_secret_password_here",
  "session_id": "unique_session_id"
}
```

#### Parameter Details:
- **ticker**: Cryptocurrency symbol (e.g., "BTC", "ETH", "SOL")
- **analysis_date**: Date for analysis (YYYY-MM-DD format)
- **analysts**: Array of analysis types to run
  - `"fundamentals"` - Fundamental analysis
  - `"market"` - Market technical analysis  
  - `"news"` - News sentiment analysis
  - `"social"` - Social media sentiment
- **research_depth**: Analysis depth (1-3, higher = more thorough)
- **llm_provider**: AI provider ("openai", "anthropic", "google")
- **shallow_thinker**: Model for quick analysis
- **deep_thinker**: Model for deep analysis
- **language**: Output language ("english" or "thai")
- **secret_pass**: Security password (required)
- **session_id**: Unique identifier for tracking

### 3. Response Format

#### Success Response:
```json
{
  "session_id": "test_session_001",
  "status": "started"
}
```

#### Error Response:
```json
{
  "error": "Invalid password"
}
```

## Complete BTC Analysis Example

### HTTP Request:
```bash
curl -X POST "http://127.0.0.1:5001/api/start_analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BTC",
    "analysis_date": "2025-11-24",
    "analysts": ["fundamentals", "market", "news", "social"],
    "research_depth": 3,
    "llm_provider": "openai",
    "shallow_thinker": "deepseek-ai/DeepSeek-R1-0528",
    "deep_thinker": "deepseek-ai/DeepSeek-R1-0528",
    "language": "english",
    "secret_pass": "your_secret_password_here",
    "session_id": "btc_analysis_2025_11_24"
  }'
```

### Response:
```json
{
  "session_id": "btc_analysis_2025_11_24",
  "status": "started"
}
```

## What Happens After API Call?

### 1. Analysis Process
The API starts a **background analysis** that includes:
- **Market Analyst**: Technical analysis and price patterns
- **Fundamentals Analyst**: On-chain metrics and fundamentals
- **News Analyst**: News sentiment and impact analysis
- **Social Analyst**: Social media sentiment (Reddit, Twitter)
- **Bull Researcher**: Bullish investment thesis
- **Bear Researcher**: Bearish investment thesis
- **Research Manager**: Final investment recommendation
- **Trader**: Trading strategy and execution plan
- **Risk Management Team**: Risk assessment and position sizing

### 2. Real-time Updates
The analysis provides **real-time updates** via WebSocket connections:
- Agent status updates
- Progress tracking
- Intermediate results
- Final reports

### 3. Final Results
The analysis returns comprehensive results including:
- **Market Report**: Technical analysis findings
- **Fundamentals Report**: On-chain metrics analysis
- **News Report**: News sentiment and impact
- **Social Sentiment Report**: Social media analysis
- **Investment Plan**: Research team recommendation
- **Trading Plan**: Specific trading strategy
- **Final Trade Decision**: Final investment decision

## Additional API Endpoints

### Health Check
```bash
GET /health
```
Returns service status and health information.

### Web Interface
```bash
GET /
```
Returns the web interface for manual analysis.

## Deployment Options

### 1. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_PASS="your_secret_password_here"
export OPENAI_API_KEY="your_api_key"

# Run the server
python3 web_app.py
```

### 2. Docker Deployment
```bash
# Build image
docker build -t tradingagents-crypto .

# Run container
docker run -p 5001:5000 \
  -e SECRET_PASS="your_secret_password_here" \
  -e OPENAI_API_KEY="your_api_key" \
  tradingagents-crypto
```

### 3. Cloud Deployment (Google Cloud Run)
```bash
# Deploy to Cloud Run
gcloud run deploy tradingagents-crypto \
  --image gcr.io/your-project/tradingagents-crypto \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Security

### Authentication
- API requires **secret password** authentication
- Password is set via `SECRET_PASS` environment variable
- Default password: `your_secret_password_here` (change in production)

### API Keys
- Requires valid LLM API keys (OpenAI, Anthropic, or Google)
- Keys are set via environment variables
- Keys are never exposed in API responses

## Rate Limiting

- No built-in rate limiting (add as needed)
- Analysis can take 2-10 minutes depending on complexity
- Multiple concurrent sessions supported

## Error Handling

### Common Errors:
1. **401 Unauthorized**: Invalid secret password
2. **500 Internal Server Error**: Analysis failure
3. **400 Bad Request**: Invalid parameters

### Error Response Format:
```json
{
  "error": "Error description"
}
```

## Monitoring

### Logs
Analysis progress and errors are logged to console:
```
[DEBUG] Starting analysis for session test_session_001
[DEBUG] Selected analysts: ['fundamentals', 'market', 'news']
[DEBUG] Graph initialized successfully
```

### WebSocket Events
For real-time monitoring, connect to WebSocket events:
- `new_message`: Analysis updates
- `agent_status_update`: Agent progress
- `report_update`: Report sections
- `progress_update`: Overall progress

## Summary

**Yes, this app fully supports API for BTC analysis!**

✅ **HTTP Endpoint**: `POST /api/start_analysis`  
✅ **BTC Analysis**: Comprehensive multi-agent analysis  
✅ **Real-time Results**: WebSocket updates and final reports  
✅ **Authentication**: Password-protected API  
✅ **Deployment**: Docker, Cloud Run, or local hosting  
✅ **Response Format**: JSON with session tracking  

The API provides professional-grade cryptocurrency analysis using multiple AI agents and returns detailed investment recommendations, trading strategies, and risk assessments.
