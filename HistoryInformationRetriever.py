from cv2 import getTickCount
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
        **history_kwargs
    ) -> None:
        ticker = get_ticker(ticker_code) 
        self._ticker_code = ticker_code.upper()
        self._history_df = ticker.history(**history_kwargs).reset_index()

    def get_values_over_time(
        self
    ) -> Series:
        return self._history_df.set_index('Date')['Close']

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
