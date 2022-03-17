from abc import ABC, abstractmethod
from itertools import cycle
from mimetypes import init
from typing import List, Dict

from pandas import DataFrame
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

from HistoryInformationRetriever import HistoryInformationRetriever


class HistoryPlotter(ABC):
    _colors : Dict[str, str]

    def __init__(
        self
    ) -> None:
        self._colors = dict()

    @abstractmethod
    def lineplot(
        self,
        ticker_code: str,
        info_retriever: HistoryInformationRetriever = None,
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
        info_retriever: HistoryInformationRetriever = None,
        **history_kwargs
    ) -> None:
        pass

    @abstractmethod
    def dividends(
        self,
        ticker_code: str,
        info_retriever: HistoryInformationRetriever = None,
        **history_kwargs
    ) -> None:
        pass


class MatplotHistoryPlotter(HistoryPlotter):
    def __init__(
        self
    ) -> None:
        super().__init__()
        plt.rcdefaults()
        self._set_colors()

    def _set_colors(
        self
    ) -> None:
        self._colors['red'] = 'r'
        self._colors['green'] = 'g'
        self._colors['blue'] = 'b'
        self._colors['cyan'] = 'c'
        self._colors['magenta'] = 'm'
        self._colors['yellow'] = 'y'
        self._colors['black'] = 'k'
        self._colors['white'] = 'w'

    def lineplot(
        self,
        ticker_code: str,
        info_retriever: HistoryInformationRetriever = None,
        ax = None,
        **history_kwargs
    ) -> None:
        if info_retriever is None:
            info_retriever = HistoryInformationRetriever(ticker_code, **history_kwargs)

        variation = info_retriever.get_variation()
        series = info_retriever.get_values_over_time()
        time_interval = info_retriever.get_interval()
        ticker_code = info_retriever.get_ticker_code()

        color = self._colors['green'] if variation > 0 else self._colors['red']

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
        linestyles : List[str] = None,
        colors : List[str] = None,
        labels : List[str] = None,
        title : str = '',
        ax = None
    ) -> None:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))

        num_cols = len(history_df.columns)
        if linewidths is None:
            linewidths = [1] * num_cols
        if len(linewidths) == 1:
            linewidths = linewidths * num_cols
        if linestyles is None:
            linestyles = ['-'] * num_cols
        if len(linestyles) == 1:
            linestyles = linestyles * num_cols
        if colors is None:
            colors = list(self._colors.values())[:num_cols]
        if labels is None:
            labels = history_df.columns.copy()

        cycler_obj = (cycler(color=colors) +
                      cycler(linewidth=linewidths) +
                      cycler(linestyle=linestyles))

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
        ax.legend(loc='upper left')

    def candlestick(
        self,
        ticker_code: str,
        info_retriever: HistoryInformationRetriever = None,
        **history_kwargs
    ) -> None:
        return super().candlestick(ticker_code, info_retriever, **history_kwargs)

    def dividends(
        self,
        ticker_code: str,
        info_retriever: HistoryInformationRetriever = None,
        ax = None,
        **history_kwargs
    ) -> None:
        if info_retriever is None:
            info_retriever = HistoryInformationRetriever(ticker_code, **history_kwargs)
        series = info_retriever.get_dividends_over_time()

        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))
        ax.bar(series.index, series, width=5, color=self._colors['green'])

        ax.set_title(f'{info_retriever.get_ticker_code()} dividends',
                     color=self._colors['green'],
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

        self._decorated_obj._colors['red'] = '#E06C75'
        self._decorated_obj._colors['green'] = '#98C379'
        self._decorated_obj._colors['blue'] = '#61AFEF'
        self._decorated_obj._colors['cyan'] = '#56B6C2'
        self._decorated_obj._colors['magenta'] = '#C678DD'
        self._decorated_obj._colors['yellow'] = '#E5C07B'
        self._decorated_obj._colors['black'] = background_color
        self._decorated_obj._colors['white'] = white_color

        return {'text.color': white_color,
                'xtick.color': white_color,
                'ytick.color': white_color,
                'axes.facecolor': background_color,
                'figure.facecolor': background_color,
                'lines.color': white_color,
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
