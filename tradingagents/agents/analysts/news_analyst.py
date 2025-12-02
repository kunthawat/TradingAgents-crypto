from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def _detect_asset_type(symbol: str) -> str:
    """
    Detect if a symbol is crypto, gold, or stock
    Returns: 'crypto', 'gold', or 'stock'
    """
    # Gold symbols - ALWAYS prioritize gold over crypto
    gold_symbols = {'GOLD', 'XAU', 'XAUUSD', 'GOLD/USD', 'GC=F'}
    
    # Known crypto symbols (most common ones)
    crypto_symbols = {
        'BTC', 'ETH', 'ADA', 'SOL', 'DOT', 'AVAX', 'MATIC', 'LINK', 'UNI', 'AAVE',
        'XRP', 'LTC', 'BCH', 'EOS', 'TRX', 'XLM', 'VET', 'ALGO', 'ATOM', 'LUNA',
        'NEAR', 'FTM', 'CRO', 'SAND', 'MANA', 'AXS', 'GALA', 'ENJ', 'CHZ', 'BAT',
        'ZEC', 'DASH', 'XMR', 'DOGE', 'SHIB', 'PEPE', 'FLOKI', 'BNB', 'USDT', 'USDC',
        'TON', 'ICP', 'HBAR', 'THETA', 'FIL', 'ETC', 'MKR', 'APT', 'LDO', 'OP',
        'IMX', 'GRT', 'RUNE', 'FLOW', 'EGLD', 'XTZ', 'MINA', 'ROSE', 'KAVA'
    }
    
    # Known stock symbols (to avoid false positives)
    stock_symbols = {
        'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'DIS', 'AMD',
        'INTC', 'CRM', 'ORCL', 'ADBE', 'CSCO', 'PEP', 'KO', 'WMT', 'JNJ', 'PFE',
        'V', 'MA', 'HD', 'UNH', 'BAC', 'XOM', 'CVX', 'LLY', 'ABBV', 'COST',
        'AVGO', 'TMO', 'ACN', 'DHR', 'TXN', 'LOW', 'QCOM', 'HON', 'UPS', 'MDT'
    }
    
    symbol_upper = symbol.upper()
    
    # Check for gold FIRST - this has highest priority
    if symbol_upper in gold_symbols:
        return 'gold'
    
    # If it's a known stock symbol, it's definitely stock
    if symbol_upper in stock_symbols:
        return 'stock'
    
    # If it's a known crypto symbol, it's definitely crypto
    if symbol_upper in crypto_symbols:
        return 'crypto'
    
    # For unknown symbols, be conservative and assume it's a stock
    # unless it has typical crypto characteristics
    if len(symbol) >= 5:  # Most stocks are 4+ characters
        return 'stock'
    
    # Short symbols (2-4 chars) could be crypto if they don't look like stocks
    if len(symbol) <= 4 and symbol.isalnum() and not any(c in symbol for c in ['.', '-', '_']):
        # Additional heuristic: crypto symbols often have certain patterns
        return 'crypto'
    
    return 'stock'


def _is_crypto_symbol(symbol: str) -> bool:
    """Legacy function for backward compatibility"""
    return _detect_asset_type(symbol) == 'crypto'


def create_news_analyst(llm, toolkit, language_prompt=""):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        # Check if we're dealing with crypto, gold, or stocks
        asset_type = _detect_asset_type(ticker)
        
        if asset_type == 'crypto':
            # Use crypto-specific tools
            tools = [toolkit.get_crypto_news_analysis, toolkit.get_google_news]
            
            system_message = (
                language_prompt +
                """ 

You are a cryptocurrency news researcher tasked with analyzing recent news and trends over the past week that affect cryptocurrency markets. Please write a comprehensive report of the current state of the crypto world and broader macroeconomic factors that are relevant for cryptocurrency trading. 
Focus on crypto-specific news including: regulatory developments, institutional adoption, technology updates, market sentiment, DeFi trends, NFT markets, blockchain developments, and major crypto exchange news. 
Also consider traditional macroeconomic factors that impact crypto markets such as inflation, monetary policy, global economic uncertainty, and traditional market trends. 
Do not simply state the trends are mixed, provide detailed and fine-grained analysis and insights that may help crypto traders make decisions."""
                + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
            )
        elif asset_type == 'gold':
            # Use gold-specific tools
            tools = [toolkit.get_gold_news_analysis, toolkit.get_google_news]
            
            system_message = (
                language_prompt +
                """ 

You are a gold market news researcher tasked with analyzing recent news and trends over the past week that affect gold markets. Please write a comprehensive report of the current state of the gold market and broader macroeconomic factors that are relevant for gold trading. 
Focus on gold-specific news including: inflation data, monetary policy decisions, central bank activities, currency movements, geopolitical tensions, economic uncertainty, mining supply dynamics, jewelry demand, ETF flows, and precious metals market developments. 
Also consider traditional macroeconomic factors that impact gold prices such as interest rates, dollar strength, inflation expectations, and global economic stability. 
Do not simply state the trends are mixed, provide detailed and fine-grained analysis and insights that may help gold traders make decisions."""
                + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
            )
        else:
            # Use stock-specific tools (original functionality)
            if toolkit.config["online_tools"]:
                tools = [toolkit.get_global_news_openai, toolkit.get_google_news]
            else:
                tools = [
                    toolkit.get_finnhub_news,
                    toolkit.get_reddit_news,
                    toolkit.get_google_news,
                ]

            system_message = (
                language_prompt +
                """ 

You are a news researcher tasked with analyzing recent news and trends over the past week. Please write a comprehensive report of the current state of the world that is relevant for trading and macroeconomics. Look at news from EODHD, and finnhub to be comprehensive. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."""
                + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
            )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. We are looking at the company {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)
        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "news_report": report,
        }

    return news_analyst_node
