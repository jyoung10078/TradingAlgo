
from dotenv import load_dotenv
import os

load_dotenv()  # Automatically looks for a .env file in the current directory

api_key = os.getenv("training_api_key")
api_secret = os.getenv("training_api_secret")
BASE_URL = 'https://paper-api.alpaca.markets' 


ALPACA_CREDS = {
    "API_KEY": api_key,
    "API_SECRET": api_secret,
    "BASE_URL": BASE_URL,
    "PAPER": True
}