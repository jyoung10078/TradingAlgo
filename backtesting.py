
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.traders import Trader
from datetime import datetime
from components.FirstStrategy import FirstStrategy
from components.api_creds import ALPACA_CREDS


start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

broker = Alpaca(ALPACA_CREDS)
strategy = FirstStrategy(name='first_strategy'
                      , broker=broker
                      , parameters={"symbol": "SPY"}
                      , cash_at_risk=0.5)

strategy.backtest(
    YahooDataBacktesting
    , backtesting_start=start_date
    , backtesting_end=end_date
    , parameters={"symbol": "SPY"
                  , "cash_at_risk": 0.5}
)

