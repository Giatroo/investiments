from statistics import variance
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

    def plot_portfolio_as_stock(
        self,
        **history_kwargs
    ) -> None:
        portfolio_values = self._portfolio.get_portfolio_values(**history_kwargs)
        
        first_vale = portfolio_values.iloc[0]
        last_value = portfolio_values.iloc[-1]
        variation = (last_value - first_vale) / first_vale

        color = 'g' if variation > 0 else 'r'
        title = f'Portfolio ({variation * 100:.2f}%)'

        self._plotter.multi_lineplot(pd.DataFrame(portfolio_values),
                                     colors=[color],
                                     title=title)

    def plot_portfolio(
        self,
        **history_kwargs
    ) -> None:
        portfolio_df = self._portfolio.get_normalized_portfolio_df(**history_kwargs)

        num_stocks = len(portfolio_df.columns) - 1
        linewidths = [1] * num_stocks + [3]
        linestyles = ['--'] * num_stocks + ['-']

        self._plotter.multi_lineplot(portfolio_df, 
                                     linewidths=linewidths,
                                     linestyles=linestyles,
                                     title='Portfolio performance')
