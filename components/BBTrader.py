
from lumibot.strategies import Strategy
from alpaca_trade_api import REST
from timedelta import Timedelta
from datetime import datetime
from components.api_creds import ALPACA_CREDS
from components.finbert_utils import estimate_sentiment

class BBTrader(Strategy):
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
        cash = self.get_portfolio_value()
        last_price = self.get_last_price(self.symbol)
        quantity = round((cash * self.cash_at_risk) / last_price, 0)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime("%Y-%m-%d"), three_days_prior.strftime("%Y-%m-%d")
    

    def get_sentiment(self):
        end_date, start_date = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=start_date, end=end_date)

        news = [ev.__dict__ ["_raw"]["headline"] for ev in news]

        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if last_price < cash:
            if sentiment == "positive" and probability > 0.9:
                if self.last_trade == "sell":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="market"
                )

                order_status = self.submit_order(order)
                self.last_trade = "buy"

            elif sentiment == "negative" and probability > 0.9:
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="market"
                )

                order_status = self.submit_order(order)
                self.last_trade = "sell"
