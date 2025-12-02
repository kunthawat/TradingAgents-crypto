import os
from dotenv import load_dotenv

# Load environment variables from .env file, overriding existing ones
load_dotenv(override=True)

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": os.getenv("TRADINGAGENTS_DATA_DIR", "./data"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "openai",
    "deep_think_llm": "zai-org/GLM-4.6",
    "quick_think_llm": "zai-org/GLM-4.6",
    "backend_url": os.getenv("LLM_URL", "https://llm.chutes.ai/v1"),
    "embeddings_url": os.getenv("EMBEDDINGS_URL", "https://chutes-qwen-qwen3-embedding-8b.chutes.ai/v1/embeddings"),
    "api_key": os.getenv("OPENAI_API_KEY", ""),
    # Gold Price API settings
    "goldapi_key": os.getenv("GOLDAPI_KEY", ""),
    "gold_api": {
        "base_url": "https://fcsapi.com/api-v3/forex",
        "history_endpoint": "/history",
        "symbol_id": "1984",  # XAU/USD
        "period": "1d",  # Daily candles
        "max_candles": 300,  # FCSAPI provides last 300 candles
        "rate_limit": 60,  # requests per hour (conservative estimate)
        "timeout": 30,  # seconds
        "cache_ttl": 1800  # 30 minutes cache for 300-candle dataset
    },
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
}
