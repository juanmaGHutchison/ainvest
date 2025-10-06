from libs.broker.alpaca.alpaca_session import Alpaca_Session

from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderClass, TimeInForce
from alpaca.data.requests import StockLatestTradeRequest

import time

class Alpaca_Trading(Alpaca_Session):
    def __init__(self):
        super().__init__()
        # TODO: Leave default value when no Paper Account
        self.init_alpaca_trading_client(is_paper = True)
        self.init_data_historic_client()

    def _get_current_trade(self, symbol):
        request_params = StockLatestTradeRequest(symbol_or_symbols=[symbol])
        latest_trade = self.broker_historic.get_stock_latest_trade(request_params)
        
        return latest_trade[symbol].price

    def buy_sell_stock(self, symbol, investment, take_profit_price):
        current_price = self._get_current_trade(symbol)
        # TODO: put in config file
        stop_loss_price = round(current_price * 0.8, 2)
        print(f"STOP-LOSS: {stop_loss_price}")

        order_request = MarketOrderRequest(
                symbol = symbol,
                qty = investment,
                side = OrderSide.BUY,
                time_in_force = TimeInForce.DAY,
                order_class = OrderClass.BRACKET,
                take_profit = {"limit_price": round(take_profit_price, 2)},
                stop_loss = {"stop_price": round(stop_loss_price, 2)} if stop_loss_price else None
            )

        order = self.broker_trading.submit_order(order_data = order_request)
        print(f"Order performed. INvested: {investment}")

    def get_current_balance(self):
        return self.broker_trading.get_account().cash
