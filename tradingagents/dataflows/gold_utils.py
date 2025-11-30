import requests
import pandas as pd
import json
import os
from typing import Dict, List, Optional, Any, Annotated
from datetime import datetime, timedelta
import time
from .config import DATA_DIR


class GoldPriceAPI:
    """Gold Price API utilities for gold trading data"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://gold-price-api.p.rapidapi.com/v1"
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY environment variable is required for Gold Price API")
        
        self.session.headers.update({
            'x-rapidapi-host': 'gold-price-api.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with error handling and rate limiting"""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            self.last_request_time = time.time()
            
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting before retry...")
                time.sleep(5)
                response = self.session.get(url, params=params)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return {}
    
    def get_gold_history(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        """
        Get gold price history data
        
        Args:
            start_date: Start date in yyyy-mm-dd format (optional)
            end_date: End date in yyyy-mm-dd format (optional)
        
        Returns:
            Dict containing gold price history with OHLCV data
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        return self._make_request("/gold/history", params)
    
    def get_current_gold_price(self) -> Dict:
        """
        Get current gold price data
        
        Returns:
            Dict containing current gold price information
        """
        return self._make_request("/gold/current")
    
    def parse_gold_data(self, api_response: Dict) -> pd.DataFrame:
        """
        Parse API response to pandas DataFrame for analysis
        
        Args:
            api_response: Response from Gold Price API
        
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        if not api_response or 'history' not in api_response:
            return pd.DataFrame()
        
        history_data = api_response['history']
        if not history_data:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(history_data)
        
        # Ensure proper data types
        df['date'] = pd.to_datetime(df['date'])
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        # Calculate additional metrics
        df['price_range'] = df['high'] - df['low']
        df['daily_change'] = df['close'] - df['open']
        df['daily_change_pct'] = (df['daily_change'] / df['open']) * 100
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        df['weighted_price'] = (df['high'] + df['low'] + 2 * df['close']) / 4
        
        return df
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators from OHLCV data
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with additional technical indicator columns
        """
        if df.empty:
            return df
        
        # Simple Moving Averages
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['ema_10'] = df['close'].ewm(span=10).mean()
        df['ema_20'] = df['close'].ewm(span=20).mean()
        
        # RSI (Relative Strength Index)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = df['close'].ewm(span=12).mean()
        ema_26 = df['close'].ewm(span=26).mean()
        df['macd'] = ema_12 - ema_26
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_position'] = (df['close'] - df['bb_lower']) / df['bb_width']
        
        # Volume indicators
        if 'volume' in df.columns:
            df['volume_sma'] = df['volume'].rolling(window=20).mean()
            df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        # Price volatility
        df['volatility'] = df['daily_change_pct'].rolling(window=20).std()
        
        # Price momentum
        df['momentum_5'] = df['close'].pct_change(periods=5)
        df['momentum_10'] = df['close'].pct_change(periods=10)
        
        return df
    
    def get_gold_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for gold data
        
        Args:
            df: DataFrame with gold price data
        
        Returns:
            Dict containing summary statistics
        """
        if df.empty:
            return {}
        
        latest = df.iloc[-1]
        earliest = df.iloc[0] if len(df) > 1 else latest
        
        summary = {
            'current_price': latest['close'],
            'price_change': latest['close'] - earliest['close'],
            'price_change_pct': ((latest['close'] - earliest['close']) / earliest['close']) * 100,
            'period_high': df['high'].max(),
            'period_low': df['low'].min(),
            'avg_volume': df['volume'].mean() if 'volume' in df.columns else 0,
            'volatility': df['daily_change_pct'].std(),
            'data_points': len(df),
            'date_range': {
                'start': earliest['date'].strftime('%Y-%m-%d'),
                'end': latest['date'].strftime('%Y-%m-%d')
            }
        }
        
        # Add latest technical indicators
        if 'rsi' in df.columns:
            summary['current_rsi'] = latest['rsi']
        if 'macd' in df.columns:
            summary['current_macd'] = latest['macd']
        if 'bb_position' in df.columns:
            summary['bb_position'] = latest['bb_position']
        
        return summary


def get_gold_price_data(
    symbol: Annotated[str, "Gold symbol like GOLD, XAU"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Get gold price data for a specific time range
    
    Args:
        symbol: Gold symbol (e.g., 'GOLD', 'XAU')
        start_date: Start date in yyyy-mm-dd format
        end_date: End date in yyyy-mm-dd format
    
    Returns:
        String representation of gold price data
    """
    try:
        api = GoldPriceAPI()
        raw_data = api.get_gold_history(start_date, end_date)
        
        if not raw_data:
            return f"No gold price data available for {symbol} from {start_date} to {end_date}"
        
        df = api.parse_gold_data(raw_data)
        if df.empty:
            return f"No valid gold price data found for {symbol}"
        
        # Format the data for output
        result_str = f"## {symbol.upper()} Gold Price Data from {start_date} to {end_date}:\n\n"
        
        # Show recent data (last 10 days)
        recent_data = df.tail(10)
        for _, row in recent_data.iterrows():
            result_str += f"Date: {row['date'].strftime('%Y-%m-%d')}\n"
            result_str += f"Open: ${row['open']:,.2f}\n"
            result_str += f"High: ${row['high']:,.2f}\n"
            result_str += f"Low: ${row['low']:,.2f}\n"
            result_str += f"Close: ${row['close']:,.2f}\n"
            result_str += f"Volume: {row['volume']:,.0f}\n"
            result_str += f"Daily Change: {row['daily_change_pct']:+.2f}%\n\n"
        
        # Add summary
        summary = api.get_gold_summary(df)
        result_str += f"## Summary Statistics:\n\n"
        result_str += f"Period Return: {summary['price_change_pct']:+.2f}%\n"
        result_str += f"Period High: ${summary['period_high']:,.2f}\n"
        result_str += f"Period Low: ${summary['period_low']:,.2f}\n"
        result_str += f"Average Volume: {summary['avg_volume']:,.0f}\n"
        result_str += f"Volatility: {summary['volatility']:.2f}%\n"
        
        return result_str
        
    except Exception as e:
        return f"Error retrieving gold price data for {symbol}: {str(e)}"


def get_gold_technical_analysis(
    symbol: Annotated[str, "Gold symbol like GOLD, XAU"],
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "How many days to look back"] = 30,
) -> str:
    """
    Get technical analysis for gold
    
    Args:
        symbol: Gold symbol
        curr_date: Current date in yyyy-mm-dd format
        look_back_days: Number of days to analyze
    
    Returns:
        String containing technical analysis
    """
    try:
        api = GoldPriceAPI()
        
        # Calculate start date
        end_date = datetime.strptime(curr_date, "%Y-%m-%d")
        start_date = end_date - timedelta(days=look_back_days)
        start_date_str = start_date.strftime("%Y-%m-%d")
        
        # Get data
        raw_data = api.get_gold_history(start_date_str, curr_date)
        if not raw_data:
            return f"No technical data available for {symbol}"
        
        df = api.parse_gold_data(raw_data)
        if df.empty:
            return f"No valid gold data found for {symbol}"
        
        # Calculate technical indicators
        df = api.calculate_technical_indicators(df)
        
        # Get latest data
        latest = df.iloc[-1]
        
        result_str = f"## {symbol.upper()} Technical Analysis (Past {look_back_days} days):\n\n"
        
        # Price levels
        result_str += f"**Price Levels:**\n"
        result_str += f"- Current Price: ${latest['close']:,.2f}\n"
        result_str += f"- 10-day SMA: ${latest['sma_10']:,.2f}\n"
        result_str += f"- 20-day SMA: ${latest['sma_20']:,.2f}\n"
        result_str += f"- 50-day SMA: ${latest['sma_50']:,.2f}\n"
        result_str += f"- Period High: ${df['high'].max():,.2f}\n"
        result_str += f"- Period Low: ${df['low'].min():,.2f}\n\n"
        
        # Technical indicators
        result_str += f"**Technical Indicators:**\n"
        result_str += f"- RSI (14): {latest['rsi']:.1f}\n"
        result_str += f"- MACD: {latest['macd']:+.2f}\n"
        result_str += f"- MACD Signal: {latest['macd_signal']:+.2f}\n"
        result_str += f"- MACD Histogram: {latest['macd_histogram']:+.2f}\n"
        result_str += f"- Bollinger Band Position: {latest['bb_position']:.2f}\n"
        result_str += f"- Volatility: {latest['volatility']:.2f}%\n\n"
        
        # Volume analysis
        if 'volume_ratio' in df.columns:
            result_str += f"**Volume Analysis:**\n"
            result_str += f"- Current Volume: {latest['volume']:,.0f}\n"
            result_str += f"- Volume Ratio (20-day avg): {latest['volume_ratio']:.2f}\n\n"
        
        # Trend analysis
        trend_10 = "Bullish" if latest['close'] > latest['sma_10'] else "Bearish"
        trend_20 = "Bullish" if latest['close'] > latest['sma_20'] else "Bearish"
        trend_50 = "Bullish" if latest['close'] > latest['sma_50'] else "Bearish"
        
        result_str += f"**Trend Analysis:**\n"
        result_str += f"- 10-day Trend: {trend_10}\n"
        result_str += f"- 20-day Trend: {trend_20}\n"
        result_str += f"- 50-day Trend: {trend_50}\n"
        
        # RSI analysis
        if latest['rsi'] > 70:
            rsi_signal = "Overbought"
        elif latest['rsi'] < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"
        
        result_str += f"- RSI Signal: {rsi_signal}\n"
        
        return result_str
        
    except Exception as e:
        return f"Error retrieving technical analysis for {symbol}: {str(e)}"
