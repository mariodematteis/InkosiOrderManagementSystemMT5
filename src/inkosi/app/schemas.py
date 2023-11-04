from dataclasses import dataclass
from datetime import date

from inkosi.utils.utils import EnhancedStrEnum


class Mode(EnhancedStrEnum):
    BACKTEST: str = "backtesting"
    WEBAPP: str = "webapp"


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
