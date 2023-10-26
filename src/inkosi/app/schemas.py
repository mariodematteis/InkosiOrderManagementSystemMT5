from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class Position(StrEnum):
    BUY: str = "buy"
    SELL: str = "sell"


@dataclass
class AdministratorRequest:
    first_name: str
    second_name: str
    email_address: str
    password: str
    policies: list[str]
    birthday: date | None = None
    fiscal_code: str | None = None
    active: bool = True


@dataclass
class Returns:
    balance: str


@dataclass
class Order:
    ticker: str
    position: Position
    take_profit: float
    stop_loss: float
    volume_percentage: float
