#!/usr/bin/env python3

from libs.broker.alpaca.alpaca_session import Alpaca_Session
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest

from datetime import datetime, timedelta

import pandas as pd

class Alpaca_Historic_Data(Alpaca_Session):
    def __init__(self):
        super().__init__()
        self.init_data_historic_client()

    def fetch_historic_from(self, n_days_ago, ticker):
        yesterday = datetime.today() - timedelta(days=1)
        start = yesterday - timedelta(days = n_days_ago)
        end = yesterday

        request = StockBarsRequest(
                    symbol_or_symbols = ticker,
                    timeframe = TimeFrame.Day,
                    start = start,
                    end = end
                )

        bars = self.brocker_historic.get_stock_bars(request)

        if ticker not in bars or bars[ticker].empty:
            return None

        df = bars[ticker]

        series = df["close"].copy()
        series.index = pd.to_datetime(df.index)
        series.name = ticker

        return series.sort_index()

    def get_prices_from_historic(self, list_of_trades):
        dataframe = pd.DataFrame ([{
            'timestamp': list_of_trades[i].timestamp,
            'price': list_of_trades[i].price,
            'size': list_of_trades[i].size
            } for i in range (len(list_of_trades))
        ])

        dataframe.set_index('timestamp', inplace = True)
        dataframe.sort_index(inplace = True)

        return dataframe['price']

