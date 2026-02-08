from dataclasses import dataclass
import pandas as pd
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class MarketWindow:
    ticker: str
    prices: pd.Series
    sentiment_score: Optional[float] = None
    timestamp: Optional[datetime] = None

