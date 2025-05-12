
from lumibot.strategies import Strategy

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