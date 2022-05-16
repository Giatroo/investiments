from typing import List, Union

from Portfolio import Portfolio
from StockPlotter import MatplotStockPlotter


class PortfolioPlotter:
    _portfolio: Portfolio
    _plotter: MatplotStockPlotter

    def __init__(
        self, portfolio: Portfolio, plotter: MatplotStockPlotter
    ) -> None:
        self._portfolio = portfolio
        self._plotter = plotter

    def plot_individual_tickers(
        self,
        linewidths: Union[List[int], None] = None,
        linestyles: Union[List[str], None] = None,
        colors: Union[List[str], None] = None,
        title: str = "",
        **history_kwargs
    ) -> None:
        portfolio_stocks = self._portfolio.stocks
        stocks_names = [stock.name for stock in portfolio_stocks]
        stocks_series = [
            stock.get_close_series(**history_kwargs)
            for stock in portfolio_stocks
        ]
        self._plotter.multi_lineplot(
            stocks_names,
            stocks_series,
            linewidths=linewidths,
            linestyles=linestyles,
            colors=colors,
            title=title,
        )

    def plot_normalized_individual_tickers(
        self,
        linewidths: Union[List[int], None] = None,
        linestyles: Union[List[str], None] = None,
        colors: Union[List[str], None] = None,
        title: str = "",
        **history_kwargs
    ) -> None:
        portfolio_stocks = self._portfolio.stocks
        stocks_names = [stock.name for stock in portfolio_stocks]
        stocks_series = [
            stock.get_normalized_close_series(**history_kwargs)
            for stock in portfolio_stocks
        ]
        self._plotter.multi_lineplot(
            stocks_names,
            stocks_series,
            linewidths=linewidths,
            linestyles=linestyles,
            colors=colors,
            title=title,
        )

    def plot_portfolio_as_stock(self, **history_kwargs) -> None:
        series = self._portfolio.get_close_series(**history_kwargs)
        self._plotter.lineplot(self._portfolio.name, stock_series=series)

    def plot_portfolio(self, **history_kwargs) -> None:
        stocks_names = [stock.name for stock in self._portfolio.stocks]
        stocks_names += [self._portfolio.name]
        stocks_series = [
            stock.get_close_series(**history_kwargs)
            for stock in self._portfolio.stocks
        ]
        stocks_series += [self._portfolio.get_close_series(**history_kwargs)]

        num_stocks = len(stocks_names) - 1
        linewidths = [1] * num_stocks + [3]
        linestyles = ["--"] * num_stocks + ["-"]

        self._plotter.multi_lineplot(
            stocks_names=stocks_names,
            stocks_series=stocks_series,
            linewidths=linewidths,
            linestyles=linestyles,
            title="Portfolio performance",
        )
