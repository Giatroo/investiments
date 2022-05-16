from functools import reduce
from itertools import combinations
from typing import List, Tuple

import numpy as np
from numpy import ndarray
from pandas import DataFrame, Series
from scipy.stats import pearsonr

from Stock import Stock, StockInterface


class Portfolio(StockInterface):
    _stocks: List[StockInterface]
    _percentages: ndarray
    _values: ndarray
    _portfolio_name: str

    def __init__(
        self,
        stocks: List[StockInterface],
        portfolio_name: str = "Portfolio",
    ) -> None:
        self._stocks = stocks
        self._portfolio_name = portfolio_name
        self._set_percentages()

    def _set_percentages(self) -> None:
        values_sum = sum(stock.value for stock in self._stocks)
        percentages = [stock.value / values_sum for stock in self._stocks]
        self._percentages = np.array(percentages, dtype=np.float64)
        self._check_percentage_consistency()

    def _check_percentage_consistency(
        self,
    ) -> None:
        percentage_sum = self._percentages.sum().round(3)
        num_percentages = len(self._percentages)
        num_tickers = len(self._stocks)

        assert (
            percentage_sum == 1
        ), f"The sum of percentages must be 1. It's {percentage_sum}."
        assert (
            num_percentages == num_tickers
        ), f"The number of tickers ({num_tickers}) must be equal to the number of percentages ({num_percentages})."

    @property
    def name(self) -> str:
        """Returns the name of the stock.

        Returns
        -------
        name : str
            The name of the stock. Each subclass can define how it returns the
            name.
        """
        return self._portfolio_name

    @property
    def value(self) -> float:
        """Returns the sum of the invested values in each asset.

        Returns
        -------
        value : float
            The value of the portfolio.
        """
        value = sum(stock.value for stock in self._stocks)
        return value

    @property
    def stocks(self) -> List[StockInterface]:
        return self._stocks

    def get_percentages(self) -> ndarray:
        return self._percentages

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
        history_dfs = [
            stock.get_history_df(**history_kwargs) for stock in self._stocks
        ]

        weighted_history_dfs = [
            history_df * percentage
            for history_df, percentage in zip(history_dfs, self._percentages)
        ]
        history_df = reduce(
            lambda x, y: x.add(y, fill_value=0.0), weighted_history_dfs
        )
        return history_df

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
        history_df = self.get_history_df(**history_kwargs)
        history_df /= history_df.iloc[0]
        return history_df

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
        history_df = self.get_history_df(**history_kwargs)
        return history_df["Close"]

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
        norm_history_df = self.get_normalized_history_df(**history_kwargs)
        return norm_history_df["Close"]

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
        norm_close_series = self.get_normalized_close_series(period=period)
        return norm_close_series.iloc[-1]

    def get_dividends_series(self, **history_kwargs) -> Series:
        """Returns a series of dividends of the stock.

        Returns
        -------
        dividends : Series
            The series of dividends of the stock.
        """
        history_df = self.get_history_df(**history_kwargs)
        return history_df["Dividents"]

    def get_monthly_dividends_series(self, **history_kwargs) -> Series:
        """Returns a series of dividends of the stock aggregating over the
        months.

        Returns
        -------
        dividends : Series
            The series of dividends of the stock aggregated over the months.
        """
        if "interval" in history_kwargs:
            history_kwargs = history_kwargs.copy()
            del history_kwargs["interval"]
        dividend_series = self.get_dividends_series(**history_kwargs)
        return dividend_series.resample("MS").sum()

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
        dividend_series = self.get_dividends_series(period=period)
        return dividend_series.sum()

    def _get_non_null_histories(self, histories: List[Series]) -> List[Series]:
        """Receives a list of histories and returns that same list of histories, but removing the null periods (and at the same time keeping the series with the same index).

        For example, if we have two series of one year (Jan to Jan) and the first has null values in March and the second has null values in July, than we'll return both Series without March and July.

        Parameters
        ----------
        histories : List[Series]
            A list of histories Series.

        Returns
        -------
        List[Series]
            The same list of histories, but removing the null periods.
        """
        # Copy the list of histories
        histories = list(map(lambda x: x.copy(), histories))

        # Get non null indexes
        non_null_idxs = map(lambda x: x.dropna().index, histories)
        # Get the intersection of the indexes
        non_null_idx = reduce(lambda x, y: x.intersection(y), non_null_idxs)
        # Keep only the intersection of non null indexes
        histories = list(map(lambda x: x[non_null_idx], histories))

        return histories

    def get_correlations(
        self, **history_kwargs
    ) -> List[Tuple[Stock, Stock, float]]:
        """Returns the correlations between the stocks of the portfolio.

        Returns
        -------
        List[Tuple[Stock, Stock, float]]
            A list of tuples with the two stock objects and the correlation between than. We return the stock objects instead of their names because this makes the method more flexible.
        """
        correlations = list()
        for stock1, stock2 in combinations(self._stocks, 2):
            history1 = stock1.get_close_series(**history_kwargs)
            history2 = stock2.get_close_series(**history_kwargs)

            history1, history2 = self._get_non_null_histories(
                [history1, history2]
            )

            correlation = pearsonr(history1, history2)[0]

            correlations.append((stock1, stock2, correlation))
        return correlations
