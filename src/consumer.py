#!/usr/bin/env python3

from libs.broker.broker_facade import Broker_Facade
from libs.queue.queue_adapter import Queue_Adapter
from libs.maths.lstm_strategy import LSTM_Strategy
from libs.log_manager.logger_factory import LoggerFactory

class Consumer:
    def __init__(self):
        logger_service_type = self.__class__.__name__
        self.log = LoggerFactory(logger_service_type)
        self.log.init_logger(self.log.consumer)
        
        self.broker = Broker_Facade(logger_service_type)
        self.queue_consumer = Queue_Adapter(logger_service_type)
        self.lstm = LSTM_Strategy(logger_service_type)

        self.broker.init_historic_api()
        self.broker.init_trading_api()
        self.queue_consumer.init_consumer()

    def consuming_handler(self, message):
        t = message.get('ticker')
        tickers = [t] if isinstance(t, str) else (t or [])

        for ticker in tickers:
            prices = self.broker.get_data_from_stock(ticker)
            if prices.empty:
                self.log.warning(f"no price data available. Skipping.", ticker)
                continue

            self.broker.buy_stock(
                    ticker,
                    float(prices.iloc[-1]),
                    self.lstm.predict(prices)
                    )

    def start_consumer(self):
        self.queue_consumer.start_consuming(self.consuming_handler)

if __name__ == "__main__":
    consumer = Consumer()

    consumer.start_consumer()
