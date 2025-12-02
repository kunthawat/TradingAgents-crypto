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
    """Gold Price API utilities for gold trading data - migrated to FCSAPI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://fcsapi.com/api-v3/forex"
        self.api_key = api_key or os.getenv("GOLDAPI_KEY")
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("GOLDAPI_KEY environment variable is required for Gold Price API")
        
        # FCSAPI uses access_key parameter, not header
        # Rate limiting - FCSAPI may have different limits
        self.last_request_time = 0
        self.min_request_interval = 60.0  # 1 minute between requests (conservative)
        
        # Cache for the 300-candle dataset
        self._cache = {}
        self._cache_ttl = 1800  # 30 minutes cache for 300-candle dataset
        self._cached_data = None
        self._cache_timestamp = 0
    
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
    
    def _get_fcsapi_data(self, force_refresh: bool = False, max_retries: int = 3) -> Dict:
        """Get the 300-candle dataset from FCSAPI with caching and robust rate limit handling"""
        current_time = time.time()
        
        # Check if we have fresh cached data
        if not force_refresh and self._cached_data and (current_time - self._cache_timestamp < self._cache_ttl):
            print(f"📋 Using cached FCSAPI data ({len(self._cached_data.get('response', {}))} candles)")
            return self._cached_data
        
        # Make API request to FCSAPI with retry logic
        params = {
            'id': '1984',
            'period': '1d',
            'access_key': self.api_key
        }
        
        url = f"{self.base_url}/history"
        
        for attempt in range(max_retries):
            try:
                # Rate limiting between attempts
                time_since_last = current_time - self.last_request_time
                if time_since_last < self.min_request_interval:
                    sleep_time = self.min_request_interval - time_since_last
                    print(f"⏳ Rate limiting: waiting {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)
                
                print(f"🔄 Attempt {attempt + 1}/{max_retries} to fetch FCSAPI data...")
                response = self.session.get(url, params=params, timeout=30)
                self.last_request_time = time.time()
                
                # Handle HTTP errors
                if response.status_code == 401:
                    raise GoldPriceAPIError("Invalid GOLDAPI_KEY for FCSAPI service.")
                elif response.status_code == 403:
                    raise GoldPriceAPIError("Access forbidden to FCSAPI.")
                elif response.status_code == 429:
                    print(f"⚠️  HTTP 429: Rate limit exceeded. Waiting 65 seconds...")
                    time.sleep(65)
                    continue
                elif response.status_code >= 500:
                    print(f"⚠️  Server error {response.status_code}. Retrying in 10 seconds...")
                    time.sleep(10)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                # Check for FCSAPI rate limit error in response body
                response_text = response.text.lower()
                if "access block for you" in response_text or "reached maximum" in response_text:
                    wait_time = 65  # FCSAPI rate limit resets after 1 minute
                    print(f"⚠️  FCSAPI Rate Limit Detected:")
                    print(f"   Message: Access block for you, You have reached maximum 3 limit per minute")
                    print(f"   Action: Waiting {wait_time} seconds for rate limit reset...")
                    
                    # Progress bar for waiting
                    for i in range(wait_time, 0, -1):
                        print(f"⏳ Rate limit reset in: {i} seconds...", end='\r')
                        time.sleep(1)
                    print("\n✅ Rate limit reset period complete. Retrying...")
                    continue
                
                # Check FCSAPI response status
                if not data.get('status', False):
                    error_msg = data.get('msg', 'Unknown FCSAPI error')
                    if "limit" in error_msg.lower() or "access" in error_msg.lower():
                        print(f"⚠️  FCSAPI Limit Error: {error_msg}")
                        print("   Waiting 65 seconds for potential rate limit reset...")
                        time.sleep(65)
                        continue
                    raise GoldPriceAPIError(f"FCSAPI Error: {error_msg}")
                
                if data.get('code') != 200:
                    error_msg = data.get('msg', f"FCSAPI returned code {data.get('code')}")
                    if "limit" in error_msg.lower() or "access" in error_msg.lower():
                        print(f"⚠️  FCSAPI Limit Error: {error_msg}")
                        print("   Waiting 65 seconds for potential rate limit reset...")
                        time.sleep(65)
                        continue
                    raise GoldPriceAPIError(f"FCSAPI Error: {error_msg}")
                
                # Success! Cache the data
                self._cached_data = data
                self._cache_timestamp = current_time
                
                candle_count = len(data.get('response', {}))
                print(f"✅ Retrieved {candle_count} candles from FCSAPI")
                
                return data
                
            except requests.exceptions.Timeout:
                print(f"⚠️  Request timeout on attempt {attempt + 1}. Retrying in 10 seconds...")
                time.sleep(10)
                continue
            except requests.exceptions.ConnectionError:
                print(f"⚠️  Connection error on attempt {attempt + 1}. Retrying in 10 seconds...")
                time.sleep(10)
                continue
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Network error on attempt {attempt + 1}: {str(e)}. Retrying in 10 seconds...")
                time.sleep(10)
                continue
            except json.JSONDecodeError:
                print(f"⚠️  Invalid JSON response on attempt {attempt + 1}. Retrying in 10 seconds...")
                time.sleep(10)
                continue
        
        # If we get here, all retries failed
        raise GoldPriceAPIError(f"Failed to retrieve data from FCSAPI after {max_retries} attempts. The service may be temporarily unavailable or rate limited.")
    
    def get_current_gold_price(self) -> Dict:
        """
        Get current gold price data (latest candle from FCSAPI)
        
        Returns:
            Dict containing current gold price information
        
        Raises:
            GoldPriceAPIError: If API request fails
        """
        # Get the full dataset from FCSAPI
        fcsapi_data = self._get_fcsapi_data()
        
        # Extract the latest candle (highest timestamp)
        response_data = fcsapi_data.get('response', {})
        if not response_data:
            raise GoldPriceAPIError("No data available from FCSAPI")
        
        # Find the candle with the highest timestamp
        latest_timestamp = max(response_data.keys())
        latest_candle = response_data[latest_timestamp]
        
        # Return in a format compatible with existing code
        return {
            'status': True,
            'code': 200,
            'msg': 'Successfully retrieved current price',
            'data': {
                'symbol': 'XAU/USD',
                'price': float(latest_candle['c']),
                'open': float(latest_candle['o']),
                'high': float(latest_candle['h']),
                'low': float(latest_candle['l']),
                'timestamp': int(latest_timestamp),
                'datetime': latest_candle['tm']
            }
        }
    
    def get_gold_history(self, start_date: Optional[str] = None, end_date: Optional[str] = None, 
                        group_by: str = "day", aggregation: str = "max") -> Dict:
        """
        Get gold price history data (filtered from FCSAPI 300-candle dataset)
        
        Args:
            start_date: Start date in yyyy-mm-dd format (optional)
            end_date: End date in yyyy-mm-dd format (optional)
            group_by: Time grouping - year, month, week, day (default: day) - ignored for FCSAPI
            aggregation: Price aggregation - max, min, avg (default: max) - ignored for FCSAPI
        
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
        
        # Get the full dataset from FCSAPI
        fcsapi_data = self._get_fcsapi_data()
        response_data = fcsapi_data.get('response', {})
        
        if not response_data:
            raise GoldPriceAPIError("No data available from FCSAPI")
        
        # Convert date strings to timestamps for filtering
        start_timestamp = self._date_to_timestamp(start_date)
        end_timestamp = self._date_to_timestamp(end_date) + 86400  # Add 1 day to include end date
        
        # Filter candles within the requested date range
        filtered_data = {}
        for timestamp_str, candle_data in response_data.items():
            candle_timestamp = int(timestamp_str)
            if start_timestamp <= candle_timestamp <= end_timestamp:
                filtered_data[timestamp_str] = candle_data
        
        if not filtered_data:
            # Check if the requested range is too old
            oldest_timestamp = min(response_data.keys())
            oldest_date = datetime.fromtimestamp(int(oldest_timestamp)).strftime('%Y-%m-%d')
            
            if start_timestamp < int(oldest_timestamp):
                raise GoldPriceAPIError(
                    f"Requested start date {start_date} is older than available data. "
                    f"FCSAPI only provides data from {oldest_date} (last 300 days)."
                )
            else:
                raise GoldPriceAPIError(
                    f"No data available for the requested date range {start_date} to {end_date}. "
                    f"Available data covers the last 300 days."
                )
        
        # Return in a format compatible with existing code
        return {
            'status': True,
            'code': 200,
            'msg': f'Successfully retrieved {len(filtered_data)} candles',
            'data': filtered_data,
            'info': fcsapi_data.get('info', {}),
            'date_range': {
                'start_date': start_date,
                'end_date': end_date,
                'actual_candles': len(filtered_data)
            }
        }
    
    def parse_gold_data(self, api_response: Dict) -> pd.DataFrame:
        """
        Parse FCSAPI response to pandas DataFrame for analysis
        
        Args:
            api_response: Response from FCSAPI with filtered data
        
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        
        Raises:
            GoldPriceAPIError: If data parsing fails or data is invalid
        """
        if not api_response:
            raise GoldPriceAPIError("No response received from FCSAPI.")
        
        # Handle FCSAPI response format
        if isinstance(api_response, dict):
            # Check if it's our filtered response format
            if 'data' in api_response and 'status' in api_response:
                # Extract the candle data from our filtered response
                history_data = api_response['data']
            elif 'response' in api_response and 'status' in api_response:
                # Direct FCSAPI response format
                history_data = api_response['response']
            elif 'price' in api_response and 'data' in api_response:
                # Current price format from get_current_gold_price
                current_data = api_response['data']
                price_data = [{
                    'date': pd.to_datetime(current_data['datetime']).date(),
                    'open': float(current_data['open']),
                    'high': float(current_data['high']),
                    'low': float(current_data['low']),
                    'close': float(current_data['price']),
                    'volume': 0
                }]
                history_data = price_data
            else:
                raise GoldPriceAPIError(f"Unknown FCSAPI response format: {list(api_response.keys())}")
        else:
            raise GoldPriceAPIError(f"Unknown FCSAPI response type: {type(api_response)}")
        
        if not history_data:
            raise GoldPriceAPIError("No price history data found in FCSAPI response.")
        
        # Convert timestamp-keyed data to list format
        if isinstance(history_data, dict):
            candle_list = []
            for timestamp_str, candle_data in history_data.items():
                # Parse the datetime from FCSAPI format
                datetime_str = candle_data.get('tm', '')
                if datetime_str:
                    date_obj = pd.to_datetime(datetime_str).date()
                else:
                    # Fallback: use timestamp
                    date_obj = pd.to_datetime(int(timestamp_str), unit='s').date()
                
                # Parse OHLCV data
                candle_list.append({
                    'date': date_obj,
                    'open': float(candle_data['o']),
                    'high': float(candle_data['h']),
                    'low': float(candle_data['l']),
                    'close': float(candle_data['c']),
                    'volume': float(candle_data['v']) if candle_data['v'] else 0.0
                })
        else:
            # Already in list format
            candle_list = history_data
        
        if not candle_list:
            raise GoldPriceAPIError("No valid candle data found in FCSAPI response.")
        
        # Convert to DataFrame
        df = pd.DataFrame(candle_list)
        
        # Ensure required columns exist
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                raise GoldPriceAPIError(f"Missing required column '{col}' in FCSAPI response.")
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Convert numeric columns
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for invalid data
        if (df[['open', 'high', 'low', 'close']] == 0).any().any():
            raise GoldPriceAPIError("Invalid price data detected (zero values) in FCSAPI response.")
        
        if df[['open', 'high', 'low', 'close']].isnull().any().any():
            raise GoldPriceAPIError("Missing price data (null values) in FCSAPI response.")
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        # Calculate additional metrics with real OHLCV data
        df['price_range'] = df['high'] - df['low']  # Real price range
        df['daily_change'] = df['close'].diff()
        df['daily_change_pct'] = df['daily_change'].pct_change(fill_method=None) * 100
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        df['weighted_price'] = (df['high'] + df['low'] + 2 * df['close']) / 4
        
        print(f"✅ Successfully parsed {len(df)} rows of gold data from FCSAPI")
        print(f"🎯 Using real OHLCV data with price ranges and volume")
        
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
        
        # Robust parameter conversion with debugging
        try:
            original_look_back = look_back_days
            look_back_days = int(look_back_days)
            print(f"DEBUG: Converted look_back_days from {type(original_look_back)} ({original_look_back}) to {type(look_back_days)} ({look_back_days})")
        except (ValueError, TypeError) as e:
            print(f"DEBUG: Failed to convert look_back_days '{look_back_days}' to int: {e}. Using default 30.")
            look_back_days = 30
        
        # Validate range
        if look_back_days < 1 or look_back_days > 365:
            print(f"DEBUG: look_back_days {look_back_days} out of range. Using default 30.")
            look_back_days = 30
        
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
