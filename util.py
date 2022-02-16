import yfinance as yf
from yfinance import Ticker

def get_ticker(ticker_code: str) -> Ticker:
    """Receives a ticker code and returns the corresponding yfinance Ticker
    object.

    It receives South America ticker names.

    Parameters
    ----------
    ticker_code : str
        A ticker code.

    Returns
    -------
    Ticker
        The south america ticker.
    """
    return yf.Ticker(f'{ticker_code}.sa'.upper())
