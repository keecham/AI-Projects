#!/usr/bin/env python3
"""
Stock Momentum Analysis Tool
Analyzes S&P 500 stocks and provides buy/sell recommendations based on momentum trends.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockMomentumAnalyzer:
    def __init__(self):
        self.sp500_tickers = self._get_sp500_tickers()
        self.data = {}
        
    def _get_sp500_tickers(self):
        """Get S&P 500 ticker symbols"""
        # Using a subset of major S&P 500 stocks for demonstration
        # In production, you'd fetch the complete list from a reliable source
        major_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK-B',
            'UNH', 'JNJ', 'V', 'PG', 'JPM', 'XOM', 'HD', 'CVX', 'MA', 'PFE',
            'ABBV', 'BAC', 'KO', 'AVGO', 'PEP', 'TMO', 'COST', 'WMT', 'DHR',
            'MRK', 'ACN', 'VZ', 'ADBE', 'TXN', 'NFLX', 'CMCSA', 'NKE', 'CRM',
            'QCOM', 'AMD', 'INTC', 'T', 'CSCO', 'ABT', 'ORCL', 'IBM', 'GE',
            'AMGN', 'PM', 'UNP', 'LOW', 'SPGI', 'INTU', 'CAT', 'AXP', 'BKNG',
            'SYK', 'GILD', 'ADP', 'ISRG', 'TJX', 'CVS', 'MDT', 'PYPL', 'NOW',
            'RTX', 'HON', 'AMT', 'LMT', 'ELV', 'TGT', 'ZTS', 'SBUX', 'CI',
            'BLK', 'SO', 'DUK', 'PLD', 'ITW', 'EOG', 'AON', 'ICE', 'SPG',
            'NOC', 'AEP', 'PWR', 'FIS', 'PSA', 'ALL', 'MMC', 'APD', 'A',
            'CL', 'EMR', 'SHW', 'ECL', 'ROP', 'AFL', 'CTAS', 'NSC', 'ETN',
            'EXC', 'CME', 'MCO', 'TEL', 'PAYX', 'ROST', 'CHTR', 'CTSH', 'PRU',
            'AEE', 'KMB', 'YUM', 'EQR', 'EXR', 'VRSK', 'MRNA', 'FTNT', 'CDNS',
            'MCHP', 'IDXX', 'FAST', 'WEC', 'ETR', 'EIX', 'XEL', 'AWK', 'SRE',
            'PEG', 'WBA', 'ES', 'D', 'ED', 'NEE', 'PCAR', 'CNP', 'EXPD',
            'FANG', 'K', 'GIS', 'KIM', 'J', 'LHX', 'MKC', 'NTRS', 'PNC',
            'RF', 'SYY', 'TROW', 'TRV', 'USB', 'VFC', 'WLTW', 'ZBH', 'AOS',
            'BIIB', 'CINF', 'CTXS', 'DOV', 'FITB', 'GLW', 'HIG', 'HUM', 'IPG',
            'JNPR', 'KEY', 'LUV', 'MKTX', 'NDAQ', 'NUE', 'O', 'PGR', 'PKI',
            'PPG', 'RMD', 'SNA', 'STT', 'SWK', 'TEL', 'TSS', 'UDR', 'VLO',
            'WY', 'XRAY', 'ZBRA', 'AAL', 'ALK', 'ALLE', 'ANSS', 'ARE', 'BEN',
            'BF-B', 'BLL', 'BR', 'CBOE', 'CHD', 'CHRW', 'CINF', 'CLX', 'CMG',
            'CNC', 'COO', 'CPRT', 'CRL', 'CSX', 'CTAS', 'CTXS', 'D', 'DG',
            'DISH', 'DLTR', 'DRE', 'DTE', 'EA', 'EBAY', 'EFX', 'EIX', 'EL',
            'EMN', 'ENPH', 'EQIX', 'EQR', 'ES', 'ETR', 'EW', 'EXC', 'EXPD',
            'EXR', 'F', 'FANG', 'FAST', 'FBHS', 'FDX', 'FE', 'FFIV', 'FIS',
            'FISV', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FTV', 'GD', 'GPN',
            'GPS', 'GRMN', 'GWW', 'HAS', 'HBAN', 'HCA', 'HES', 'HIG', 'HOLX',
            'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUM', 'HWM', 'IEX',
            'IFF', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IQV', 'IRM',
            'ISRG', 'IT', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JKHY', 'JNJ', 'JPM',
            'JWN', 'K', 'KDP', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX',
            'KO', 'KR', 'KSU', 'L', 'LB', 'LDOS', 'LEG', 'LEN', 'LH', 'LHX',
            'LIN', 'LKQ', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUV',
            'LW', 'LYB', 'M', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK',
            'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM',
            'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPC', 'MRK', 'MRNA', 'MRO',
            'MS', 'MSCI', 'MSI', 'MTB', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NEE',
            'NEM', 'NFLX', 'NI', 'NKE', 'NLOK', 'NOC', 'NOV', 'NRG', 'NSC',
            'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA', 'O',
            'ODFL', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PCAR',
            'PEG', 'PEP', 'PFE', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI',
            'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL', 'PRU', 'PSA',
            'PSX', 'PWR', 'PXD', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN',
            'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST',
            'RSG', 'RTX', 'SBAC', 'SBUX', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM',
            'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STT',
            'STX', 'STZ', 'SWK', 'SWKS', 'SYY', 'T', 'TAP', 'TDG', 'TDY',
            'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TMO', 'TMUS', 'TPG', 'TROW',
            'TRMB', 'TSN', 'TT', 'TTWO', 'TWTR', 'TXN', 'TXT', 'TYL', 'UA',
            'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS',
            'URI', 'USB', 'V', 'VFC', 'VLO', 'VMC', 'VRSK', 'VRTX', 'VTR',
            'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WEC', 'WELL', 'WFC', 'WHR',
            'WM', 'WMB', 'WMT', 'WRB', 'WY', 'WYNN', 'XEL', 'XLNX', 'XOM',
            'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS'
        ]
        return major_stocks[:100]  # Using first 100 for performance
    
    def fetch_stock_data(self, ticker, period='6mo'):
        """Fetch stock data for a given ticker"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            if data.empty:
                return None
            return data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
    
    def calculate_momentum_indicators(self, data, ticker):
        """Calculate various momentum indicators"""
        if data is None or len(data) < 20:
            return None
            
        # Price change over different periods
        price_1w = data['Close'].iloc[-5] if len(data) >= 5 else data['Close'].iloc[0]
        price_1m = data['Close'].iloc[-20] if len(data) >= 20 else data['Close'].iloc[0]
        price_3m = data['Close'].iloc[-60] if len(data) >= 60 else data['Close'].iloc[0]
        
        current_price = data['Close'].iloc[-1]
        
        # Calculate returns
        returns_1w = (current_price - price_1w) / price_1w * 100
        returns_1m = (current_price - price_1m) / price_1m * 100
        returns_3m = (current_price - price_3m) / price_3m * 100
        
        # RSI calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1] if not rsi.empty else 50
        
        # Moving averages
        sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(window=50).mean().iloc[-1] if len(data) >= 50 else sma_20
        
        # Volume trend
        avg_volume_20 = data['Volume'].rolling(window=20).mean().iloc[-1]
        recent_volume = data['Volume'].iloc[-5:].mean()
        volume_ratio = recent_volume / avg_volume_20 if avg_volume_20 > 0 else 1
        
        # Volatility (20-day rolling standard deviation)
        volatility = data['Close'].pct_change().rolling(window=20).std().iloc[-1] * 100
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'returns_1w': returns_1w,
            'returns_1m': returns_1m,
            'returns_3m': returns_3m,
            'rsi': current_rsi,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'volume_ratio': volume_ratio,
            'volatility': volatility,
            'price_vs_sma20': (current_price - sma_20) / sma_20 * 100,
            'price_vs_sma50': (current_price - sma_50) / sma_50 * 100 if sma_50 > 0 else 0
        }
    
    def calculate_momentum_score(self, indicators):
        """Calculate a composite momentum score"""
        if not indicators:
            return 0
            
        score = 0
        
        # Short-term momentum (40% weight)
        if indicators['returns_1w'] > 0:
            score += min(indicators['returns_1w'] * 2, 20)  # Cap at 20 points
        else:
            score += max(indicators['returns_1w'] * 2, -20)  # Cap at -20 points
        
        # Medium-term momentum (30% weight)
        if indicators['returns_1m'] > 0:
            score += min(indicators['returns_1m'] * 1.5, 15)
        else:
            score += max(indicators['returns_1m'] * 1.5, -15)
        
        # Long-term momentum (20% weight)
        if indicators['returns_3m'] > 0:
            score += min(indicators['returns_3m'], 10)
        else:
            score += max(indicators['returns_3m'], -10)
        
        # RSI momentum (10% weight)
        if 30 <= indicators['rsi'] <= 70:  # Not overbought/oversold
            score += 5
        elif indicators['rsi'] > 80:  # Overbought
            score -= 10
        elif indicators['rsi'] < 20:  # Oversold
            score += 10
        
        # Volume confirmation
        if indicators['volume_ratio'] > 1.2:  # Above average volume
            score += 5
        elif indicators['volume_ratio'] < 0.8:  # Below average volume
            score -= 5
        
        # Price vs moving averages
        if indicators['price_vs_sma20'] > 0:
            score += 3
        if indicators['price_vs_sma50'] > 0:
            score += 2
        
        return score
    
    def analyze_stocks(self):
        """Analyze all S&P 500 stocks and return recommendations"""
        print("Fetching stock data and calculating momentum indicators...")
        
        results = []
        
        for i, ticker in enumerate(self.sp500_tickers):
            if i % 20 == 0:
                print(f"Processing {i+1}/{len(self.sp500_tickers)} stocks...")
            
            data = self.fetch_stock_data(ticker)
            if data is not None:
                indicators = self.calculate_momentum_indicators(data, ticker)
                if indicators:
                    indicators['momentum_score'] = self.calculate_momentum_score(indicators)
                    results.append(indicators)
        
        return results
    
    def get_recommendations(self, results, top_n=5):
        """Get top buy and sell recommendations"""
        if not results:
            return [], []
        
        # Filter out stocks with extreme volatility or very low prices
        filtered_results = [
            r for r in results 
            if r['volatility'] < 50 and r['current_price'] > 5
        ]
        
        # Sort by momentum score
        sorted_results = sorted(filtered_results, key=lambda x: x['momentum_score'], reverse=True)
        
        # Top buys (highest momentum scores)
        top_buys = sorted_results[:top_n]
        
        # Top sells (lowest momentum scores)
        top_sells = sorted_results[-top_n:]
        
        return top_buys, top_sells
    
    def print_recommendations(self, top_buys, top_sells):
        """Print formatted recommendations"""
        print("\n" + "="*80)
        print("STOCK MOMENTUM ANALYSIS - RECOMMENDATIONS")
        print("="*80)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data Period: Last 6 months")
        print(f"Stocks Analyzed: {len(self.sp500_tickers)}")
        
        print("\n" + "🔥 TOP 5 BUY RECOMMENDATIONS" + "🔥")
        print("-" * 50)
        for i, stock in enumerate(top_buys, 1):
            print(f"{i}. {stock['ticker']}")
            print(f"   Price: ${stock['current_price']:.2f}")
            print(f"   Momentum Score: {stock['momentum_score']:.1f}")
            print(f"   1W Return: {stock['returns_1w']:.1f}%")
            print(f"   1M Return: {stock['returns_1m']:.1f}%")
            print(f"   3M Return: {stock['returns_3m']:.1f}%")
            print(f"   RSI: {stock['rsi']:.1f}")
            print(f"   Volume Ratio: {stock['volume_ratio']:.1f}x")
            print()
        
        print("\n" + "❌ TOP 5 SELL RECOMMENDATIONS" + "❌")
        print("-" * 50)
        for i, stock in enumerate(top_sells, 1):
            print(f"{i}. {stock['ticker']}")
            print(f"   Price: ${stock['current_price']:.2f}")
            print(f"   Momentum Score: {stock['momentum_score']:.1f}")
            print(f"   1W Return: {stock['returns_1w']:.1f}%")
            print(f"   1M Return: {stock['returns_1m']:.1f}%")
            print(f"   3M Return: {stock['returns_3m']:.1f}%")
            print(f"   RSI: {stock['rsi']:.1f}")
            print(f"   Volume Ratio: {stock['volume_ratio']:.1f}x")
            print()
        
        print("\n" + "⚠️  DISCLAIMER" + "⚠️")
        print("-" * 30)
        print("This analysis is for educational purposes only.")
        print("Past performance does not guarantee future results.")
        print("Always do your own research before making investment decisions.")
        print("Consider consulting with a financial advisor.")

def main():
    """Main function to run the stock momentum analysis"""
    print("Stock Momentum Analysis Tool")
    print("Fetching S&P 500 data and analyzing momentum trends...")
    
    analyzer = StockMomentumAnalyzer()
    results = analyzer.analyze_stocks()
    
    if not results:
        print("No data available for analysis.")
        return
    
    top_buys, top_sells = analyzer.get_recommendations(results)
    analyzer.print_recommendations(top_buys, top_sells)

if __name__ == "__main__":
    main()
