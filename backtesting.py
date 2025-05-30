
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.traders import Trader
from datetime import datetime
from components.FirstStrategy import FirstStrategy
from components.MLTrader import MLTrader
from components.BBTrader import BBTrader
from components.MomentumRiskTrader import MomentumRiskTrader
from components.api_creds import ALPACA_CREDS


start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

broker = Alpaca(ALPACA_CREDS)

# Strategy Testing 1
# strategy = FirstStrategy(name='first_strategy'
#                       , broker=broker
#                       , parameters={"symbol": "SPY"
#                                     , "cash_at_risk": 0.5}
#                       )

# strategy.backtest(
#     YahooDataBacktesting
#     , backtesting_start=start_date
#     , backtesting_end=end_date
#     , parameters={"symbol": "SPY"
#                   , "cash_at_risk": 0.5}
# )

# Strategy Testing 2
# strategy2 = MLTrader(name='ml_trader_strategy'
#                       , broker=broker
#                       , parameters={"symbol": "SPY"
#                                     , "cash_at_risk": 0.25}
#                       )

# strategy2.backtest(
#     YahooDataBacktesting
#     , backtesting_start=start_date
#     , backtesting_end=end_date
#     , parameters={"symbol": "SPY"
#                   , "cash_at_risk": 0.25}
# )


# Strategy Testing 3
strategy3 = BBTrader(name='indicator_trader_strategy'
                      , broker=broker
                      , parameters={"symbol": "IVR"
                                    , "cash_at_risk": 1}
                      )

strategy3.backtest(
    YahooDataBacktesting
    , backtesting_start=start_date
    , backtesting_end=end_date
    , parameters={"symbol": "IVR"
                  , "cash_at_risk": 1}
)

# Strategy Testing 4
strategy4 = MomentumRiskTrader(name='momentum_risk_trader_strategy'
                       , broker=broker
                       , parameters={"symbol": "SPY"
                                     , "cash_at_risk": 0.5}
                       )
strategy4.backtest(
    YahooDataBacktesting
    , backtesting_start=start_date
    , backtesting_end=end_date
    , parameters={"symbol": "SPY"
                  , "cash_at_risk": 0.5}
)