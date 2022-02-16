from abc import ABC, abstractmethod
from matplotlib import ticker

from pandas import DataFrame
import matplotlib.pyplot as plt

from HistoryInformationRetriever import HistoryInformationRetriever


class HistoryPlotter(ABC):
    _info_retriever: DataFrame

    def __init__(
        self,
        ticker_code: DataFrame,
        **history_kwargs
    ) -> None:
        self._info_retriever = HistoryInformationRetriever(ticker_code, **history_kwargs)

    @abstractmethod
    def lineplot(self) -> None:
        pass

    @abstractmethod
    def candlestick(self) -> None:
        pass

    @abstractmethod
    def dividends(self) -> None:
        pass


class MatplotHistoryPlotter(HistoryPlotter):
    def __init__(self,
                 ticker_code: DataFrame,
                 theme: str = 'onedark',
                 **history_kwargs
                 ) -> None:
        super().__init__(ticker_code, **history_kwargs)

        if theme == 'onedark':
            self._set_onedark_theme()

    def _set_onedark_theme(self):
        self._background_color = '#292C34'
        self._green_color = '#98C379'
        self._red_color = '#E06C75'
        self._white_color = '#ABB2BF'

        plt.rcParams.update({'text.color': self._white_color,
                            'xtick.color': self._white_color,
                             'ytick.color': self._white_color,
                             'axes.facecolor': self._background_color,
                             'figure.facecolor': self._background_color,
                             'lines.color': self._white_color
                             })

    def lineplot(self) -> None:
        variation = self._info_retriever.get_variation()
        series = self._info_retriever.get_values_over_time()
        time_interval = self._info_retriever.get_interval()
        ticker_code = self._info_retriever._ticker_code

        color = self._green_color if variation > 0 else self._red_color

        fig, ax = plt.subplots(1, 1, figsize=(15, 3))
        plt.plot(series.index, series, linewidth=5, c=color)

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

        fig.show()

    def candlestick(self) -> None:
        return super().candlestick()

    def dividends(self) -> None:
        series = self._info_retriever.get_dividends_over_time()
        ticker_code = self._info_retriever._ticker_code


        fig, ax = plt.subplots(1, 1, figsize=(15, 3))
        ax.bar(series.index, series, width=5, color=self._green_color)

        ax.set_title(f'{ticker_code} dividends', 
                     color=self._green_color,
                     fontsize='x-large',
                     fontweight='bold')

        ax.spines[:].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.grid(which='major', axis='y', linewidth=0.1)

        fig.show()