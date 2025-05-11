
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime


from dotenv import load_dotenv
import os

load_dotenv()  # Automatically looks for a .env file in the current directory

api_key = os.getenv("training_api_key")
api_secret = os.getenv("training_api_secret")
BASE_URL = 'https://paper-api.alpaca.markets' 


class AlpacaCreds:
    def __init__(self, api_key, api_secret, base_url, paper):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.BASE_URL = base_url
        self.Paper = paper


ALPACA_CREDS = AlpacaCreds(api_key, api_secret, BASE_URL, True)

class FirstStrategy(Strategy):
    def initialize(self, symbol:str="SPY"):
        self.symbol = symbol
        self.sleeptime = "24H" # The amount of time to sleep between trades
        self.last_trade = None

    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
            )

            self.submit_order(order)
            self.last_trade = "buy"

start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 10, 1)

broker = Alpaca(ALPACA_CREDS)
strategy = FirstStrategy(name='first_strategy'
                      , broker=broker
                      , parameters={"symbol": "SPY"})

strategy.backtest(
    YahooDataBacktesting
    , start_date=start_date
    , end_date=end_date
    , parameters={"symbol": "SPY"}
)

