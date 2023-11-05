from dataclasses import dataclass
from enum import IntEnum


class StatusTradeResult(IntEnum):
    ORDER_FILLED: int = 0
    NO_TICKER_PROVIDED: int = -1
    TICKER_NOT_FOUND: int = -2
    NO_VOLUME_PROVIDED: int = -3
    NO_OPERATION_SPECIFIED: int = -4
    NO_TAKE_PROFIT_SPECIFIED: int = -5
    NO_STOP_LOSS_SPECIFIED: int = -6
    NO_ORDER_FILLING: int = -7


@dataclass
class OpenRequestTradeResult:
    trade_id: int
    detail: str
    status: StatusTradeResult
    error: str | None = None
    error_code: int | None = None
