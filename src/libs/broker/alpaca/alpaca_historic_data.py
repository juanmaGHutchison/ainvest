#!/usr/bin/env python3

from alpaca.data import StockHistoricalDataClient, StockTradesRequest

from datetime import datetime, timedelta

import pandas as pd

class Alpaca_Historic_Data:
    def __init__(self, api_key, api_secret):
        self.broker_historic = StockHistoricalDataClient(api_key, api_secret)

    def fetch_historic_from(self, n_days_ago, ticker):
        yesterday = datetime.today() - timedelta(days=1)

        # TODO: paralelize in windows of X days
        # start = yesterday - timedelta(days=120),
        self.historic_data_params = StockTradesRequest(
                symbol_or_symbols = ticker,
                start = yesterday - timedelta(days=4),
                end = yesterday
                )

        trades = self.broker_historic.get_stock_trades(self.historic_data_params)
        return trades[ticker]

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


