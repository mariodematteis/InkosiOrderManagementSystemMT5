import pandas as pd
from numpy.typing import NDArray

from inkosi.backtest.operation.models import SourceType
from inkosi.database.postgresql.database import PostgreSQLInstance


class Dataset:
    """
    A class for handling datasets from various sources.

    Parameters:
        source (str): The source of the dataset (e.g., SQL table, CSV file, HDF file,
        Parquet file).
        source_type (SourceType): The type of the data source (enum: SQL, CSV, HDF,
        PARQUET).
        **kwargs: Additional keyword arguments for reading data from the source.

    Attributes:
        postgres_instance (PostgreSQLInstance): An instance of the PostgreSQLInstance
        class for SQL data source.
        dataset (pd.DataFrame): The dataset loaded from the specified source.
        np_dataset (NDArray): The dataset converted to a NumPy array.

    Methods:
        get_dataset() -> NDArray | None: Returns the dataset as a NumPy array or None
        if not available.
    """

    def __init__(
        self,
        source: str,
        source_type: SourceType,
        **kwargs,
    ) -> None:
        """
        Initialize the Dataset object.

        Parameters:
            source (str): The source of the dataset (e.g., SQL table, CSV file, HDF
            file, Parquet file).
            source_type (SourceType): The type of the data source (enum: SQL, CSV, HDF,
            PARQUET).
            **kwargs: Additional keyword arguments for reading data from the source.
        """

        self.postgres_instance = PostgreSQLInstance()

        match source_type:
            case SourceType.SQL:
                with self.postgres_instance.engine.connect() as conn, conn.begin():
                    self.dataset: pd.DataFrame = pd.read_sql_table(
                        table_name=source,
                        con=conn,
                        **kwargs,
                    )
            case SourceType.CSV:
                self.dataset: pd.DataFrame = pd.read_csv(
                    filepath_or_buffer=source,
                    **kwargs,
                )
            case SourceType.HDF:
                self.dataset: pd.DataFrame = pd.read_hdf(
                    path_or_buf=source,
                    **kwargs,
                )
            case SourceType.PARQUET:
                self.dataset: pd.DataFrame = pd.read_parquet(
                    path=source,
                    **kwargs,
                )

        self.np_dataset: NDArray = self.dataset.to_numpy()

    def get_dataset(
        self,
    ) -> NDArray | None:
        """
        Get the dataset as a NumPy array.

        Returns:
            NDArray | None: The dataset as a NumPy array or None if not available.
        """

        return self.np_dataset
