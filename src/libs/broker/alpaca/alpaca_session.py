from alpaca_trade_api import Stream, REST
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient

from dotenv import load_dotenv
from pathlib import Path
import os

class Alpaca_Session:
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/alpaca.env"
        load_dotenv(dotenv_path.resolve())
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")

        self.broker_historic: StockHistoricalDataClient
        self.broker: Stream
        self.broker_trading: TradingClient
        self.broker_rest: REST

    def init_data_historic_client(self):
        self.broker_historic = StockHistoricalDataClient(self.api_key, self.api_secret)

    def init_alpaca_stream_session(self):
        self.broker = Stream(self.api_key, self.api_secret)

    def init_alpaca_trading_client(self, is_paper = False):
        self.broker_trading = TradingClient(
                api_key = self.api_key,
                secret_key = self.api_secret,
                paper = is_paper
            )

    def init_alpaca_trading_rest(self):
        self.broker_rest = REST(
                self.api_key,
                self.api_secret,
                base_url = "https://paper-api.alpaca.markets"
            )

