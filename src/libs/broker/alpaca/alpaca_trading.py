from libs.broker.alpaca.alpaca_session import Alpaca_Session

from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderClass, TimeInForce
from alpaca.data.requests import StockLatestTradeRequest
from alpaca.trading.requests import GetOrdersRequest
from alpaca.common.exceptions import APIError

import time
import requests

class Alpaca_Trading(Alpaca_Session):
    class TickerPriceUnknownError(Exception):
        def __init__(self, symbol, message = None):
            msg = message or f"No data price about ticker {symbol}"
            super().__init__(msg)
            self.symbol = symbol

    def __init__(self):
        super().__init__()
        # TODO: Leave default value when no Paper Account
        self.init_alpaca_trading_client(is_paper = True)
        self.init_data_historic_client()

    def buy_sell_stock(self, symbol, qty, target_price, stop_loss_price):
        order_request = MarketOrderRequest(
                symbol = symbol,
                qty = qty,
                side = OrderSide.BUY,
                time_in_force = TimeInForce.GTC,
                order_class = OrderClass.BRACKET,
                take_profit = {"limit_price": round(target_price, 2)},
                stop_loss = {"stop_price": round(stop_loss_price, 2)}
            )

        order = self.broker_trading.submit_order(order_data = order_request)
        print(f"Order performed. Invested(qty): {qty}")

    def get_current_balance(self):
        return self.broker_trading.get_account().cash

    def get_active_symbols(self):
        current_positions = self.broker_trading.get_all_positions()
        current_orders = self.broker_trading.get_orders(
                GetOrdersRequest(status='open', limit = 100)
                )

        active_positions = {pos.symbol.upper() for pos in current_positions}
        active_orders = {order.symbol.upper() for order in current_orders}
        
        return active_positions.union(active_orders)

    def get_latest_price(self, symbol):
        try:
            request_params = StockLatestTradeRequest(symbol_or_symbols=[symbol])
            latest_trade = self.broker_historic.get_stock_latest_trade(request_params)

            return latest_trade[symbol].price
        except APIError as e:
            if "invalid symbol" in str(e).lower():
                raise self.TickerPriceUnknownError(symbol, f"Invalid symbol returned by Alpaca: {symbol}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] HTTP error while fetching {symbol}: {e}")
            return None
        except KeyError:
            raise self.TickerPriceUnknownError(symbol)

