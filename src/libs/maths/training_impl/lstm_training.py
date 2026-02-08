from libs.maths.base_trainer import BaseTrainer

class LSTM_Training(BaseTrainer):
    def __init__(self, tickers, lookback, horizon, output_dir, prices_dict, logger_service_type):
        # TODO: logging system
        super().__init__(tickers = tickers,
                         lookback = lookback,
                         horizon = horizon,
                         output_dir = output_dir,
                         prices_dict = prices_dict
                         )

    def build_sample(self, ticker, window, full_series, index):
        raise NotImplementedError("LSTM uses sequence builder")

    def _train(self, splits):
        X_seq, y_seq = build_sequences(...)
        model = build_lstm()
        model.fit(X_seq, y_seq)
        return model, {"scaler": scaler}
