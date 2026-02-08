from libs.maths.maths_factory import Training_factory
from libs.broker.broker_facade import Broker_Facade

import pandas as pd

class Train_AI:
    def __init__(self):
        logger_service_type = self.__class__.__name__

        self.broker_trading = Broker_Facade(logger_service_type)
        self.broker_trading.init_historic_api()
        self.broker_trading.init_trading_api()

        tickers = self.broker_trading.get_all_tickers()
        # TODO: the prices dict should not be here
        prices_dict = {}
        for ticker in tickers:
            data = self.broker_trading.get_data_from_stock(
                    ticker, lambda t: "/" in t or "$" in t)
            if data is None or data.empty:
                continue
            series = data
            series.index = pd.to_datetime(series.index)
            series.name = ticker

            prices_dict[ticker] = series
        self.training_model = Training_factory.init_training(
                tickers, prices_dict, logger_service_type)

    def run_training(self):
        self.training_model.run()

if __name__ == "__main__":
    ai_training = Train_AI()
    ai_training.run_training()
