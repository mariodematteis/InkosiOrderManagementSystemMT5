from datetime import date
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
        time_frame="1d",
    ):
        self.period = period
        self.time_frame = time_frame

        self.logger = Logger("Quote", package_name="backtest.operation")

        self.financial_instruments = {}

    def download_quote(
        self,
        ticker: str,
        start: date | None = None,
        end: date | None = None,
    ) -> dict[str, list] | None:
        quote = yf.Ticker(ticker)

        try:
            if start and end:
                h_prices = quote.history(
                    start=start,
                    end=end,
                    interval=self.time_frame,
                )
            else:
                h_prices = quote.history(
                    period=self.period,
                    interval=self.time_frame,
                )
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
            "Dates": dates,
            "Open": open_prices,
            "High": high_prices,
            "Low": low_prices,
            "Close": close_prices,
            "Returns": list(returns),
        }

    def __repr__(self) -> str:
        return str(self.financial_instruments)
