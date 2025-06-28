from libs.broker.alpaca.alpaca_session import Alpaca_Session

from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

class Alpaca_Trading(Alpaca_Session):
    def __init__(self):
        super().__init__()
        # TODO: Leave default value when no Paper Account
        self.init_alpaca_trading_client(is_paper = True)

    def buy_stock(self, in_symbol, in_notional, in_limit_price):
        sell_order = LimitOrderRequest(
                symbol = in_symbol,
                notional = in_notional,
                side = OrderSide.BUY,
                limit_price = in_limit_price,
                time_in_force = TimeInForce.GTC
            )

        self.broker_trading.submit_order(order_data = sell_order) 
