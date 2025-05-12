
from lumibot.strategies import Strategy
from alpaca_trade_api import REST
from timedelta import Timedelta
from datetime import datetime
from components.api_creds import ALPACA_CREDS

class MLTrader(Strategy):
    """ Class for a simple strategy that buys a stock and holds it. """

    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H" # The amount of time to sleep between trades
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=ALPACA_CREDS["BASE_URL"],
                        key_id=ALPACA_CREDS["API_KEY"],
                        secret_key=ALPACA_CREDS["API_SECRET"])


    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round((cash * self.cash_at_risk) / last_price, 0)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime("%Y-%m-%d"), three_days_prior.strftime("%Y-%m-%d")
    

    def get_news(self):
        end_date, start_date = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=start_date, end=end_date)

        news = [ev.__dict__ ["_raw"]["headline"] for ev in news]
        return news


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()

        order = None

        if last_price < cash:
            if self.last_trade == None:
                news = self.get_news()
                print(f"News for {self.symbol}: {news}")
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="market"
                )

                order_status = self.submit_order(order)
                self.last_trade = "buy"
