from abc import ABC, abstractmethod
from typing import Dict, List, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import Cycler, cycler
from matplotlib.axes import Axes
from pandas import Series, Timestamp


class StockPlotter(ABC):
    _colors: Dict[str, str]

    def __init__(self) -> None:
        self._colors = dict()

    @abstractmethod
    def lineplot(self, stock_name: str, stock_series: Series) -> None:
        """Plots a line of the stocks prices. If the final price is higher than
        the initial price, the line is plotted in green. If the final price is
        lower than the initial price, the line is plotted in red.

        The title is contains the name of the stock and the overall performance.

        Parameters
        ----------
        stock_name : str
            The stock name.
        stock_series : Series
            The series of prices.
        """
        pass

    @abstractmethod
    def multi_lineplot(
        self,
        stock_names: List[str],
        stocks_series: List[Series],
    ) -> None:
        """Plots multiple lines for each stock.

        Parameters
        ----------
        stock_names : List[str]
            The names of the stocks, it can be used to label the lines.
        stocks_series : List[Series]
            The series of prices.
        """
        pass

    @abstractmethod
    def candlestick(self, stock_name: str, stock_series: Series) -> None:
        pass

    @abstractmethod
    def dividends(self, stock_name: str, stock_series: Series) -> None:
        """Plots the dividends of the stock.

        Parameters
        ----------
        stock_name : str
            The stock name.
        stock_series : Series
            The series of dividends.
        """
        pass


class MatplotStockPlotter(StockPlotter):
    def __init__(self) -> None:
        super().__init__()
        plt.rcdefaults()
        self._set_colors()

    def _set_colors(self) -> None:
        self._colors["red"] = "r"
        self._colors["green"] = "g"
        self._colors["blue"] = "b"
        self._colors["cyan"] = "c"
        self._colors["magenta"] = "m"
        self._colors["yellow"] = "y"
        self._colors["black"] = "k"
        self._colors["white"] = "w"

    def lineplot(
        self,
        stock_name: str,
        stock_series: Series,
        ax: Union[Axes, None] = None,
    ) -> None:
        """Plots a line of the stocks prices. If the final price is higher than
        the initial price, the line is plotted in green. If the final price is
        lower than the initial price, the line is plotted in red.

        The title is contains the name of the stock and the overall performance.

        Parameters
        ----------
        stock_name : str
            The stock name.
        stock_series : Series
            The series of prices.
        """

        start_time = stock_series.index[0]
        end_time = stock_series.index[-1]
        normalized_series = stock_series / stock_series.iloc[0]
        variation = normalized_series[-1] - 1

        color = self._colors["green"] if variation > 0 else self._colors["red"]

        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))
        plt.plot(stock_series.index, stock_series, linewidth=3, c=color)

        ax.set_xlim([start_time, end_time])
        ax.set_ylabel("")
        ax.set_xlabel("")

        ax.set_title(
            f"{stock_name} ({variation * 100:.2f}%)",
            color=color,
            fontsize="x-large",
            fontweight="bold",
        )

        ax.spines[:].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.grid(which="major", axis="y", linewidth=0.1)

    def _create_multi_lineplot_cycler(
        self,
        linewidths: Union[List[int], None] = None,
        linestyles: Union[List[str], None] = None,
        colors: Union[List[str], None] = None,
    ) -> Cycler:
        if colors is None:
            # remove background colors
            colors = list(self._colors.values())[:-2]
        num_colors = len(colors)
        if linewidths is None:
            linewidths = [1] * num_colors
        num_widths = len(linewidths)
        if linestyles is None:
            linestyles = ["-"] * num_colors
        num_styles = len(linestyles)

        max_cycle = max(num_colors, num_widths, num_styles)

        colors = (colors * max_cycle)[:max_cycle]
        linewidths = (linewidths * max_cycle)[:max_cycle]
        linestyles = (linestyles * max_cycle)[:max_cycle]

        color_cycler = cycler(color=colors)
        linewidth_cycler = cycler(linewidth=linewidths)
        linestyle_cycler = cycler(linestyle=linestyles)

        cycler_obj = color_cycler + linewidth_cycler + linestyle_cycler
        return cycler_obj

    def multi_lineplot(
        self,
        stocks_names: List[str],
        stocks_series: List[Series],
        linewidths: Union[List[int], None] = None,
        linestyles: Union[List[str], None] = None,
        colors: Union[List[str], None] = None,
        title: str = "",
        ax: Union[Axes, None] = None,
    ) -> None:
        """Plots multiple lines for each stock.

        Parameters
        ----------
        stock_names : List[str]
            The names of the stocks, it can be used to label the lines.
        stocks_series : List[Series]
            The series of prices.
        """
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))

        cycler_obj = self._create_multi_lineplot_cycler(
            linewidths=linewidths, linestyles=linestyles, colors=colors
        )
        ax.set_prop_cycle(cycler_obj)

        tmp_series = stocks_series[0]
        start_time = Timestamp(tmp_series.index[0])
        end_time = Timestamp(tmp_series.index[-1])
        for series, name in zip(stocks_series, stocks_names):
            ax.plot(series.index, series, label=name)

            series_start_time = Timestamp(series.index[0])
            series_end_time = Timestamp(series.index[-1])
            if series_start_time < start_time:
                start_time = series_start_time
            if series_end_time > end_time:
                end_time = series_end_time

        ax.set_xlim([start_time, end_time])
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.set_title(title)

        ax.spines[:].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.grid(which="major", axis="y", linewidth=0.1)
        ax.legend(loc="upper left")

    def candlestick(self, stock_name: str, stock_series: Series) -> None:
        return super().candlestick(stock_name, stock_series)

    def dividends(
        self,
        stock_name: str,
        dividends: Series,
        ax: Union[Axes, None] = None,
    ) -> None:
        """Plots the dividends of the stock.

        Parameters
        ----------
        stock_name : str
            The stock name.
        stock_series : Series
            The series of dividends.
        """
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(15, 3))

        ax.bar(dividends.index, dividends, width=5, color=self._colors["green"])

        ax.set_title(
            f"{stock_name} dividends",
            color=self._colors["green"],
            fontsize="x-large",
            fontweight="bold",
        )

        dividends.index = dividends.index.strftime("%Y-%m")

        ax.set_xticks(dividends.index)
        ax.set_xticklabels(dividends.index)
        ax.spines[:].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.grid(which="major", axis="y", linewidth=0.1)


class OneDarkPlotDecorator(MatplotStockPlotter):
    _decorated_obj: MatplotStockPlotter

    def __init__(self, decorated_obj: MatplotStockPlotter) -> None:
        self._decorated_obj = decorated_obj

    def _get_theme(self):
        background_color = "#292C34"
        white_color = "#ABB2BF"

        self._decorated_obj._colors["red"] = "#E06C75"
        self._decorated_obj._colors["green"] = "#98C379"
        self._decorated_obj._colors["blue"] = "#61AFEF"
        self._decorated_obj._colors["cyan"] = "#56B6C2"
        self._decorated_obj._colors["magenta"] = "#C678DD"
        self._decorated_obj._colors["yellow"] = "#E5C07B"
        self._decorated_obj._colors["black"] = background_color
        self._decorated_obj._colors["white"] = white_color

        return {
            "text.color": white_color,
            "xtick.color": white_color,
            "ytick.color": white_color,
            "axes.facecolor": background_color,
            "figure.facecolor": background_color,
            "lines.color": white_color,
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
