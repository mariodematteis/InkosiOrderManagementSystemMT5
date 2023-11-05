from dataclasses import dataclass

from inkosi.utils.utils import EnhancedStrEnum


class OrderType(EnhancedStrEnum):
    MARKET_ORDER: str = "market_order"
    SCHEDULED: str = "scheduled"


class Position(EnhancedStrEnum):
    BUY: str = "buy"
    SELL: str = "sell"


@dataclass
class TradeRequest:
    fund: int | None = None
    portfolio_manager: int | None = None
    ats: str | None = None
    investors: dict | None = None
    order_type: OrderType | None = None
    operation: Position | None = None
    ticker: str | None = None
    take_profit: float | None = None
    stop_loss: float | None = None
    entry_point: float | None = None
    close_price: float | None = None
    volume: float | None = None
    returns: float | None = None
    commission_broker: float | None = None
    commission_fund: float | None = None
    risk_management: bool | None = None
    notes: dict | None = None
