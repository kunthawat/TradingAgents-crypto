# Gold Trading Setup Guide

## 🥇 Can I use this app for Gold trading?

**YES!** You can now use this TradingAgents app for Gold trading. This guide shows you exactly what to fill instead of BTC.

## 🚀 Quick Start

### What to fill instead of BTC:

Simply replace `BTC` with any of these gold symbols:

- **`GOLD`** (recommended)
- **`XAU`** 
- **`XAUUSD`**
- **`GOLD/USD`**
- **`GC=F`**

### Example Setup:

```
Asset Symbol: GOLD
Analysis Date: [today's date]
Analyst Team: [select your preferred analysts]
Research Depth: Standard (3 Rounds)
LLM Provider: OpenAI
Output Language: English
Security: [enter your secret password]
```

## 📋 Step-by-Step Instructions

### 1. Get Your RapidAPI Key
1. Go to [RapidAPI](https://rapidapi.com/)
2. Sign up for an account
3. Search for "Gold Price API"
4. Subscribe to the API (free tier available)
5. Copy your API key

### 2. Configure Environment
Add this line to your `.env` file:
```bash
RAPIDAPI_KEY=your_actual_api_key_here
```

### 3. Start the Web App
```bash
python web_app.py
```

### 4. Configure Gold Analysis
1. Open your browser to `http://localhost:5000`
2. In the "Asset Symbol" field, type `GOLD` (or `XAU`)
3. You'll see the help text turn amber: "Gold trading symbol detected"
4. Fill in the analysis date (defaults to today)
5. Select your preferred analysts
6. Configure other settings as needed
7. Enter your secret password
8. Click "Start Analysis"

## 🎯 What Happens Next

The system will automatically:
- ✅ Detect that you're trading gold (not crypto)
- ✅ Fetch real-time gold price data
- ✅ Perform technical analysis (RSI, MACD, Bollinger Bands)
- ✅ Gather gold-specific news and market trends
- ✅ Analyze gold fundamentals (supply/demand, central bank activity)
- ✅ Generate comprehensive trading recommendations

## 📊 Sample Gold Analysis Output

```
## GOLD Gold Market Analysis:

**Current Price:** $2,070.30
**Period Change:** +0.50%
**Period High:** $2,075.80
**Period Low:** $2,055.20
**Average Volume:** 125,000
**Volatility:** 1.20%
**Current RSI:** 65.2
**Current MACD:** +2.15

## Gold Market Context:
Gold is showing moderate strength with RSI above 50, indicating bullish momentum...
```

## 🔧 Advanced Usage

### Programmatic Access
```python
from tradingagents.dataflows.interface import get_asset_data

# Get gold analysis
analysis = get_asset_data("GOLD", "2024-01-01")
print(analysis)

# Check asset type
from tradingagents.dataflows.interface import detect_asset_type
asset_type = detect_asset_type("GOLD")  # Returns: 'gold'
```

### Different Gold Symbols
```python
# All these work the same way
get_asset_data("GOLD", "2024-01-01")
get_asset_data("XAU", "2024-01-01") 
get_asset_data("XAUUSD", "2024-01-01")
```

## 🛠️ Troubleshooting

### "Unknown asset type" Error
**Solution**: Make sure you're using one of the supported gold symbols:
- ✅ `GOLD`, `XAU`, `XAUUSD`, `GOLD/USD`, `GC=F`
- ❌ `GOLDUSD`, `AU`, `GOLD.XAU`

### API Key Issues
**Error**: `Missing RAPIDAPI_KEY environment variable`
**Solution**: 
1. Check your `.env` file exists
2. Ensure `RAPIDAPI_KEY=your_key` is on its own line
3. Restart the web app

### Rate Limiting
**Error**: `429 Too Many Requests`
**Solution**: 
- Free tier has 100 requests/hour limit
- Wait a bit before trying again
- Consider upgrading to paid tier for heavy usage

## 📈 Gold vs Crypto Analysis

The system automatically adjusts its analysis based on asset type:

| Feature | Crypto Analysis | Gold Analysis |
|---------|----------------|---------------|
| **Price Data** | CoinGecko API | RapidAPI Gold API |
| **Technical Indicators** | Standard crypto TA | Gold-specific TA |
| **News Sources** | Crypto news sites | Gold market news |
| **Fundamentals** | Token economics, adoption | Supply/demand, central banks |
| **Market Context** | DeFi, NFTs, regulations | Inflation, USD strength, safe-haven |

## 🎨 UI Indicators

The web interface helps you know you're set up correctly:

- 🟢 **Green text** = Cryptocurrency detected
- 🟡 **Amber text** = Gold detected  
- ⚪ **Default text** = Unknown symbol

When you type `GOLD`, you should see:
> "Gold trading symbol detected (e.g., GOLD, XAU)"

## 🔒 Security Notes

- Your RapidAPI key is stored securely in environment variables
- No sensitive data is logged or exposed
- All API calls use HTTPS encryption
- The system only accesses public market data

## 📞 Support

If you encounter issues:

1. **Check the logs**: Look for error messages in the console
2. **Verify your API key**: Ensure it's valid and active
3. **Test connectivity**: Try the API directly first
4. **Check symbol format**: Use exact symbol formats listed above

## 🚀 Ready to Start?

**Your setup should look like this:**

```
Asset Symbol: GOLD
Analysis Date: 2024-01-01
Analyst Team: [selected]
Research Depth: Standard (3 Rounds)
LLM Provider: OpenAI
Output Language: English
Security: [your password]
```

**Click "Start Analysis" and you're ready to trade gold! 🥇**

---

## 📚 Additional Resources

- [Full Documentation](GOLD_TRADING_DOCUMENTATION.md)
- [Test Suite](test_gold_trading_integration.py)
- [API Setup Guide](https://rapidapi.com/hub)
- [GitHub Repository](https://github.com/0x0funky/TradingAgents-crypto)

**Happy Gold Trading! 🏆**
