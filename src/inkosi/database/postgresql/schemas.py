from dataclasses import dataclass

from inkosi.utils.utils import EnhancedStrEnum


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
class ReturnRequest:
    fund_name: str


@dataclass
class LoginCredentials:
    email_address: str
    password: str
