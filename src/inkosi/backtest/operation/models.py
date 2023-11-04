from dataclasses import dataclass
from datetime import datetime

from inkosi.backtest.operation.sources import Dataset
from inkosi.database.mongodb.schemas import Position
from inkosi.utils.utils import EnhancedStrEnum

TICKS_DATETIME_INDEX = 0
TICKS_BID_INDEX = 1
TICKS_ASK_INDEX = 2


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


@dataclass
class BacktestRequest:
    starting_indexes: list[int]
    direction: list[Position]
    take_profits: list[float]
    stop_losses: list[float]
    dataset: Dataset
