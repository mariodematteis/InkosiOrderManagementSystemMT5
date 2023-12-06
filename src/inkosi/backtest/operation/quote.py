from typing import Any

import numpy as np
import yfinance as yf

from inkosi.log.log import Logger


class QuoteMetaclass(type):
    """
    Metaclass for the Quote class to ensure a single instance.
    """

    _instance = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        Create or return the existing instance of the Quote class.
        """

        if not self._instance:
            return super().__call__(*args, **kwds)

        return self._instance


class Quote(metaclass=QuoteMetaclass):
    """
    Class for handling financial quotes and historical prices.

    Attributes:
        period (str): The period for historical prices (default: "1y").
        time_frame (str): The time frame for historical prices (default: "1d").
        logger (Logger): Logger instance for logging messages.
        financial_instruments (dict): Dictionary to store financial instruments and
        their details.
    """

    def __init__(
        self,
        period="1y",
        timeframe="1d",
    ):
        """
        Initialize the Quote class.

        Parameters:
            period (str): The period for historical prices.
            time_frame (str): The time frame for historical prices.
        """

        self.period = period
        self.time_frame = timeframe

        self.logger = Logger("Quote", package_name="backtest.operation")

        self.financial_instruments = {}

    def download_quote(self, ticker: str) -> dict[str, list] | None:
        """
        Download historical prices for a given ticker.

        Parameters:
            ticker (str): The financial instrument's ticker.

        Returns:
            dict[str, list] | None: Historical prices as a dictionary or None if the
            ticker is not found.
        """

        quote = yf.Ticker(ticker)

        try:
            h_prices = quote.history(period=self.period, interval=self.time_frame)
        except Exception:
            self.logger.error("Unable to find the specififed ticker")
            return

        dates = h_prices.index.astype(str).to_numpy()
        open_prices = h_prices["Open"].to_numpy()
        high_prices = h_prices["High"].to_numpy()
        low_prices = h_prices["Low"].to_numpy()
        close_prices = h_prices["Close"].to_numpy()

        returns = np.array(close_prices) - np.array(open_prices)

        return {
            "DATES": dates,
            "OPEN": open_prices,
            "HIGH": high_prices,
            "LOW": low_prices,
            "CLOSE": close_prices,
            "RETURNS": list(returns),
        }

    def details(
        self,
        ticker: str,
    ) -> dict[str | list] | None:
        """
        Get details of a financial instrument.

        Parameters:
            ticker (str): The financial instrument's ticker.

        Returns:
            dict[str | list] | None: Details of the financial instrument or None if not
            found.
        """

        return self.financial_instruments.get(ticker)

    def __repr__(self) -> str:
        """
        Return a string representation of the Quote instance.
        """

        return str(self.financial_instruments)
