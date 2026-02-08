from conf.maths.maths_config import MathsConfig

from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

import json
import joblib
import pandas as pd

class BaseTrainer(ABC):
    """
    Base class for all model trainers.
    Handles:
    - data loading
    - windowing
    - splitting
    - artifact persistence

    Strategy-specific logic must be implemented by subclasses.
    """

    def __init__(
        self,
        tickers: list[str],
        lookback: int,
        horizon: int,
        output_dir: str,
        prices_dict: dict[str, pd.Series],
        test_ratio: float = 0.2,
        val_ratio: float = 0.1,
        random_seed: int = 42,
    ):
        self.configuration = MathsConfig.load()
        self.tickers = tickers
        self.lookback = lookback
        self.horizon = horizon
        self.test_ratio = test_ratio
        self.val_ratio = val_ratio
        self.random_seed = random_seed
        self.prices_dict = prices_dict

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.metadata = {
            "created_at": datetime.utcnow().isoformat(),
            "tickers": tickers,
            "lookback": lookback,
            "horizon": horizon,
            "trainer": self.__class__.__name__,
        }

    # ---------------------------
    # Public entry point
    # ---------------------------
    def run(self):
        X, y = self._build_global_dataset()
        splits = self._split_dataset(X, y)

        model, artifacts = self._train(splits)
        self._persist(model, artifacts)

        self._persist_metadata(splits)

    # ---------------------------
    # Shared logic
    # ---------------------------
    def _build_global_dataset(self):
        X_all, y_all = [], []

        for ticker in self.tickers:
            prices = self.prices_dict.get(ticker)

            if prices is None or prices.empty:
                continue

            if len(prices) < self.lookback + self.horizon:
                print(f"------ DEBUG: Not enough prices. Skipping {ticker}")
                continue

            print(f"--DEBUG: 'ticker'-{ticker}, 'prices'-{prices}") 
            print(f"--DEBUG: 'lookback'-{self.lookback}, 'len(prices)'-{len(prices)}, 'horizon'-{self.horizon}")

            for i in range(self.lookback, len(prices) - self.horizon):
                window = prices.iloc[i - self.lookback : i]

                features, target = self.build_sample(ticker, window, prices, i)

                if features is None or target is None:
                    continue

                X_all.append(features)
                y_all.append(target)

        return pd.DataFrame(X_all), pd.Series(y_all)

    def _split_dataset(self, X, y):
        n = len(X)
        test_size = int(n * self.test_ratio)
        val_size = int(n * self.val_ratio)

        train_end = n - test_size - val_size
        val_end = n - test_size

        return {
            "X_train": X.iloc[:train_end],
            "y_train": y.iloc[:train_end],
            "X_val": X.iloc[train_end:val_end],
            "y_val": y.iloc[train_end:val_end],
            "X_test": X.iloc[val_end:],
            "y_test": y.iloc[val_end:],
        }

    def _persist(self, model, artifacts: dict):
        model_path = self.output_dir / "model.pkl"
        model.save(model_path) if hasattr(model, "save") else None

        for name, obj in artifacts.items():
            path = self.output_dir / f"{name}.pkl"
            joblib.dump(obj, path)

    def _persist_metadata(self, splits):
        self.metadata.update({
            "samples": {
                "train": len(splits["X_train"]),
                "val": len(splits["X_val"]),
                "test": len(splits["X_test"]),
            }
        })

        with open(self.output_dir / "training_meta.json", "w") as f:
            json.dump(self.metadata, f, indent=2)

    @abstractmethod
    def build_sample(
        self,
        ticker: str,
        window: pd.Series,
        full_series: pd.Series,
        index: int,
    ):
        """
        Returns:
          features: dict or pd.Series
          target: float
        """
        pass

    @abstractmethod
    def _train(self, splits: dict):
        """
        Must return:
          model
          artifacts: dict (scalers, schemas, etc.)
        """
        pass
