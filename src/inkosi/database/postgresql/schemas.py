from dataclasses import dataclass, field
from datetime import date, datetime

from inkosi.utils.utils import CommissionTypes, EnhancedStrEnum


class Tables(EnhancedStrEnum):
    ADMINISTRATOR: str = "administrators"
    INVESTOR: str = "investors"
    FUNDS: str = "funds"
    AUTHENTICATION: str = "authentication"
    STRATEGIES: str = "strategies"


class UserRole(EnhancedStrEnum):
    ADMINISTRATOR: str = "administrator"
    INVESTOR: str = "investor"


class CategoriesATS(EnhancedStrEnum):
    GENERAL_PURPOSE: str = "general_purpose"
    TECHNICAL: str = "technical_indicators"


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
    policies: list[str]


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
class InvestorProfile:
    id: int
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    policies: list[str]
    role: str


@dataclass
class ATSProfile:
    id: int
    full_name: str
    administrator_id: int
    fund_names: list
    category: str


@dataclass
class Fund:
    id: int
    fund_name: str
    investment_firm: str
    created_at: date
    administrators: list[int]
    investors: list[int]
    capital_distribution: dict[str, float]
    commission_type: str
    commission_value: float
    risk_limits: bool
    raising_funds: bool


@dataclass
class AuthenticationOutput:
    id: str
    created_at: datetime
    validity: bool
    user_id: str
    ip_address: str


@dataclass
class LoginCredentials:
    email_address: str
    password: str


@dataclass
class FundInformation:
    id: int
    fund_name: str
    created_at: date | str
    investment_firm: str | None = None
    administrators: list[int] = field(default_factory=[])
    administrators_full_name: list[str] = field(default_factory=[])
    investors: list[int] = field(default_factory=[])
    investors_full_name: list[str] = field(default_factory=[])
    capital_distribution: dict = field(default_factory={})
    commission_type: str = field(default_factory=str)
    commission_value: float = field(default=0.0)
    strategies: list[str] | str = field(default_factory=[])
    raising_funds: bool = field(default=False)


@dataclass
class RaiseNewFund:
    fund_name: str
    investment_firm: str | None
    commission_type: CommissionTypes
    commission_value: float
    administrators: list[int]
    investors: list[str] = field(default_factory=list)
    capital_distribution: dict = field(default_factory=dict)
    created_at: date = field(default=datetime.today())


@dataclass
class AddInvestorToFund:
    investor_id: int | None
    fund: str | int


@dataclass
class AddAdministratorToFund:
    administrator_id: int | None
    fund: str | int


@dataclass
class Commission:
    commission_type: str
    commission_value: float | int
    fund: str | int


@dataclass
class DepositFundRequest:
    investor_id: int
    deposit: float
    fund_name: str
