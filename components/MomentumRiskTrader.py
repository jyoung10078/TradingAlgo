from lumibot.strategies import Strategy
from alpaca_trade_api import REST, TimeFrame
from timedelta import Timedelta
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from components.api_creds import ALPACA_CREDS

class MomentumRiskTrader(Strategy):
    """ Algorithmic trading strategy using momentum indicators and risk analysis """

    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.05):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=ALPACA_CREDS["BASE_URL"],
                        key_id=ALPACA_CREDS["API_KEY"],
                        secret_key=ALPACA_CREDS["API_SECRET"])

    def position_sizing(self):
        """ Determine position size based on risk-adjusted return (Sharpe Ratio) """
        cash = self.get_portfolio_value()
        last_price = self.get_last_price(self.symbol)
        sharpe_ratio = self.get_sharpe_ratio()
        
        # Adjust position sizing based on Sharpe Ratio (higher ratio -> bigger trade size)
        risk_factor = min(max(sharpe_ratio / 2, 0.02), 0.1)  # Dynamic risk scaling
        quantity = round((cash * risk_factor) / last_price, 0)
        
        return cash, last_price, quantity
    
    
    def get_daterange(self, days=60):
        """Generate RFC3339-formatted start and end dates for Alpaca API."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        return end_date.strftime("%Y-%m-%dT%H:%M:%SZ"), start_date.strftime("%Y-%m-%dT%H:%M:%SZ")


    def get_market_data(self):
        end_date, start_date = self.get_daterange(days=60)
        historic_data = self.api.get_bars(
            self.symbol,
            TimeFrame.Day,
            start=start_date,
            end=end_date,
            adjustment='raw',
            feed='iex'
        ).df

        if historic_data.empty or len(historic_data) < 2:
            raise ValueError("Not enough market data retrieved for analysis")

        return historic_data


    def get_moving_averages(self):
        """ Compute moving average crossovers for trend analysis """
        data = self.get_market_data()
        data["SMA_50"] = data["close"].rolling(window=50).mean()
        data["SMA_200"] = data["close"].rolling(window=200).mean()
        
        return data

    def get_sharpe_ratio(self):
        """ Calculate Sharpe Ratio for risk-adjusted returns """
        data = self.get_market_data()
        daily_returns = data["close"].pct_change().dropna()
        avg_return = daily_returns.mean()
        std_dev = daily_returns.std()
        
        sharpe_ratio = avg_return / std_dev if std_dev > 0 else 0  # Avoid division by zero
        return sharpe_ratio

    def get_volatility(self):
        """ Compute market volatility using standard deviation """
        data = self.get_market_data()
        return data["close"].std()

    def get_trade_signal(self):
        """ Generate buy/sell signals based on momentum analysis """
        data = self.get_moving_averages()
        
        # Golden Cross (Bullish Signal)
        if data["SMA_50"].iloc[-1] > data["SMA_200"].iloc[-1] and self.last_trade != "buy":
            return "buy"
        
        # Death Cross (Bearish Signal)
        elif data["SMA_50"].iloc[-1] < data["SMA_200"].iloc[-1] and self.last_trade != "sell":
            return "sell"
        
        return "hold"

    def on_trading_iteration(self):
        """ Execute trades based on signals and risk optimization """
        cash, last_price, quantity = self.position_sizing()
        trade_signal = self.get_trade_signal()

        if last_price < cash:
            if trade_signal == "buy":
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(self.symbol, quantity, "buy", type="market")
                self.submit_order(order)
                self.last_trade = "buy"

            elif trade_signal == "sell":
                if self.last_trade == "buy":
                    self.sell_all()
                self.last_trade = "sell"
