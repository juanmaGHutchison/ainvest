from alpaca_trade_api import Stream, REST
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from conf.broker.broker_config import BrokerConfig

class Alpaca_Session:
    def __init__(self):
        self.configuration = BrokerConfig.load()
        self.api_key = self.configuration.api_key
        self.api_secret = self.configuration.api_secret
        self.api_endpoint = self.configuration.api_endpoint

        self.broker_historic: StockHistoricalDataClient
        self.broker: Stream
        self.broker_trading: TradingClient
        self.broker_rest: REST

    def init_data_historic_client(self):
        self.broker_historic = StockHistoricalDataClient(self.api_key, self.api_secret)

    def init_alpaca_stream_session(self):
        self.broker = Stream(self.api_key, self.api_secret, websocket_params={"open_timeout": 50})

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
                base_url = self.api_endpoint
            )

