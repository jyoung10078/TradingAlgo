
from lumibot.strategies import Strategy

class FirstStrategy(Strategy):
    """ Class for a simple strategy that buys a stock and holds it. """

    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H" # The amount of time to sleep between trades
        self.last_trade = None
        self.cash_at_risk = cash_at_risk


    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round((cash * self.cash_at_risk) / last_price, 0)
        return cash, last_price, quantity


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()

        order = None

        if last_price < cash:
            if self.last_trade == None:
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="market"
                )

                order_status = self.submit_order(order)
                print(f"Order status: {order_status}")  # Debugging step
                self.last_trade = "buy"
