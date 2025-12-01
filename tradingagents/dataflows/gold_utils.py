import requests
import pandas as pd
import json
import os
from typing import Dict, List, Optional, Any, Annotated
from datetime import datetime, timedelta
import time
from .config import DATA_DIR


class GoldPriceAPIError(Exception):
    """Custom exception for Gold Price API errors"""
    pass


class GoldPriceAPI:
    """Gold Price API utilities for gold trading data - migrated to gold-api.com"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.gold-api.com"
        self.api_key = api_key or os.getenv("GOLDAPI_KEY")
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("GOLDAPI_KEY environment variable is required for Gold Price API")
        
        self.session.headers.update({
            'x-api-key': self.api_key
        })
        
        # Rate limiting - new API has 10 requests/hour limit for free tier
        self.last_request_time = 0
        self.min_request_interval = 360.0  # 6 minutes between requests (10/hour)
        
        # Cache for rate limiting
        self._cache = {}
        self._cache_ttl = 3600  # 1 hour cache
    
    def _date_to_timestamp(self, date_str: str) -> int:
        """Convert date string to Unix timestamp"""
        try:
            return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())
        except ValueError:
            raise GoldPriceAPIError(f"Invalid date format: {date_str}. Use yyyy-mm-dd format.")
    
    def _get_cache_key(self, endpoint: str, params: Dict = None) -> str:
        """Generate cache key for requests"""
        key = endpoint
        if params:
            key += "_" + "_".join(f"{k}:{v}" for k, v in sorted(params.items()))
        return key
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Get data from cache if available and not expired"""
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                return cached_data
            else:
                del self._cache[cache_key]
        return None
    
    def _store_in_cache(self, cache_key: str, data: Dict):
        """Store data in cache"""
        self._cache[cache_key] = (data, time.time())
    
    def _make_request(self, endpoint: str, params: Dict = None, use_cache: bool = True) -> Dict:
        """Make API request with error handling, rate limiting, and caching"""
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(endpoint, params)
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                print(f"📋 Using cached data for {endpoint}")
                return cached_data
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            print(f"⏳ Rate limiting: waiting {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            self.last_request_time = time.time()
            
            # Handle rate limiting explicitly
            if response.status_code == 429:
                raise GoldPriceAPIError("Gold price API rate limit exceeded. Please try again later.")
            
            # Handle other HTTP errors
            if response.status_code == 401:
                raise GoldPriceAPIError("Invalid API key for gold price service.")
            elif response.status_code == 403:
                raise GoldPriceAPIError("Access forbidden to gold price API.")
            elif response.status_code == 404:
                raise GoldPriceAPIError("Gold price API endpoint not found.")
            elif response.status_code >= 500:
                raise GoldPriceAPIError("Gold price service temporarily unavailable.")
            
            response.raise_for_status()
            data = response.json()
            
            # Store in cache
            if use_cache:
                self._store_in_cache(cache_key, data)
            
            return data
            
        except requests.exceptions.Timeout:
            raise GoldPriceAPIError("Request to gold price API timed out.")
        except requests.exceptions.ConnectionError:
            raise GoldPriceAPIError("Unable to connect to gold price service. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise GoldPriceAPIError(f"Network error accessing gold price API: {str(e)}")
        except json.JSONDecodeError:
            raise GoldPriceAPIError("Invalid response format from gold price API.")
    
    def get_current_gold_price(self) -> Dict:
        """
        Get current gold price data
        
        Returns:
            Dict containing current gold price information
        
        Raises:
            GoldPriceAPIError: If API request fails
        """
        return self._make_request("/price/XAU")
    
    def get_gold_history(self, start_date: Optional[str] = None, end_date: Optional[str] = None, 
                        group_by: str = "day", aggregation: str = "max") -> Dict:
        """
        Get gold price history data
        
        Args:
            start_date: Start date in yyyy-mm-dd format (optional)
            end_date: End date in yyyy-mm-dd format (optional)
            group_by: Time grouping - year, month, week, day (default: day)
            aggregation: Price aggregation - max, min, avg (default: max)
        
        Returns:
            Dict containing gold price history data
        
        Raises:
            GoldPriceAPIError: If API request fails
        """
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date_obj = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=30)
            start_date = start_date_obj.strftime("%Y-%m-%d")
        
        # Convert dates to Unix timestamps
        start_timestamp = self._date_to_timestamp(start_date)
        end_timestamp = self._date_to_timestamp(end_date)
        
        params = {
            'symbol': 'XAU',
            'startTimestamp': start_timestamp,
            'endTimestamp': end_timestamp,
            'groupBy': group_by,
            'aggregation': aggregation
        }
        
        return self._make_request("/history", params)
    
    def parse_gold_data(self, api_response: Dict) -> pd.DataFrame:
        """
        Parse API response to pandas DataFrame for analysis
        
        Args:
            api_response: Response from Gold Price API (new gold-api.com format)
        
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        
        Raises:
            GoldPriceAPIError: If data parsing fails or data is invalid
        """
        if not api_response:
            raise GoldPriceAPIError("No response received from gold price API.")
        
        # Handle new gold-api.com response format
        if isinstance(api_response, list):
            # New API format: [{"day":"2025-12-01 00:00:00","max_price":"4255.6001"}, ...]
            history_data = api_response
        elif isinstance(api_response, dict):
            # Current price format: {"name":"Gold","price":4235.700195,"symbol":"XAU","updatedAt":"..."}
            if 'price' in api_response and 'name' in api_response:
                # Convert single price response to DataFrame
                current_time = datetime.now()
                price_data = [{
                    'date': current_time.strftime('%Y-%m-%d'),
                    'max_price': str(api_response['price'])
                }]
                history_data = price_data
            else:
                raise GoldPriceAPIError(f"Unknown API response format: {list(api_response.keys())}")
        else:
            raise GoldPriceAPIError(f"Unknown API response type: {type(api_response)}")
        
        if not history_data:
            raise GoldPriceAPIError("No price history data found in API response.")
        
        # Convert to DataFrame
        df = pd.DataFrame(history_data)
        
        # Handle different column names from new API
        if 'day' in df.columns:
            df.rename(columns={'day': 'date'}, inplace=True)
        
        # Find the price column (could be max_price, min_price, avg_price)
        price_column = None
        for col in ['max_price', 'min_price', 'avg_price', 'price']:
            if col in df.columns:
                price_column = col
                break
        
        if not price_column:
            raise GoldPriceAPIError(f"No price column found in API response. Available columns: {list(df.columns)}")
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Convert price to numeric
        df['price'] = pd.to_numeric(df[price_column], errors='coerce')
        
        # Create OHLCV structure from single price data
        # Since new API only provides aggregated prices, use the same value for all OHLC
        df['open'] = df['price']
        df['high'] = df['price']
        df['low'] = df['price']
        df['close'] = df['price']
        df['volume'] = 0  # New API doesn't provide volume data
        
        # Select and reorder columns
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        
        # Check for invalid data
        if (df[['open', 'high', 'low', 'close']] == 0).any().any():
            raise GoldPriceAPIError("Invalid price data detected (zero values) in API response.")
        
        if df[['open', 'high', 'low', 'close']].isnull().any().any():
            raise GoldPriceAPIError("Missing price data (null values) in API response.")
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        # Calculate additional metrics (adapted for single price data)
        df['price_range'] = 0  # No range since all OHLC are the same
        df['daily_change'] = df['close'].diff()
        df['daily_change_pct'] = df['daily_change'].pct_change(fill_method=None) * 100
        df['typical_price'] = df['close']  # Same as close since no OHLC variation
        df['weighted_price'] = df['close']  # Same as close
        
        print(f"✅ Successfully parsed {len(df)} rows of gold data from gold-api.com")
        print(f"⚠️  Note: Using aggregated price data for all OHLC values (API limitation)")
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
        
        df = api.parse_gold_data(raw_data)
        
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
        
    except GoldPriceAPIError as e:
        return f"Gold Price API Error: {str(e)}"
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
        df = api.parse_gold_data(raw_data)
        
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
        
    except GoldPriceAPIError as e:
        return f"Gold Price API Error: {str(e)}"
    except Exception as e:
        return f"Error retrieving technical analysis for {symbol}: {str(e)}"
