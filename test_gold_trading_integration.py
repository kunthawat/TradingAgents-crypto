#!/usr/bin/env python3
"""
Comprehensive test suite for Gold Trading Integration
Tests the complete gold trading workflow from API to analysis
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.gold_utils import GoldPriceAPI, get_gold_price_data, get_gold_technical_analysis
from tradingagents.dataflows.interface import (
    get_gold_market_analysis, 
    get_gold_news_analysis, 
    get_gold_fundamentals_analysis,
    detect_asset_type,
    get_asset_data
)
from tradingagents.default_config import DEFAULT_CONFIG


class TestGoldPriceAPI(unittest.TestCase):
    """Test the Gold Price API functionality"""
    
    def setUp(self):
        self.api = GoldPriceAPI()
    
    @patch('tradingagents.dataflows.gold_utils.requests.get')
    def test_get_gold_history_success(self, mock_get):
        """Test successful gold history retrieval"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [
                {
                    "date": "2024-01-01",
                    "open": 2060.50,
                    "high": 2075.80,
                    "low": 2055.20,
                    "close": 2070.30,
                    "volume": 125000
                },
                {
                    "date": "2024-01-02",
                    "open": 2070.30,
                    "high": 2085.60,
                    "low": 2065.10,
                    "close": 2080.40,
                    "volume": 130000
                }
            ]
        }
        mock_get.return_value = mock_response
        
        result = self.api.get_gold_history()
        
        self.assertIsNotNone(result)
        self.assertIn("success", result)
        self.assertTrue(result["success"])
        self.assertEqual(len(result["data"]), 2)
    
    @patch('tradingagents.dataflows.gold_utils.requests.get')
    def test_get_gold_history_api_error(self, mock_get):
        """Test API error handling"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = Exception("Rate limit exceeded")
        mock_get.return_value = mock_response
        
        result = self.api.get_gold_history()
        self.assertIsNone(result)
    
    def test_parse_gold_data_valid(self):
        """Test parsing valid gold data"""
        raw_data = {
            "success": True,
            "data": [
                {
                    "date": "2024-01-01",
                    "open": 2060.50,
                    "high": 2075.80,
                    "low": 2055.20,
                    "close": 2070.30,
                    "volume": 125000
                }
            ]
        }
        
        df = self.api.parse_gold_data(raw_data)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertIn('date', df.columns)
        self.assertIn('close', df.columns)
        self.assertEqual(df.iloc[0]['close'], 2070.30)
    
    def test_parse_gold_data_invalid(self):
        """Test parsing invalid gold data"""
        raw_data = {"success": False, "error": "API Error"}
        
        df = self.api.parse_gold_data(raw_data)
        
        self.assertTrue(df.empty)
    
    def test_get_gold_summary(self):
        """Test gold summary statistics"""
        # Create test DataFrame
        data = {
            'date': pd.date_range('2024-01-01', periods=5),
            'close': [2070.30, 2080.40, 2075.60, 2090.20, 2085.80],
            'volume': [125000, 130000, 127000, 135000, 132000]
        }
        df = pd.DataFrame(data)
        
        summary = self.api.get_gold_summary(df)
        
        self.assertIn('current_price', summary)
        self.assertIn('price_change_pct', summary)
        self.assertIn('period_high', summary)
        self.assertIn('period_low', summary)
        self.assertEqual(summary['current_price'], 2085.80)
        self.assertEqual(summary['period_high'], 2090.20)
        self.assertEqual(summary['period_low'], 2070.30)


class TestGoldInterfaceFunctions(unittest.TestCase):
    """Test the gold interface functions"""
    
    @patch('tradingagents.dataflows.interface.GoldPriceAPI')
    def test_get_gold_market_analysis(self, mock_api_class):
        """Test gold market analysis function"""
        # Mock API instance
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        
        # Mock API response
        mock_api.get_gold_history.return_value = {
            "success": True,
            "data": [
                {
                    "date": "2024-01-01",
                    "open": 2060.50,
                    "high": 2075.80,
                    "low": 2055.20,
                    "close": 2070.30,
                    "volume": 125000
                }
            ]
        }
        
        mock_df = pd.DataFrame([{
            'date': '2024-01-01',
            'open': 2060.50,
            'high': 2075.80,
            'low': 2055.20,
            'close': 2070.30,
            'volume': 125000
        }])
        
        mock_api.parse_gold_data.return_value = mock_df
        mock_api.get_gold_summary.return_value = {
            'current_price': 2070.30,
            'price_change_pct': 0.5,
            'period_high': 2075.80,
            'period_low': 2055.20,
            'avg_volume': 125000,
            'volatility': 1.2,
            'data_points': 1,
            'date_range': {'start': '2024-01-01', 'end': '2024-01-01'}
        }
        
        result = get_gold_market_analysis("GOLD", "2024-01-01")
        
        self.assertIsInstance(result, str)
        self.assertIn("GOLD Gold Market Analysis", result)
        self.assertIn("2070.30", result)
    
    @patch('tradingagents.dataflows.interface.get_google_news')
    def test_get_gold_news_analysis(self, mock_get_news):
        """Test gold news analysis function"""
        mock_get_news.return_value = "## gold price:\n### Gold prices rise amid uncertainty\nGold prices increased today..."
        
        result = get_gold_news_analysis("GOLD", "2024-01-01", 7)
        
        self.assertIsInstance(result, str)
        self.assertIn("GOLD Gold News and Market Trends", result)
        self.assertIn("Gold Market Context", result)
    
    def test_get_gold_fundamentals_analysis(self):
        """Test gold fundamentals analysis function"""
        result = get_gold_fundamentals_analysis("GOLD", "2024-01-01")
        
        self.assertIsInstance(result, str)
        self.assertIn("GOLD Gold Fundamental Analysis", result)
        self.assertIn("Gold as an Asset Class", result)
        self.assertIn("Supply and Demand Dynamics", result)


class TestAssetTypeDetection(unittest.TestCase):
    """Test asset type detection functionality"""
    
    def test_detect_gold_symbols(self):
        """Test gold symbol detection"""
        gold_symbols = ['GOLD', 'XAU', 'XAUUSD', 'GOLD/USD', 'GC=F']
        
        for symbol in gold_symbols:
            with self.subTest(symbol=symbol):
                result = detect_asset_type(symbol)
                self.assertEqual(result, 'gold')
    
    def test_detect_crypto_symbols(self):
        """Test cryptocurrency symbol detection"""
        crypto_symbols = ['BTC', 'ETH', 'ADA', 'SOL', 'DOT', 'AVAX']
        
        for symbol in crypto_symbols:
            with self.subTest(symbol=symbol):
                result = detect_asset_type(symbol)
                self.assertEqual(result, 'crypto')
    
    def test_detect_unknown_symbols(self):
        """Test unknown symbol detection"""
        unknown_symbols = ['UNKNOWN', 'TEST123', 'FAKE_SYMBOL']
        
        for symbol in unknown_symbols:
            with self.subTest(symbol=symbol):
                result = detect_asset_type(symbol)
                self.assertEqual(result, 'unknown')
    
    def test_case_insensitive_detection(self):
        """Test case insensitive symbol detection"""
        test_cases = [
            ('gold', 'gold'),
            ('Gold', 'gold'),
            ('GOLD', 'gold'),
            ('btc', 'crypto'),
            ('Btc', 'crypto'),
            ('BTC', 'crypto')
        ]
        
        for symbol, expected in test_cases:
            with self.subTest(symbol=symbol):
                result = detect_asset_type(symbol)
                self.assertEqual(result, expected)


class TestAssetDataRetrieval(unittest.TestCase):
    """Test universal asset data retrieval"""
    
    @patch('tradingagents.dataflows.interface.get_gold_market_analysis')
    @patch('tradingagents.dataflows.interface.get_crypto_market_analysis')
    def test_get_asset_data_gold(self, mock_crypto, mock_gold):
        """Test asset data retrieval for gold"""
        mock_gold.return_value = "Gold market analysis result"
        
        result = get_asset_data("GOLD", "2024-01-01")
        
        self.assertEqual(result, "Gold market analysis result")
        mock_gold.assert_called_once_with("GOLD", "2024-01-01")
        mock_crypto.assert_not_called()
    
    @patch('tradingagents.dataflows.interface.get_gold_market_analysis')
    @patch('tradingagents.dataflows.interface.get_crypto_market_analysis')
    def test_get_asset_data_crypto(self, mock_crypto, mock_gold):
        """Test asset data retrieval for crypto"""
        mock_crypto.return_value = "Crypto market analysis result"
        
        result = get_asset_data("BTC", "2024-01-01")
        
        self.assertEqual(result, "Crypto market analysis result")
        mock_crypto.assert_called_once_with("BTC", "2024-01-01")
        mock_gold.assert_not_called()
    
    @patch('tradingagents.dataflows.interface.get_gold_market_analysis')
    @patch('tradingagents.dataflows.interface.get_crypto_market_analysis')
    def test_get_asset_data_unknown(self, mock_crypto, mock_gold):
        """Test asset data retrieval for unknown symbol"""
        result = get_asset_data("UNKNOWN", "2024-01-01")
        
        self.assertIn("Unknown asset type", result)
        mock_gold.assert_not_called()
        mock_crypto.assert_not_called()


class TestConfiguration(unittest.TestCase):
    """Test configuration settings for gold trading"""
    
    def test_gold_api_config(self):
        """Test gold API configuration"""
        self.assertIn('gold_api', DEFAULT_CONFIG)
        gold_config = DEFAULT_CONFIG['gold_api']
        
        self.assertIn('base_url', gold_config)
        self.assertIn('history_endpoint', gold_config)
        self.assertIn('current_endpoint', gold_config)
        self.assertIn('rate_limit', gold_config)
        self.assertIn('timeout', gold_config)
        
        self.assertEqual(gold_config['base_url'], 'https://gold-price-api.p.rapidapi.com/v1')
        self.assertEqual(gold_config['history_endpoint'], '/gold/history')
        self.assertEqual(gold_config['rate_limit'], 100)
        self.assertEqual(gold_config['timeout'], 30)
    
    def test_rapidapi_key_config(self):
        """Test RapidAPI key configuration"""
        self.assertIn('rapidapi_key', DEFAULT_CONFIG)


class TestIntegrationWorkflow(unittest.TestCase):
    """Test complete integration workflow"""
    
    @patch.dict(os.environ, {'RAPIDAPI_KEY': 'test_key'})
    @patch('tradingagents.dataflows.interface.GoldPriceAPI')
    def test_complete_gold_workflow(self, mock_api_class):
        """Test complete gold trading workflow"""
        # Mock API instance and responses
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        
        mock_api.get_gold_history.return_value = {
            "success": True,
            "data": [
                {
                    "date": "2024-01-01",
                    "open": 2060.50,
                    "high": 2075.80,
                    "low": 2055.20,
                    "close": 2070.30,
                    "volume": 125000
                }
            ]
        }
        
        mock_df = pd.DataFrame([{
            'date': '2024-01-01',
            'open': 2060.50,
            'high': 2075.80,
            'low': 2055.20,
            'close': 2070.30,
            'volume': 125000
        }])
        
        mock_api.parse_gold_data.return_value = mock_df
        mock_api.get_gold_summary.return_value = {
            'current_price': 2070.30,
            'price_change_pct': 0.5,
            'period_high': 2075.80,
            'period_low': 2055.20,
            'avg_volume': 125000,
            'volatility': 1.2,
            'data_points': 1,
            'date_range': {'start': '2024-01-01', 'end': '2024-01-01'}
        }
        
        # Test asset type detection
        asset_type = detect_asset_type("GOLD")
        self.assertEqual(asset_type, 'gold')
        
        # Test market analysis
        market_analysis = get_gold_market_analysis("GOLD", "2024-01-01")
        self.assertIsInstance(market_analysis, str)
        self.assertIn("GOLD Gold Market Analysis", market_analysis)
        
        # Test news analysis
        with patch('tradingagents.dataflows.interface.get_google_news') as mock_news:
            mock_news.return_value = "Gold market news..."
            news_analysis = get_gold_news_analysis("GOLD", "2024-01-01")
            self.assertIsInstance(news_analysis, str)
            self.assertIn("Gold News and Market Trends", news_analysis)
        
        # Test fundamentals analysis
        fundamentals_analysis = get_gold_fundamentals_analysis("GOLD", "2024-01-01")
        self.assertIsInstance(fundamentals_analysis, str)
        self.assertIn("Gold Fundamental Analysis", fundamentals_analysis)
        
        # Test universal asset data retrieval
        asset_data = get_asset_data("GOLD", "2024-01-01")
        self.assertIsInstance(asset_data, str)
        self.assertIn("Gold Market Analysis", asset_data)


def run_comprehensive_tests():
    """Run all gold trading integration tests"""
    print("🧪 Running Gold Trading Integration Tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestGoldPriceAPI,
        TestGoldInterfaceFunctions,
        TestAssetTypeDetection,
        TestAssetDataRetrieval,
        TestConfiguration,
        TestIntegrationWorkflow
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed! Gold trading integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
