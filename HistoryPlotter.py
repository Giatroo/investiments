from abc import ABC, abstractmethod

from pandas import DataFrame
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

from HistoryInformationRetriever import HistoryInformationRetriever


class HistoryPlotter(ABC):
    @abstractmethod
    def lineplot(
        self,
        ticker_code: str,
        **history_kwargs
    ) -> None:
        pass

    @abstractmethod
    def multi_lineplot(
        self,
        history_df: DataFrame
    ) -> None:
        pass

    @abstractmethod
    def candlestick(
        self,
        ticker_code: str,
        **history_kwargs
    ) -> None:
        pass

    @abstractmethod
    def dividends(
        self,
        ticker_code: str,
        **history_kwargs
    ) -> None:
        pass


class MatplotHistoryPlotter(HistoryPlotter):
    def __init__(
        self
    ) -> None:
        plt.rcdefaults()
        plt.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')

    def lineplot(
        self,
        ticker_code: str,
        ax = None,
        **history_kwargs
    ) -> None:
        info_retriever = HistoryInformationRetriever(ticker_code, **history_kwargs)

        variation = info_retriever.get_variation()
        series = info_retriever.get_values_over_time()
        time_interval = info_retriever.get_interval()
        ticker_code = info_retriever._ticker_code

        color = 'C1' if variation > 0 else 'C2'

        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))
        plt.plot(series.index, series, linewidth=3, c=color)

        ax.set_xlim(time_interval)
        ax.set_ylabel('')
        ax.set_xlabel('')

        ax.set_title(f'{ticker_code} ({variation * 100:.2f}%)',
                     color=color,
                     fontsize='x-large',
                     fontweight='bold')

        ax.spines[:].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.grid(which='major', axis='y', linewidth=0.1)

    def multi_lineplot(
        self,
        history_df : DataFrame,
        ax = None
    ) -> None:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))

        for ticker_code in history_df.columns:
            plt.plot(history_df.index, history_df[ticker_code], linewidth=1, label=ticker_code)

        time_interval = history_df.index.min(), history_df.index.max()
        ax.set_xlim(time_interval)
        ax.set_ylabel('')
        ax.set_xlabel('')

        ax.spines[:].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.grid(which='major', axis='y', linewidth=0.1)

        ax.legend()

    def candlestick(
        self,
        ticker_code: str,
        **history_kwargs
    ) -> None:
        return super().candlestick()

    def dividends(
        self,
        ticker_code: str,
        ax = None,
        **history_kwargs
    ) -> None:
        info_retriever = HistoryInformationRetriever(ticker_code, **history_kwargs)
        series = info_retriever.get_dividends_over_time()

        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))
        ax.bar(series.index, series, width=5, color='C1')

        ax.set_title(f'{ticker_code} dividends',
                     color='C1',
                     fontsize='x-large',
                     fontweight='bold')

        ax.spines[:].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.grid(which='major', axis='y', linewidth=0.1)

        fig.show()