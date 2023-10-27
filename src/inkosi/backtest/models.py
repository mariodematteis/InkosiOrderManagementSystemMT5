from dataclasses import dataclass
from datetime import datetime

from inkosi.database.mongodb.schemas import Position
from inkosi.utils.utils import EnhancedStrEnum


class SourceType(EnhancedStrEnum):
    SQL: str = "sql"
    CSV: str = "csv"
    HDF: str = "hdf"
    PARQUET: str = "parquet"


class TradeResult(EnhancedStrEnum):
    PROFIT: str = "profit"
    LOSS: str = "loss"
    PENDING: str = "pending"


class TradeStatus(EnhancedStrEnum):
    CLOSED: str = "closed"
    PENDING: str = "pending"


@dataclass
class BacktestRecord:
    direction: Position
    entry_point: float
    entry_point_index: int
    take_profit: float
    stop_loss: float
    price_close: float
    price_close_index: int
    time_opening: datetime
    time_closing: datetime
    status: TradeStatus
    result: TradeResult
