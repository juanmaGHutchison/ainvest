from libs.maths.market_window import MarketWindow

import pandas as pd
import numpy as np

from typing import Optional

class HybridFeatureBuilder:

    @staticmethod
    def build(window: MarketWindow) -> Optional[pd.DataFrame]:
        prices = window.prices

        if prices.empty:
            return None

        returns = np.log(prices / prices.shift(1)).dropna()
        if len(returns) < 10:
            return None

        features = {
            "mean_return": returns[-10:].mean(),
            "volatility": returns[-10:].std(),
            "ma_slope": prices[-5:].mean() - prices[-10:].mean(),
            "sentiment": window.sentiment_score or 0.0,
            "downside_vol": returns[returns < 0].std() or 0.0,
            "max_drawdown_10": (prices[-10:] / prices[-10:].cummax() - 1).min()
        }

        return pd.DataFrame([features])

