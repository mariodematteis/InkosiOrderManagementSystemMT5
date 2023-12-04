import pandas as pd
from numpy.typing import NDArray

from inkosi.backtest.operation.asset import Asset
from inkosi.backtest.operation.models import SourceType
from inkosi.database.postgresql.database import PostgreSQLInstance


class Dataset:
    def __init__(
        self,
        source: str | Asset,
        source_type: SourceType,
        **kwargs,
    ) -> None:
        self.postgres_instance = PostgreSQLInstance()

        if isinstance(source, str) or isinstance(source, Asset):
            self.dataset: None = None

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
            case SourceType.ASSET:
                self.dataset: pd.DataFrame = pd.DataFrame(
                    {
                        0: source.dates(),
                        1: source.close_prices(),
                        2: source.open_prices(),
                    }
                )

        self.np_dataset: NDArray = self.dataset.to_numpy()

    def get_dataset(
        self,
    ) -> NDArray | None:
        return self.np_dataset
