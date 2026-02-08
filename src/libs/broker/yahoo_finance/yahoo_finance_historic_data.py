#!/usr/bin/env python3

import yfinance as yf
import pandas as pd

class Yahoo_Historic_Data:
    def __init__(self):
        super().__init__()

    def fetch_historic_prices_from(self, n_days_ago, in_ticker):
        # TODO: include the omit filter (function to omit or not a ticker)
        try:
            n_days_str = str(n_days_ago) + "d"
            ticker = yf.Ticker(in_ticker)
            historic_data = ticker.history(period = n_days_str)
            print(f"-------------- HISTORIC DATA OF {in_ticker}: {historic_data}")

            if historic_data.empty:
                print(f"------------- HISTORIC DATA EMPTY: {in_ticker}")
                return None

            series = historic_data["Close"].copy()
            series.index = pd.to_datetime(series.index).tz_localize(None)
            series.name = in_ticker

            return series.sort_index()
        except Exception as e:
            # TODO: filter with log library
            print(f"TODO: catch with LOG library. [Yahoo] Failed for {in_ticker}: {e}")
            return None
        
