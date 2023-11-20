from enum import StrEnum


class EnhancedStrEnum(StrEnum):
    @classmethod
    def has(cls, key: str):
        return key in cls.__members__.values()

    @classmethod
    def list(cls):
        return list(cls.__members__.values())


class GeneralPolicies(EnhancedStrEnum):
    ACCESS_LOGIN: str = "ACCESS_LOGIN"


class AdministratorPolicies(EnhancedStrEnum):
    ADMINISTRATOR_ENDPOINTS: str = "ADMINISTRATOR_ENDPOINTS"
    OPERATIONS_ENDPOINTS: str = "OPERATIONS_ENDPOINTS"
    SCHEDULER_ENDPOINTS: str = "SCHEDULER_ENDPOINTS"
    DATABASE_TRADES_ENDPOINTS: str = "DATABASE_TRADES_ENDPOINTS"
    TRADING_ENDPOINTS: str = "TRADING_ENDPOINTS"
    PROFILE_ENDPOINTS: str = "PROFILE_ENDPOINTS"


class InvestorPolicies(EnhancedStrEnum):
    ADMINISTRATOR_ENDPOINTS: str = "ADMINISTRATOR_ENDPOINTS"
