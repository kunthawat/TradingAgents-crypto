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


def create_social_media_analyst(llm, toolkit, language_prompt=""):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        # Check if we're dealing with crypto, gold, or stocks
        asset_type = _detect_asset_type(ticker)
        
        if asset_type == 'crypto':
            # Use crypto-specific tools
            if toolkit.config["online_tools"]:
                tools = [toolkit.get_stock_news_openai]  # This will search for crypto social media
            else:
                tools = [toolkit.get_reddit_stock_info]  # Reddit discussions for crypto
            
            system_message = (
                language_prompt +
                """ 

You are a cryptocurrency social media and community researcher/analyst tasked with analyzing social media posts, recent crypto news, and public sentiment for a specific cryptocurrency over the past week. You will be given a cryptocurrency's name your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors on this cryptocurrency's current state after looking at social media and what people are saying about that cryptocurrency, analyzing sentiment data of what people feel each day about the cryptocurrency, and looking at recent crypto news. 
Focus on crypto-specific social media platforms and communities like Twitter/X, Reddit crypto subreddits, Telegram groups, Discord channels, and crypto forums. Pay attention to developer activity, community engagement, influencer opinions, and market sentiment trends. 
Try to look at all sources possible from social media to sentiment to news. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help crypto traders make decisions."""
                + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read.""",
            )
        elif asset_type == 'gold':
            # Use gold-specific tools
            if toolkit.config["online_tools"]:
                tools = [toolkit.get_stock_news_openai]  # This will search for gold social media
            else:
                tools = [toolkit.get_reddit_stock_info]  # Reddit discussions for gold
            
            system_message = (
                language_prompt +
                """ 

You are a gold market social media and sentiment researcher/analyst tasked with analyzing social media posts, recent gold news, and public sentiment for gold over the past week. You will be analyzing gold as a commodity and investment asset. Your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors on gold's current state after looking at social media and what people are saying about gold, analyzing sentiment data of what people feel each day about gold, and looking at recent gold-related news. 
Focus on gold-specific discussions around inflation hedging, safe-haven demand, central bank policies, economic uncertainty, jewelry demand, mining activities, and investment flows. Pay attention to discussions in financial forums, precious metals communities, and economic commentary. 
Try to look at all sources possible from social media to sentiment to news. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help gold traders make decisions."""
                + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read.""",
            )
        else:
            # Use stock-specific tools (original functionality)
            if toolkit.config["online_tools"]:
                tools = [toolkit.get_stock_news_openai]
            else:
                tools = [
                    toolkit.get_reddit_stock_info,
                ]

            system_message = (
                language_prompt +
                """ 

You are a social media and company specific news researcher/analyst tasked with analyzing social media posts, recent company news, and public sentiment for a specific company over the past week. You will be given a company's name your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors on this company's current state after looking at social media and what people are saying about that company, analyzing sentiment data of what people feel each day about the company, and looking at recent company news. Try to look at all sources possible from social media to sentiment to news. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."""
                + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read.""",
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
                    "For your reference, the current date is {current_date}. The current company we want to analyze is {ticker}",
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
            "sentiment_report": report,
        }

    return social_media_analyst_node
