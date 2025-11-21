from libs.broker.broker_interface import Broker_Interface

from libs.broker.alpaca.alpaca_news import Alpaca_News
from libs.broker.yahoo_finance.yahoo_finance_historic_data import Yahoo_Historic_Data
from libs.broker.alpaca.alpaca_trading import Alpaca_Trading

from conf.broker.broker_config import BrokerConfig

from math import floor
from textwrap import dedent
import requests

class Broker_Facade(Broker_Interface):

    def __init__(self):
        self.configuration = BrokerConfig.load()
        self.invest_threshold = self.configuration.max_invest
        self.blacklist = self.configuration.blacklist

        self.broker_news: Alpaca_News
        self.broker_historic: Yahoo_Historic_Data
        self.broker_trading: Alpaca_Trading

    def init_news_api(self):
        self.broker_news = Alpaca_News()

    def init_historic_api(self):
        self.broker_historic = Yahoo_Historic_Data()

    def init_trading_api(self):
        self.broker_trading = Alpaca_Trading()

    def fetch_news(self, stock, handler_function):
        self.broker_news.fetch_news(stock, handler_function)

    def get_data_from_stock(self, stock):
        return self.broker_historic.fetch_historic_prices_from(
                self.configuration.historic_lookback_days, stock
            )

    def buy_stock(self, symbol, latest_value, target_price):
        gap_of_goodness = (target_price - latest_value) / latest_value
        investment = self.configuration.base_investment * (1 + gap_of_goodness)
        balance = float(self.broker_trading.get_current_balance())

        qty = max(floor(investment/latest_value), 1) 
        stop_loss_price = latest_value * (1 - self.configuration.stop_loss_percentage / 100)
        total_cost = qty * latest_value

        has_cash = balance >= total_cost
        worthwhile_operation = qty >= 1

        if has_cash and worthwhile_operation:
            print(dedent(f"""\
            [INFO] Ticker {symbol} invest operation data:
            \t- Current price: {latest_value}
            \t- Invested amount: {total_cost}
            \t- Stop loss price: {stop_loss_price}
            \t- Target price: {target_price}
            \t- Shares to buy(qty): {qty}
            -----------------------------------------------------"""))

            self.broker_trading.buy_sell_stock(symbol, qty, target_price, stop_loss_price)
        else:
            # TODO: Use log files
            if not has_cash:
                print (f"[WARNING]  Account balance is {balance} and investment requires {total_cost}€. Ignoring operation")
            if not worthwhile_operation:
                print (f"[WARNING] QTY to sell will be less than 1. This operation is worthless")

    def is_blacklisted(self, symbols):
        if isinstance(symbols, str):
            symbols = [symbols]
        elif not symbols:
            symbols = []

        return any(symbol in self.blacklist for symbol in symbols)

    def is_already_open(self, symbols):
        try:
            active_symbols = self.broker_trading.get_active_symbols()
        except requests.exceptions.ConnectionError as e:
            print(f"[ERROR] Network error while fetching active symbol(s) {symbols}: {e}")
            return false

        if isinstance(symbols, str):
            symbols = [symbols]
        elif not symbols:
            symbols = []

        return any(sym in active_symbols for sym in symbols)

    def is_under_threshold_invest(self, symbols):
        omit_operation = False

        try:
            for symbol in symbols:
                latest_symbol_price = self.broker_trading.get_latest_price(symbol)
                omit_operation = latest_symbol_price > self.invest_threshold
                if (omit_operation):
                    print(f"[DEBUG] {symbol} price {latest_symbol_price} is greater than configured invest threshold {self.invest_threshold}")
                    break

            return omit_operation
        except Alpaca_Trading.TickerPriceUnknownError as e:
            print(f"[WARN] {e}. Cowardly ommitting operation")
            return False

