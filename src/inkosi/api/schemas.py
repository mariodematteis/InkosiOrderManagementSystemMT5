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
    NO_FILLING_TYPE_FOUND: int = -8
    MARKET_CLOSED: int = -9
    NO_DEAL_ID_FOUND: int = -10
    NO_POSITION_ID_FOUND: int = -11


@dataclass
class OpenRequestTradeResult:
    detail: str
    status: StatusTradeResult
    trade_id: int | None = None
    deal_id: int | None = None
    volume: float | None = None
    error: str | None = None
    error_code: int | None = None


@dataclass
class CloseRequestTradeResult:
    detail: str
    status: StatusTradeResult
    profit: float | None = None
    fee: float | None = None
    error: str | None = None
    error_code: int | None = None
