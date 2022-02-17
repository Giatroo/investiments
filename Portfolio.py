from typing import List
from matplotlib.pyplot import hist
from pandas import DataFrame
from numpy import dtype, ndarray

import pandas as pd
import numpy as np

from yfinance import Ticker
from itertools import combinations
from scipy.stats import pearsonr

from util import get_ticker

from HistoryInformationRetriever import HistoryInformationRetriever

class Portfolio:
    _ticker_codes: List[str]
    _tickers: List[Ticker]
    _percentages: ndarray
    _values: ndarray

    def __init__(
        self,
        ticker_codes: List[str],
        values: List[float] = None,
    ) -> None:
        self._ticker_codes = ticker_codes
        self._ticker_list = [get_ticker(ticker_code) for ticker_code in ticker_codes]
        self._values = np.array(values, dtype=np.float64)
        self._set_percentages(values)

    def _set_percentages(
        self,
        values: List[float]
    ) -> None:
        if values is None:
            num_tickers = len(self._ticker_codes)
            self._percentages = np.ones((num_tickers, ))
            self._percentages /= num_tickers
            return

        self._percentages = np.array(values, dtype=np.float64)
        self._percentages /= self._percentages.sum()
        self._check_percentage_consistency()

    def _check_percentage_consistency(
        self,
    ) -> None:
        percentage_sum = self._percentages.sum()

        assert percentage_sum == 1, "The sum of percentages must be 100 or 1."
        assert len(self._percentages) == len(self._ticker_codes), "The number of tickers must be equal to the number of percentages"

    def get_percentages(
        self
    ) -> ndarray:
        return self._percentages

    def get_history_df(
        self,
        **history_kwargs
    ) -> DataFrame:
        values_list = [HistoryInformationRetriever(ticker, **history_kwargs).get_values_over_time()
                       for ticker in self._ticker_codes]

        history_df = pd.concat(values_list, axis='columns')
        history_df.columns = self._ticker_codes
        return history_df

    def get_normalized_history_df(
        self,
        **history_kwargs
    ) -> DataFrame:
        history_df = self.get_history_df(**history_kwargs)
        history_df /= history_df.iloc[0]
        return history_df

    def get_portfolio_df(
        self, 
        **history_kwargs
    ) -> DataFrame:
        history_df = self.get_normalized_history_df(**history_kwargs)
        history_df *= self._values
        history_df['portfolio'] = history_df.sum(axis='columns')
        return history_df

    def get_normalized_portfolio_df(
        self, 
        **history_kwargs
    ) -> DataFrame:
        portfolio_df = self.get_portfolio_df(**history_kwargs)
        portfolio_df /= portfolio_df.iloc[0]
        return portfolio_df

    def get_correlations(self, **history_kwargs):
        for ticker1, ticker2 in combinations(self._ticker_list, 2):
            history1 = ticker1.history(**history_kwargs)['Close']
            history2 = ticker2.history(**history_kwargs)['Close']

            print(f'{ticker1.ticker} {ticker2.ticker} -> {pearsonr(history1, history2)[0]}')
