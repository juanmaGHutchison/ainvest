#!/usr/bin/env python3

import yfinance as yf
import pandas as pd

class Yahoo_Historic_Data:
    def __init__(self):
        super().__init__()

    def fetch_historic_prices_from(self, n_days_ago, in_ticker):
        n_days_str = str(n_days_ago) + "d"
        ticker = yf.Ticker(in_ticker)
        historic_data = ticker.history(period = n_days_str)
        
        return pd.Series(historic_data['Close'])

