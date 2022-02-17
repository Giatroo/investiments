from abc import ABC, abstractmethod
from itertools import cycle
from typing import List

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
        linewidths : List[int] = None,
        colors : List[str] = None,
        labels : List[str] = None,
        title : str = '',
        ax = None
    ) -> None:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))

        if linewidths is None:
            linewidths = [1]
        if colors is None:
            colors = list('rgbcmyk')
        if labels is None:
            labels = history_df.columns.copy()

        cycler_obj = (cycler(color=colors) *
                      cycler(linewidth=linewidths))

        ax.set_prop_cycle(cycler_obj)
        for ticker_code, label in zip(history_df.columns, labels):
            ax.plot(history_df.index, history_df[ticker_code], label=label)

        time_interval = history_df.index.min(), history_df.index.max()
        ax.set_xlim(time_interval)
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_title(title)

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

class OneDarkPlotDecorator(HistoryPlotter):
    _decorated_obj: HistoryPlotter

    def __init__(
        self,
        decorated_obj: HistoryPlotter
    ) -> None:
        self._decorated_obj = decorated_obj

    def _get_theme(self):
        background_color = '#292C34'
        white_color = '#ABB2BF'

        return {'text.color': white_color,
                'xtick.color': white_color,
                'ytick.color': white_color,
                'axes.facecolor': background_color,
                'figure.facecolor': background_color,
                'lines.color': white_color,
                'axes.prop_cycle': cycler('color', ['#61afef',
                                                    '#98c379',
                                                    '#e06c75',
                                                    '#56b6c2',
                                                    '#c678dd',
                                                    '#e5c07b',
                                                    '#282c34',
                                                   ])
               }

    def lineplot(self, *args, **kwargs) -> None:
        with mpl.rc_context(rc=self._get_theme()):
            self._decorated_obj.lineplot(*args, **kwargs)

    def multi_lineplot(self, *args, **kwargs) -> None:
        with mpl.rc_context(rc=self._get_theme()):
            self._decorated_obj.multi_lineplot(*args, **kwargs)

    def candlestick(self, *args, **kwargs) -> None:
        with mpl.rc_context(rc=self._get_theme()):
            self._decorated_obj.candlestick(*args, **kwargs)

    def dividends(self, *args, **kwargs) -> None:
        with mpl.rc_context(rc=self._get_theme()):
            self._decorated_obj.dividends(*args, **kwargs)
