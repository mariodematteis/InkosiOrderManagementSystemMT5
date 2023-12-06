from dataclasses import dataclass, field

from inkosi.utils.utils import EnhancedStrEnum


class Templates(EnhancedStrEnum):
    """
    Enumeration representing different email templates.

    Attributes:
        NEW_ADMINISTRATOR (str): Email template for notifying about a new administrator.
        NEW_FUND (str): Email template for notifying about a new fund.

    Note:
        This enumeration defines different email templates as class attributes.
        Each attribute represents a specific template with a descriptive name.
    """

    NEW_ADMINISTRATOR: str = "new_administrator"
    NEW_FUND: str = "new_fund"


@dataclass
class NewFund:
    """
    Data class representing information about a new fund.

    Attributes:
        fund_name (str): The name of the new fund.

    Note:
        This data class is decorated with the `@dataclass` decorator and represents
        information about a new fund. It includes an attribute to store the name of the
        new fund.
    """

    fund_name: str


@dataclass
class EmailReceivedAdministratorFundRaising:
    """
    Data class representing the receipt status of fundraising emails by administrators.

    Attributes:
        administrator_received (list[str]): List of administrators who received the
        email.
        administrator_not_received (dict[str, str]): Dictionary of administrators who
        did not receive the email,
        with reasons specified as values.
    """

    administrator_received: list[str]
    administrator_not_received: dict[str, str] = field(default_factory={})
