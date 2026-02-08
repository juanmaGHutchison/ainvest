from conf.maths.maths_config import MathsConfig, Strategies_enum

from libs.maths.predict_impl.lstm_strategy import LSTM_Strategy
from libs.maths.predict_impl.hybrid_ensemble_strategy import HybridEnsembleStrategy

from libs.maths.training_impl.lstm_training import LSTM_Training
from libs.maths.training_impl.hybrid_ensemble_training import HybridEnsembleTraining

import os

class Predict_factory:
    @classmethod
    def init_strategy(cls, logger_service_type):
        configuration = MathsConfig.load()
        strategy_str = configuration.strategy_used
        strategy = None

        if strategy_str == Strategies_enum.LSTM:
            strategy = LSTM_Strategy(logger_service_type)
        elif strategy_str == Strategies_enum.HLSTM:
            strategy = HybridEnsembleStrategy(logger_service_type)

        return strategy

class Training_factory:
    @classmethod
    def init_training(cls, tickers, prices_dict, logger_service_type):
        configuration = MathsConfig.load()
        strategy_str = configuration.strategy_used
        strategy = None
        
        output_dir = os.path.join(
                os.getenv("AINVEST_PERSISTENT_DIR", ""),
                configuration.training_strategy_dir)
        os.makedirs(output_dir, exist_ok=True)

        lookback = configuration.window_size_days
        horizon = configuration.window_size_horizon

        if strategy_str == Strategies_enum.LSTM:
            # TODO: tickers maybe not needed
            strategy = LSTM_Training(tickers = tickers,
                                     lookback = lookback,
                                     horizon = horizon,
                                     output_dir = output_dir,
                                     prices_dict = prices_dict,
                                     logger_service_type = logger_service_type)

        elif strategy_str == Strategies_enum.HLSTM:
            strategy = HybridEnsembleTraining(tickers = tickers,
                                              lookback = lookback,
                                              horizon = horizon,
                                              output_dir = output_dir,
                                              prices_dict = prices_dict,
                                              logger_service_type = logger_service_type)

        return strategy

