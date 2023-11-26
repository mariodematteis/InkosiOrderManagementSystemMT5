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
    ADMINISTRATOR_IFM_FULL_ACCESS: str = "ADMINISTRATOR_IFM_FULL_ACCESS"
    ADMINISTRATOR_FM_FULL_ACCESS: str = "ADMINISTRATOR_FM_FULL_ACCESS"
    ADMINISTRATOR_PM_FULL_ACCESS: str = "ADMINISTRATOR_PM_FULL_ACCESS"


class InvestorPolicies(EnhancedStrEnum):
    INVESTOR_DASHBOARD_VISUALISATION: str = "INVESTOR_DASHBOARD_VISUALISATION"
    INVESTOR_SAMPLING_SCENARIOS: str = "INVESTOR_SAMPLING_SCENARIOS"
    INVESTOR_BACKTEST_ALL: str = "INVESTOR_BACKTEST_ALL"


class CommissionTypes(EnhancedStrEnum):
    PERCENTUAL_TYPE: str = "percentual"
    ABSOLUTE_TYPE: str = "absolute"
