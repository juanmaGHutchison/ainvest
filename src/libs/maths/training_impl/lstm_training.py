from libs.maths.base_trainer import BaseTrainer

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Input

import joblib

class LSTM_Training(BaseTrainer):

    def __init__(self, tickers, lookback, horizon, output_dir, prices_dict, logger_service_type):
        super().__init__(
            tickers=tickers,
            lookback=lookback,
            horizon=horizon,
            output_dir=output_dir,
            prices_dict=prices_dict
        )

        self.scaler = MinMaxScaler()

    # ❌ no usado
    def build_sample(self, *args, **kwargs):
        raise NotImplementedError("LSTM uses sequence builder")

    # --------------------------------------------------
    # 🔥 DATASET
    # --------------------------------------------------
    def _build_sequences_dataset(self):
        X_all, y_all = [], []

        for ticker in self.tickers:
            prices = self.prices_dict.get(ticker)

            if prices is None or prices.empty:
                continue

            if len(prices) < self.lookback + self.horizon + 1:
                continue

            # 🔥 convertir a numpy
            prices = prices.values

            # 🔥 RETURNS (input base)
            returns = np.log(prices[1:] / prices[:-1])

            for i in range(self.lookback, len(returns) - self.horizon):

                # 🔹 ventana de entrada (returns)
                window = returns[i - self.lookback:i]

                # 🔥 TARGET = FUTURE RETURN
                target = np.log(prices[i + self.horizon] / prices[i])

                X_all.append(window.reshape(-1, 1))
                y_all.append(target)

        # 🔹 convertir a arrays
        X_all = np.array(X_all)
        y_all = np.array(y_all)

        # 🚨 limpiar NaNs e infs
        mask = (
            np.isfinite(X_all).all(axis=(1, 2)) &
            np.isfinite(y_all)
        )

        X_all = X_all[mask]
        y_all = y_all[mask]

        # 🔹 limitar tamaño (evita overkill)
        MAX_SAMPLES = 200_000
        if len(X_all) > MAX_SAMPLES:
            X_all = X_all[-MAX_SAMPLES:]
            y_all = y_all[-MAX_SAMPLES:]

        return X_all, y_all

    # --------------------------------------------------
    def _split_dataset(self, X, y):
        n = len(X)

        test_size = int(n * self.test_ratio)
        val_size = int(n * self.val_ratio)

        train_end = n - test_size - val_size
        val_end = n - test_size

        return {
            "X_train": X[:train_end],
            "y_train": y[:train_end],
            "X_val": X[train_end:val_end],
            "y_val": y[train_end:val_end],
            "X_test": X[val_end:],
            "y_test": y[val_end:],
        }

    # --------------------------------------------------
    # 🔥 TRAIN
    # --------------------------------------------------
    def _train(self, splits):

        model = Sequential([
            Input(shape=(self.lookback, 1)),
            LSTM(64, return_sequences=True),
            Dropout(0.2),
            LSTM(32),
            Dropout(0.2),
            Dense(1)
        ])

        model.compile(
            optimizer="adam",
            loss="mse"
        )

        model.fit(
            splits["X_train"],
            splits["y_train"],
            validation_data=(splits["X_val"], splits["y_val"]),
            epochs=10,
            batch_size=32,
            verbose=1
        )

        return model, {
            "scaler": self.scaler
        }

    def _persist(self, model, artifacts: dict):
        # ✅ guardar modelo correctamente (Keras 3)
        model.save(self.output_dir / "model.keras")

        # resto igual
        for name, obj in artifacts.items():
            joblib.dump(obj, self.output_dir / f"{name}.pkl")

    # --------------------------------------------------
    # 🔥 RUN
    # --------------------------------------------------
    def run(self):
        X, y = self._build_sequences_dataset()

        splits = self._split_dataset(X, y)

        model, artifacts = self._train(splits)

        self._persist(model, artifacts)
        self._persist_metadata(splits)

