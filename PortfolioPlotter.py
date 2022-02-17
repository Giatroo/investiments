from cv2 import norm
from matplotlib.pyplot import hist
import pandas as pd

from Portfolio import Portfolio
from HistoryPlotter import HistoryPlotter

class PortfolioPlotter():
    _portfolio: Portfolio
    _plotter: HistoryPlotter

    def __init__(
        self,
        portfolio: Portfolio,
        history_plotter: HistoryPlotter
    ) -> None:
        self._portfolio = portfolio
        self._plotter = history_plotter
        
    def plot_individual_tickers(
        self,
        **history_kwargs
    ) -> None:
        history_df = self._portfolio.get_history_df(**history_kwargs)
        self._plotter.multi_lineplot(history_df)
        

    def plot_normalized_individual_tickers(
        self,
        **history_kwargs
    ) -> None:
        normalized_history_df = self._portfolio.get_normalized_history_df(**history_kwargs)
        self._plotter.multi_lineplot(normalized_history_df)

    def plot_portfolio(
        self,
        **history_kwargs
    ) -> None:
        portfolio_df = self._portfolio.get_portfolio_df(**history_kwargs)
        # temporary
        self._plotter.multi_lineplot(pd.DataFrame(portfolio_df['portfolio']))

    def plot_portfolio_and_individual_tickers(
        self,
        **history_kwargs
    ) -> None:
        portfolio_df = self._portfolio.get_normalized_portfolio_df(**history_kwargs)
        self._plotter.multi_lineplot(portfolio_df)
