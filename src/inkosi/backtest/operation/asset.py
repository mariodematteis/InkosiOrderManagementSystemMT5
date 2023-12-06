import numpy as np
from numpy.typing import NDArray

from inkosi.backtest.operation.quote import Quote
from inkosi.backtest.operation.schemas import AvailableRawColumns


class Asset:
    """
    A class for handling financial data for a specific asset.

    Parameters:
        asset_name (str): The name of the asset.
        period (str, optional): The time period for the financial data. Defaults to
        "1y" (1 year).
        time_frame (str, optional): The time frame for the financial data. Defaults to
        "1d" (1 day).

    Attributes:
        asset_name (str): The name of the asset.
        period (str): The time period for the financial data.
        time_frame (str): The time frame for the financial data.
        quote (Quote): An instance of the Quote class for downloading quotes.
        result: The result of downloading the quote for the specified asset.
        asset_data: Details of the financial data for the specified asset.

    Methods:
        dates() -> NDArray: Returns an array of dates in the financial data.
        open_prices() -> NDArray: Returns an array of open prices in the financial data.
        high_prices() -> NDArray: Returns an array of high prices in the financial data.
        low_prices() -> NDArray: Returns an array of low prices in the financial data.
        close_prices() -> NDArray: Returns an array of close prices in the financial
        data.
        returns() -> NDArray: Returns an array of returns in the financial data.
        return_distribution() -> NDArray: Returns a sorted array of return
        distributions.
    """

    def __init__(
        self,
        asset_name: str,
        period: str = "1y",
        time_frame: str = "1d",
    ):
        """
        Initialize the FinancialData object.

        Parameters:
            asset_name (str): The name of the asset.
            period (str, optional): The time period for the financial data. Defaults
            to "1y" (1 year).
            time_frame (str, optional): The time frame for the financial data. Defaults
            to "1d" (1 day).
        """

        self.asset_name = asset_name
        self.period = period
        self.time_frame = time_frame

        self.quote = Quote()
        self.result = self.quote.download_quote(self.asset_name)
        self.asset_data = self.quote.details(self.asset_name)

    def dates(self) -> NDArray:
        """
        Get an array of dates in the financial data.

        Returns:
            NDArray: Array of dates.
        """

        return self.asset_data[AvailableRawColumns.DATES]

    def open_prices(self) -> NDArray:
        """
        Get an array of open prices in the financial data.

        Returns:
            NDArray: Array of open prices.
        """
        return self.asset_data[AvailableRawColumns.OPEN_PRICE]

    def high_prices(self) -> NDArray:
        """
        Get an array of high prices in the financial data.

        Returns:
            NDArray: Array of high prices.
        """

        return self.asset_data[AvailableRawColumns.HIGH_PRICE]

    def low_prices(self) -> NDArray:
        """
        Get an array of low prices in the financial data.

        Returns:
            NDArray: Array of low prices.
        """

        return self.asset_data[AvailableRawColumns.LOW_PRICE]

    def close_prices(self) -> NDArray:
        """
        Get an array of close prices in the financial data.

        Returns:
            NDArray: Array of close prices.
        """

        return self.asset_data[AvailableRawColumns.CLOSE_PRICE]

    def returns(self) -> NDArray:
        """
        Get an array of returns in the financial data.

        Returns:
            NDArray: Array of returns.
        """

        return self.asset_data[AvailableRawColumns.RETURNS]

    def return_distribution(self) -> NDArray:
        """
        Get a sorted array of return distributions.

        Returns:
            NDArray: Sorted array of return distributions.
        """

        return np.sort(self.asset_data[AvailableRawColumns.RETURNS])
