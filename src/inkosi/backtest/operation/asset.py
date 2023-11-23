import numpy as np
from numpy.typing import NDArray

from .quote import Quote
from .schemas import AvailableRawColumns


class Asset:
    def __init__(
        self,
        asset_name: str,
        period: str = "1y",
        time_frame: str = "1d",
    ):
        self.asset_name = asset_name
        self.period = period
        self.time_frame = time_frame

        self.quote = Quote()
        self.result = self.quote.download_quote(self.asset_name)
        self.asset_data = self.quote.details(self.asset_name)

    def dates(self) -> NDArray:
        return self.asset_data[AvailableRawColumns.DATES]

    def open_prices(self) -> NDArray:
        return self.asset_data[AvailableRawColumns.OPEN_PRICE]

    def high_prices(self) -> NDArray:
        return self.asset_data[AvailableRawColumns.HIGH_PRICE]

    def low_prices(self) -> NDArray:
        return self.asset_data[AvailableRawColumns.LOW_PRICE]

    def close_prices(self) -> NDArray:
        return self.asset_data[AvailableRawColumns.CLOSE_PRICE]

    def returns(self) -> NDArray:
        return self.asset_data[AvailableRawColumns.RETURNS]

    def return_distribution(self) -> NDArray:
        return np.sort(self.asset_data[AvailableRawColumns.RETURNS])
