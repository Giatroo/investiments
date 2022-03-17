from HistoryInformationRetriever import HistoryInformationRetriever

from Portfolio import Portfolio
from HistoryPlotter import HistoryPlotter

from typing import List

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
        linewidths : List[int] = None,
        linestyles : List[str] = None,
        colors : List[str] = None,
        labels : List[str] = None,
        title : str = '',
        **history_kwargs
    ) -> None:
        history_df = self._portfolio.get_history_df(**history_kwargs)
        self._plotter.multi_lineplot(history_df, 
                                     linewidths=linewidths, 
                                     linestyles=linestyles,
                                     colors=colors,
                                     labels=labels,
                                     title=title)
        
    def plot_normalized_individual_tickers(
        self,
        linewidths : List[int] = None,
        linestyles : List[str] = None,
        colors : List[str] = None,
        labels : List[str] = None,
        title : str = '',
        **history_kwargs
    ) -> None:
        normalized_history_df = self._portfolio.get_normalized_history_df(**history_kwargs)
        self._plotter.multi_lineplot(normalized_history_df,
                                     linewidths=linewidths, 
                                     linestyles=linestyles,
                                     colors=colors,
                                     labels=labels,
                                     title=title)

    def plot_portfolio_as_stock(
        self,
        **history_kwargs
    ) -> None:
        history_df = self._portfolio.get_portfolio_as_history(**history_kwargs).reset_index()
        history_df.rename(columns={history_df.columns[0]: 'Date'}, inplace=True)

        info_retriever = HistoryInformationRetriever('portfolio', history_df=history_df, **history_kwargs)
        
        self._plotter.lineplot('portfolio', info_retriever=info_retriever, **history_kwargs)

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
