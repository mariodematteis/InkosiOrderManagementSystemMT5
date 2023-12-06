from enum import StrEnum


class EnhancedStrEnum(StrEnum):
    """
    Enhanced string enumeration class.

    This class extends the functionality of the `StrEnum` class by providing additional
    methods.

    Methods:
        - has(cls, key: str) -> bool:
            Check if a specific key exists in the enumeration.

        - list(cls) -> List[str]:
            Get a list of all values in the enumeration.

    Note:
        This class serves as a base class for string enumerations with added
        functionality.
    """

    @classmethod
    def has(
        cls,
        key: str,
    ) -> bool:
        return key in cls.__members__.values()

    @classmethod
    def list(cls) -> list[str]:
        return list(cls.__members__.values())


class GeneralPolicies(EnhancedStrEnum):
    """
    Enumeration representing general policies.

    Attributes:
        ACCESS_LOGIN (str): General policy related to access login.
    """

    ACCESS_LOGIN: str = "ACCESS_LOGIN"


class AdministratorPolicies(EnhancedStrEnum):
    """
    Enumeration representing administrator policies.

    Attributes:
        ADMINISTRATOR_ENDPOINTS (str): Policy related to administrator endpoints.
        OPERATIONS_ENDPOINTS (str): Policy related to operations endpoints.
        SCHEDULER_ENDPOINTS (str): Policy related to scheduler endpoints.
        DATABASE_TRADES_ENDPOINTS (str): Policy related to database trades endpoints.
        TRADING_ENDPOINTS (str): Policy related to trading endpoints.
        PROFILE_ENDPOINTS (str): Policy related to profile endpoints.
    """

    ADMINISTRATOR_ENDPOINTS: str = "ADMINISTRATOR_ENDPOINTS"
    OPERATIONS_ENDPOINTS: str = "OPERATIONS_ENDPOINTS"
    SCHEDULER_ENDPOINTS: str = "SCHEDULER_ENDPOINTS"
    DATABASE_TRADES_ENDPOINTS: str = "DATABASE_TRADES_ENDPOINTS"
    TRADING_ENDPOINTS: str = "TRADING_ENDPOINTS"
    PROFILE_ENDPOINTS: str = "PROFILE_ENDPOINTS"


class InvestorPolicies(EnhancedStrEnum):
    """
    Enumeration representing investor policies.

    Attributes:
        ADMINISTRATOR_ENDPOINTS (str): Policy related to administrator endpoints.
    """

    ADMINISTRATOR_ENDPOINTS: str = "ADMINISTRATOR_ENDPOINTS"
