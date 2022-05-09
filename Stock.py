from abc import ABC, abstractmethod

from pandas import DataFrame, Series
from yfinance import Ticker

import util


class StockInterface(ABC):
    @abstractmethod
    def get_stock_name(self) -> str:
        """Returns the name of the stock.

        Returns
        -------
        name : str
            The name of the stock. Each subclass can define how it returns the
            name.
        """
        pass

    @abstractmethod
    def get_history_df(self, **history_kwargs) -> DataFrame:
        """The history DataFrame of the stock.

        The history DataFrame is a pandas DataFrame with the following columns:
        - Open
        - High
        - Low
        - Close
        - Volume
        - Dividends
        - Stock Splits

        The index of the DataFrame is the time. Depending on how the client
        requests it, the name of the index may vary. The names can be:
        - Date - if it only contains the days (for intervals of 1 day, 5 days,
        1 week, 1 month, and 3 months)
        - Datetime - if it also contains minutes (for intervals of 1 minute, 2
        minutes, 5 minutes, 15 minutes, 30 minutes, 60 minutes, 90 minutes, and
        1 hour)

        Returns
        -------
        history_df : DataFrame
            The history DataFrame of the stock.

        See Also
        --------
        yfinance.Ticker.history
        """
        pass

    @abstractmethod
    def get_normalized_history_df(self, **history_kwargs) -> DataFrame:
        """Returns the same history DataFrame as get_history_df, but normalized.

        It means that the values of the DataFrame are 1.0 and the other lines
        are the variation betweeen that day and the first day.

        Returns
        -------
        norm_history_df : DataFrame
            The normalized history DataFRame.


        See Also
        --------
        get_history_df
        """
        pass

    @abstractmethod
    def get_close_series(self, **history_kwargs) -> Series:
        """Returns a series of the close values of the stock. It's the same as
        the history DataFrame, but only the 'Close' column.

        Returns
        -------
        close_series : Series
            The series of the close values of the stock.

        See Also
        --------
        get_history_df
        """
        pass

    @abstractmethod
    def get_normalized_close_series(self, **history_kwargs) -> Series:
        """Returns the same series as get_close_series, but normalized.

        It means that the values of the Series are 1.0 and the other lines are
        the variation betweeen that day and the first day.

        Returns
        -------
        norm_close_series : Series
            The normalized series of the close values of the stock.

        See Also
        --------
        get_close_series
        """
        pass

    @abstractmethod
    def get_period_valorization(self, period: str) -> float:
        """Returns the valorization or devaluation of the stock in a given period.

        Parameters
        ----------
        period : str
            The period. Must be a string accepted by the Yahoo Finance API.

        Returns
        -------
        valorization : float
            The valorization or devaluation of the stock in the given period.

        See Also
        --------
        yfinance.Ticker.history
        """
        pass

    @abstractmethod
    def get_dividends_series(self, **history_kwargs) -> Series:
        """Returns a series of dividends of the stock.

        Returns
        -------
        dividends : Series
            The series of dividends of the stock.
        """
        pass

    @abstractmethod
    def get_monthly_dividends_series(self, **history_kwargs) -> Series:
        """Returns a series of dividends of the stock aggregating over the
        months.

        Returns
        -------
        dividends : Series
            The series of dividends of the stock aggregated over the months.
        """
        pass

    @abstractmethod
    def get_period_dividends(self, period: str) -> float:
        """Returns the total amount of dividends in a given period.

        Parameters
        ----------
        period : str
            The period. Must be a string accepted by the Yahoo Finance API.

        Returns
        -------
        dividends : float
            The total amount of dividends in the given period.
        """
        pass


class Stock(StockInterface):
    _ticker_code: str
    _ticker: Ticker
    _value: float

    def __init__(self, ticker_code: str, value: float = 1.0):
        self._ticker_code = ticker_code.upper()
        self._value = value
        self._ticker = util.get_ticker(self._ticker_code)

    def get_stock_name(self) -> str:
        return self._ticker_code

    def get_history_df(self, **history_kwargs) -> DataFrame:
        return self._ticker.history(**history_kwargs)

    def get_normalized_history_df(self, **history_kwargs) -> DataFrame:
        history_df = self.get_history_df(**history_kwargs)
        history_df /= history_df.iloc[0]
        return history_df

    def get_close_series(self, **history_kwargs) -> Series:
        history_df = self.get_history_df(**history_kwargs)
        return history_df["Close"]

    def get_normalized_close_series(self, **history_kwargs) -> Series:
        close_series = self.get_close_series(**history_kwargs)
        close_series /= close_series.iloc[0]
        return close_series

    def get_period_valorization(self, period: str) -> float:
        n_close_series = self.get_normalized_close_series(period=period)
        return n_close_series[-1]

    def get_dividends_series(self, **history_kwargs) -> Series:
        history_df = self.get_history_df(**history_kwargs)
        return history_df["Dividends"]

    def get_monthly_dividends_series(self, **history_kwargs) -> Series:
        if "interval" in history_kwargs:
            history_kwargs = history_kwargs.copy()
            del history_kwargs["interval"]
        dividend_series = self.get_dividends_series(**history_kwargs)
        return dividend_series.resample("MS").sum()

    def get_period_dividends(self, period: str) -> float:
        dividend_series = self.get_dividends_series(period=period)
        return dividend_series.sum()
