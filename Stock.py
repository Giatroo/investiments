from abc import ABC, abstractmethod

from pandas import DataFrame, Series
from yfinance import Ticker

import util


class StockInterface(ABC):
    @abstractmethod
    def get_history_df(self, **history_kwargs) -> DataFrame:
        pass

    @abstractmethod
    def get_normalized_history_df(self, **history_kwargs) -> DataFrame:
        pass

    @abstractmethod
    def get_close_series(self, **history_kwargs) -> DataFrame:
        pass

    @abstractmethod
    def get_period_valorization(self, period: str) -> float:
        pass

    @abstractmethod
    def get_dividends_series(self, **history_kwargs) -> Series:
        pass

    @abstractmethod
    def get_period_dividends(self, period: str) -> float:
        pass


class Stock(StockInterface):
    _ticker_code: str
    _ticker: Ticker
    _value: float

    def __init__(self, ticker_code: str, value: float = 1.0):
        self._ticker_code = ticker_code.upper()
        self._value = value
        self._ticker = util.get_ticker(self._ticker_code)

    def get_history_df(self, **history_kwargs) -> DataFrame:
        return self._ticker.history(**history_kwargs)

    def get_normalized_history_df(self, **history_kwargs) -> DataFrame:
        history_df = self.get_history_df(**history_kwargs)
        history_df /= history_df.iloc[0]
        return history_df

    def get_close_series(self, **history_kwargs) -> Series:
        history_df = self.get_history_df(**history_kwargs)
        return history_df["Close"]

    def get_period_valorization(self, period: str) -> float:
        n_history_df = self.get_normalized_history_df(period=period)
        return n_history_df.iloc[-1]["Close"]

    def get_dividends_series(self, **history_kwargs) -> Series:
        history_df = self.get_history_df(**history_kwargs)
        return history_df["Dividends"]

    def get_period_dividends(self, period: str) -> float:
        dividend_series = self.get_dividends_series(period=period)
        return dividend_series.sum()
