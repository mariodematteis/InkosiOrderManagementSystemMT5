from typing import Any

import numpy as np
import yfinance as yf

from inkosi.log.log import Logger


class QuoteMetaclass(type):
    _instance = None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self._instance:
            return super().__call__(*args, **kwds)

        return self._instance


class Quote(metaclass=QuoteMetaclass):
    def __init__(
        self,
        period="1y",
        timeframe="1d",
    ):
        self.period = period
        self.time_frame = timeframe

        self.logger = Logger("Quote", package_name="backtest.operation")

        self.financial_instruments = {}

    def download_quote(self, ticker: str) -> dict[str, list] | None:
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
        return self.financial_instruments.get(ticker)

    def __repr__(self) -> str:
        return str(self.financial_instruments)
