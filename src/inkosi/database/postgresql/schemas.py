from dataclasses import dataclass, field
from datetime import date, datetime

from inkosi.utils.utils import EnhancedStrEnum


class Tables(EnhancedStrEnum):
    """
    Enumeration of table names in the database.

    Attributes:
        ADMINISTRATOR (str): Table name for the 'administrator' table.
        INVESTOR (str): Table name for the 'investor' table.
        FUNDS (str): Table name for the 'funds' table.
        AUTHENTICATION (str): Table name for the 'authentication' table.
    """

    ADMINISTRATOR: str = "administrator"
    INVESTOR: str = "investor"
    FUNDS: str = "funds"
    AUTHENTICATION: str = "authentication"


class UserRole(EnhancedStrEnum):
    """
    Enumeration of user roles.

    Attributes:
        ADMINISTRATOR (str): Role for administrators.
        INVESTOR (str): Role for investors.
    """

    ADMINISTRATOR: str = "administrator"
    INVESTOR: str = "investor"


@dataclass
class PoliciesUpdate:
    """
    Dataclass representing a user's policies update.

    Attributes:
        user_id (int): The user's ID.
        role (str): The user's role.
        policies (Union[list[str], str]): The updated policies for the user.
    """

    user_id: int
    role: str
    policies: list[str] | str


@dataclass
class User:
    """
    Dataclass representing user information.

    Attributes:
        id (int): The user's ID.
        full_name (str): The user's full name.
        first_name (str): The user's first name.
        second_name (str): The user's second name.
        email_address (str): The user's email address.
        role (str): The user's role.
    """

    id: int
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    role: str


@dataclass
class AdministratorProfile:
    """
    Dataclass representing administrator profile information.

    Attributes:
        id (int): The administrator's ID.
        full_name (str): The administrator's full name.
        first_name (str): The administrator's first name.
        second_name (str): The administrator's second name.
        email_address (str): The administrator's email address.
        policies (list[str]): The administrator's policies.
        role (str): The administrator's role.
    """

    id: int
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    policies: list[str]
    role: str


@dataclass
class InvestorProfile:
    """
    Dataclass representing investor profile information.

    Attributes:
        id (int): The investor's ID.
        full_name (str): The investor's full name.
        first_name (str): The investor's first name.
        second_name (str): The investor's second name.
        email_address (str): The investor's email address.
        policies (list[str]): The investor's policies.
        role (str): The investor's role.
    """

    id: int
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    policies: list[str]
    role: str


@dataclass
class Fund:
    """
    Dataclass representing fund information.

    Attributes:
        id (str): The fund's ID.
        fund_name (str): The fund's name.
        investment_firm (str): The investment firm associated with the fund.
        created_at (date): The date when the fund was created.
        administrator (list[str]): The list of administrator IDs associated with the
        fund.
        investors (list[str]): The list of investor IDs associated with the fund.
        capital_distribution (dict): The capital distribution details for the fund.
        commission_type (str): The type of commission for the fund.
        commission_value (str): The commission value for the fund.
    """

    id: str
    fund_name: str
    investment_firm: str
    created_at: date
    administrator: list[str]
    investors: list[str]
    capital_distribution: dict
    commission_type: str
    commission_value: str


@dataclass
class AuthenticationOutput:
    """
    Dataclass representing authentication output.

    Attributes:
        id (str): The authentication record's ID.
        created_at (datetime): The date and time when the authentication record was
        created.
        validity (bool): The status indicating whether the authentication record is
        valid.
        user_id (str): The user's ID associated with the authentication record.
        ip_address (str): The IP address associated with the authentication record.
    """

    id: str
    created_at: datetime
    validity: bool
    user_id: str
    ip_address: str


@dataclass
class LoginCredentials:
    """
    Dataclass representing login credentials.

    Attributes:
        email_address (str): The user's email address for login.
        password (str): The user's password for login.
    """

    email_address: str
    password: str


@dataclass
class FundInformation:
    """
    Dataclass representing fund information.

    Attributes:
        id (int): The fund's ID.
        fund_name (str): The fund's name.
        created_at (date): The date when the fund was created.
        investment_firm (str): The investment firm associated with the fund.
        administrator (list[str]): The list of administrator IDs associated with the
        fund.
        investors (list[str]): The list of investor IDs associated with the fund.
        capital_distribution (dict): The capital distribution details for the fund.
        commission_type (str): The type of commission for the fund (default: "-").
        commission_value (str): The commission value for the fund (default: "-").
        strategies (list[str]): The list of strategies associated with the fund
        (default: []).
        fund_raising (bool): The status indicating whether the fund is raising funds
        (default: False).
    """

    id: int
    fund_name: str
    created_at: date
    investment_firm: str = ""
    administrator: list[str] = field(default_factory=[])
    investors: list[str] = field(default_factory=[])
    capital_distribution: dict = field(default_factory={})
    commission_type: str = "-"
    commission_value: str = "-"
    strategies: list[str] = field(default_factory=[])
    fund_raising: bool = False


@dataclass
class RaiseNewFund:
    """
    Dataclass representing information for raising a new fund.

    Attributes:
        fund_name (str): The name of the new fund.
        investment_firm (str | None): The investment firm associated with the new fund.
        commission_type (str): The type of commission for the new fund.
        commission_value (str): The commission value for the new fund.
        administrators (list[int]): The list of administrator IDs associated with the
        new fund.
        investors (list[str]): The list of investor IDs associated with the new fund
        (default: []).
        capital_distribution (dict): The capital distribution details for the new fund
        (default: {}).
        created_at (date): The date when the new fund is created
        (default: datetime.today()).
    """

    fund_name: str
    investment_firm: str | None
    commission_type: str
    commission_value: str
    administrators: list[int]
    investors: list[str] = field(default_factory=[])
    capital_distribution: dict = field(default_factory={})
    created_at: date = field(default=datetime.today())


@dataclass
class AddInvestorToFund:
    """
    Dataclass representing information for adding an investor to a fund.

    Attributes:
        investor_id (int): The ID of the investor to be added.
        fund (str | int): The fund's name or ID to which the investor will be added.
    """

    investor_id: int
    fund: str | int


@dataclass
class AddAdministratorToFund:
    """
    Dataclass representing information for adding an administrator to a fund.

    Attributes:
        administrator_id (int): The ID of the administrator to be added.
        fund (str | int): The fund's name or ID to which the administrator will be
        added.
    """

    administrator_id: int
    fund: str | int


@dataclass
class Commission:
    """
    Dataclass representing commission information.

    Attributes:
        commission_type (str): The type of commission.
        commission_value (float | int): The commission value.
        fund (str | int): The fund's name or ID associated with the commission.
    """

    commission_type: str
    commission_value: float | int
    fund: str | int
