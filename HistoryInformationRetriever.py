from pandas import Series, Timestamp
from typing import Tuple
from pandas import DataFrame

import numpy as np

from util import get_ticker


class HistoryInformationRetriever:
    _history_df: DataFrame
    _ticker_code: str

    def __init__(
        self,
        ticker_code: str,
        history_df: DataFrame = None,
        **history_kwargs
    ) -> None:
        self._ticker_code = ticker_code.upper()
        if history_df is None:
            ticker = get_ticker(ticker_code) 
            self._history_df = ticker.history(**history_kwargs).reset_index()
            self._history_df.rename(columns={self._history_df.columns[0]: 'Date'}, inplace=True)
        else:
            self._history_df = history_df

    def get_ticker_code(
        self
    ) -> str:
        return self._ticker_code

    def get_values_over_time(
        self
    ) -> Series:
        return self._history_df.set_index('Date')['Close']
    
    def get_history_df(
        self
    ) -> DataFrame:
        return self._history_df

    def get_normalized_values_over_time(
        self
    ) -> Series:
        return self._history_df.set_index('Date')['Close'] / self._history_df['Close'].iloc[0]

    def get_dividends_over_time(
        self,
    ) -> float:
        return self._history_df.set_index('Date')['Dividends']

    def get_total_dividends(
        self,
    ) -> float:
        return self._history_df['Dividends'].sum()

    def get_interval(
        self
    ) -> Tuple[Timestamp]:
        start_date = self._history_df.iloc[0].Date
        end_date = self._history_df.iloc[-1].Date
        return start_date, end_date

    def get_variation(
        self
    ) -> float:
        first_vale = self._history_df.iloc[0]['Close']
        last_value = self._history_df.iloc[-1]['Close']

        var = (last_value - first_vale) / first_vale
        return var
