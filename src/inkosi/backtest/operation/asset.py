from datetime import date

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from inkosi.backtest.operation.quote import Quote
from inkosi.backtest.operation.schemas import AvailableRawColumns, SamplingMethods


class Asset:
    def __init__(
        self,
        asset_name: str,
        period: str = "1y",
        time_frame: str = "1d",
        start: date | None = None,
        end: date | None = None,
    ):
        self.asset_name = asset_name
        self.period = period
        self.time_frame = time_frame

        self.quote = Quote(time_frame=time_frame)
        self.result = self.quote.download_quote(
            self.asset_name,
            start=start,
            end=end,
        )

    def sampling(
        self,
        sampling_method: SamplingMethods,
        steps_forward: int,
        column: str = AvailableRawColumns.CLOSE_PRICE,
        samples: int = 1,
    ) -> NDArray | None:
        if not 1 < steps_forward < 255 or not isinstance(steps_forward, int):
            return None

        if not 1 <= samples < 10000 or not isinstance(samples, int):
            return None

        prices = self.result.get(column, np.array([0]))
        last_prices = np.ones(shape=(samples, 1)) * prices[-1]

        match sampling_method:
            case SamplingMethods.NORMAL_DISTRIBUTION:
                sampling = np.random.normal(
                    loc=0,
                    scale=np.std(
                        self.close_prices(),
                    ),
                    size=(samples, steps_forward - 1),
                )

                cum_raw_last_prices = np.hstack((last_prices, sampling))
                cum_prices = np.cumsum(cum_raw_last_prices, axis=1)

                return self.plotting(
                    column,
                    np.hstack(
                        (
                            np.repeat(
                                np.reshape(prices, (prices.shape[0], 1)),
                                repeats=samples,
                                axis=1,
                            ).T,
                            cum_prices,
                        )
                    ),
                )
            case SamplingMethods.LAPLACE_DISTRIBUTION:
                sampling = np.random.laplace(
                    loc=0,
                    scale=np.std(
                        self.close_prices(),
                    ),
                    size=(samples, steps_forward - 1),
                )

                cum_raw_last_prices = np.hstack((last_prices, sampling))
                cum_prices = np.cumsum(cum_raw_last_prices, axis=1)

                return self.plotting(
                    column,
                    np.hstack(
                        (
                            np.repeat(
                                np.reshape(prices, (prices.shape[0], 1)),
                                repeats=samples,
                                axis=1,
                            ).T,
                            cum_prices,
                        )
                    ),
                )
            case SamplingMethods.UNIFORM_DISTRIBUTION:
                sampling = np.random.uniform(
                    low=0,
                    high=np.max(prices) - np.min(prices),
                    size=(samples, steps_forward - 1),
                )
                cum_raw_last_prices = np.hstack((last_prices, sampling))
                cum_prices = np.cumsum(cum_raw_last_prices, axis=1)

                return self.plotting(
                    column,
                    np.hstack(
                        (
                            np.repeat(
                                np.reshape(prices, (prices.shape[0], 1)),
                                repeats=samples,
                                axis=1,
                            ).T,
                            cum_prices,
                        )
                    ),
                )
            case _:
                return None

    def dates(self) -> NDArray:
        return self.result.get(AvailableRawColumns.DATES, [])

    def open_prices(self) -> NDArray:
        return self.result.get(AvailableRawColumns.OPEN_PRICE, [])

    def high_prices(self) -> NDArray:
        return self.result.get(AvailableRawColumns.HIGH_PRICE, [])

    def low_prices(self) -> NDArray:
        return self.result.get(AvailableRawColumns.LOW_PRICE, [])

    def close_prices(self) -> NDArray:
        return self.result.get(AvailableRawColumns.CLOSE_PRICE, [])

    def returns(self) -> NDArray:
        return self.result.get(AvailableRawColumns.RETURNS, [])

    def return_distribution(self) -> NDArray:
        return np.sort(self.result.get(AvailableRawColumns.RETURNS, []))

    def data_frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.result)

    def plotting(
        self,
        column: AvailableRawColumns = AvailableRawColumns.CLOSE_PRICE,
        sampling: NDArray | None = None,
    ) -> tuple:
        return (
            self.dates() if sampling is None else np.arange(0, sampling.shape[1]),
            self.result.get(column).reshape(1, self.result.get(column).shape[0])
            if sampling is None
            else sampling,
        )
