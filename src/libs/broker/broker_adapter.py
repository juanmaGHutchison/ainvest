 
from libs.broker.broker_interface import Broker_Interface

from libs.broker.alpaca.alpaca_news import Alpaca_News
from libs.broker.alpaca.alpaca_historic_data import Alpaca_Historic_Data

from dotenv import load_dotenv
from pathlib import Path
import os

class Broker_Adapter(Broker_Interface):
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/alpaca.env"
        load_dotenv(dotenv_path.resolve())
        self.API_KEY = os.getenv("API_KEY")
        self.API_SECRET = os.getenv("API_SECRET")

        self.broker_news: Alpaca_News
        self.broker_historic: Alpaca_Historic_Data

    def init_news_api(self):
        self.broker_news = Alpaca_News(self.API_KEY, self.API_SECRET)

    def init_historic_api(self):
        self.broker_historic = Alpaca_Historic_Data(self.API_KEY, self.API_SECRET)

    def fetch_news(self, stock, what_to_do_func):
        self.broker.subscribe_news(what_to_do_func, stock)
        self.broker.run()

    def get_data_from_stock(self, stock):
        # TODO: 120 days
        n_days_ago = 2
        list_of_trades = self.broker_historic.fetch_historic_from(n_days_ago, stock)
        return self.broker_historic.get_prices_from_historic(list_of_trades)
