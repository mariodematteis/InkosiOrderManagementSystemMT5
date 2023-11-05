from dataclasses import dataclass, field
from datetime import datetime

from inkosi.utils.utils import EnhancedStrEnum


class Tables(EnhancedStrEnum):
    ADMINISTRATOR: str = "administrator"
    INVESTOR: str = "investor"
    FUNDS: str = "funds"
    AUTHENTICATION: str = "authentication"


class UserRole(EnhancedStrEnum):
    ADMINISTRATOR: str = "administrator"
    INVESTOR: str = "investor"


@dataclass
class PoliciesUpdate:
    user_id: int
    role: str
    policies: list[str] | str


@dataclass
class User:
    id: int
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    role: str


@dataclass
class AdministratorProfile:
    id: int
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    policies: list[str]
    role: str


@dataclass
class Fund:
    id: str
    fund_name: str
    portfolio_managers: list[str]
    investors: list[str]


@dataclass
class AuthenticationOutput:
    id: str
    created_at: datetime
    validity: bool
    user_id: str
    ip_address: str


@dataclass
class ReturnRequest:
    fund_name: str


@dataclass
class LoginCredentials:
    email_address: str
    password: str


@dataclass
class FundInformation:
    investment_firm: str
    fund_name: str
    administrators: list[str]
    investors: list[str]
    strategies: list[str]
    capital_distribution: dict
    commission_type: str
    commission_value: str


@dataclass
class RaiseNewFund:
    fund_name: str
    investment_firm: str | None
    commission_type: str
    commission_value: str
    administrators: list[int]
    investors: list[str] = field(default_factory=[])
    capital_distribution: dict = field(default_factory={})


@dataclass
class AddInvestorToFund:
    investor_id: int
    fund: str | int


@dataclass
class AddAdministratorToFund:
    administrator_id: int
    fund: str | int


@dataclass
class Commission:
    commission_type: str
    commission_value: float | int
    fund: str | int
