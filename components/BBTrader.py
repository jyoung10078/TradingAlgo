
from lumibot.strategies import Strategy
from alpaca_trade_api import REST, TimeFrame
from timedelta import Timedelta
from datetime import datetime
from components.api_creds import ALPACA_CREDS
import alpaca_trade_api as tradeapi
import pandas as pd

class BBTrader(Strategy):
    """ Class for an indicator-centric trading strategy """

    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.05):
        self.symbol = symbol
        self.sleeptime = "24H" # The amount of time to sleep between trades
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=ALPACA_CREDS["BASE_URL"],
                        key_id=ALPACA_CREDS["API_KEY"],
                        secret_key=ALPACA_CREDS["API_SECRET"])


    def position_sizing(self):
        cash = self.get_portfolio_value()
        last_price = self.get_last_price(self.symbol)
        quantity = round((cash * self.cash_at_risk) / last_price, 0)
        return cash, last_price, quantity
    
    
    def get_BB_daterange(self):
        today = self.get_datetime()
        twenty_days_prior = today - Timedelta(days=20)
        return today.strftime("%Y-%m-%d"), twenty_days_prior.strftime("%Y-%m-%d")
    

    def get_closing_prices(self):
        end_date, start_date = self.get_BB_daterange()

        historic_data = self.api.get_bars(self.symbol, TimeFrame.Day, start_date, end_date, adjustment='raw').df

        # Extract closing prices
        closing_prices = historic_data['close']
        
        return closing_prices
    

    def get_BB_buy_signal(self):
        closing_prices = self.get_closing_prices()

        # Calculate the Bollinger Bands
        rolling_mean = closing_prices.mean()
        rolling_std = closing_prices.std()

        upper_band = rolling_mean + (rolling_std * 2)
        lower_band = rolling_mean - (rolling_std * 2)

        # Using bands to calculate the buy signal

        # Upward pressure for mean reversion
        if ((closing_prices.iloc[-1] >= lower_band) & (closing_prices.iloc[-2] < lower_band) & (self.last_trade == "sell" or self.last_trade == None)):
            return 'buy'
        # Price breaking upper band and will experience downard pressure eventually
        elif ((closing_prices.iloc[-1] < upper_band) & (closing_prices.iloc[-2] >= upper_band) & (self.last_trade == "buy" or self.last_trade == None)):
            return 'sell'
        else:
            return 'hold' 


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        BB_buy_signal = self.get_BB_buy_signal()

        if last_price < cash:
            if BB_buy_signal == 'buy':
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="market"
                )

                order_status = self.submit_order(order)
                self.last_trade = "buy"

            elif BB_buy_signal == 'sell':
                if self.last_trade == "buy":
                    self.sell_all()

                self.last_trade = "sell"
