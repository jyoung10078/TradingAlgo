from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest

# Connect using your real or paper API keys
trading_client = TradingClient("YOUR_API_KEY", "YOUR_SECRET_KEY", paper=True)

# Get account info
account = trading_client.get_account()

# Print account status
if account.trading_blocked:
    print("Account is currently restricted from trading.")

print(f"${account.buying_power} is available as buying power.")
