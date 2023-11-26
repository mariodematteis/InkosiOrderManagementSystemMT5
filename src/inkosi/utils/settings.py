from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache
from pathlib import Path

from omegaconf import OmegaConf
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="INKOSI_",
        case_sensitive=False,
    )

    ACCOUNT: int
    PASSWORD: str
    SERVER: str


@dataclass
class TimeActivity:
    days: int
    hours: int
    minutes: int
    seconds: int


@dataclass
class MongoDBCollections:
    Log: str
    Trade: str


@dataclass
class PostgreSQL:
    PROTOCOL: str
    USERNAME: str
    PASSWORD: str
    HOSTNAME: str
    PORT: int
    DATABASE: str
    SCHEMA: str
    PARAMETERS: str


@dataclass
class MongoDB:
    PROTOCOL: str
    USERNAME: str
    PASSWORD: str
    HOSTNAME: str
    PORT: int
    DATABASE: str
    PARAMETERS: str
    TLS: bool

    COLLECTIONS: MongoDBCollections


@dataclass
class API:
    AllowedIPAddresses: str | list
    TokenAuthentication: bool
    IPAddressCorrespondence: bool
    TimeActivity: TimeActivity
    APIs: list


@dataclass
class Policies:
    Administrator: list[str]
    Investor: list[str]


@dataclass
class RiskManagement:
    Models: list | None


@dataclass
class TechnicalIndicators:
    MovingAveragePeriod: int | float


@dataclass
class Settings:
    PostgreSQL: PostgreSQL
    MongoDB: MongoDB
    API: API
    Policies: Policies
    RiskManagement: RiskManagement
    TechnicalIndicators: TechnicalIndicators

    DefaultAdministrators: dict[int, dict[str, str | date | list | None]] = field(
        default_factory=dict
    )
    DefaultInvestors: list[dict[str, str | date | list | None]] = field(
        default_factory=list
    )


@lru_cache
def get_environmental_settings() -> EnvSettings:
    return EnvSettings()


@lru_cache
def get_settings() -> Settings:
    settings_import = OmegaConf.load(
        Path(__file__)
        .absolute()
        .parent.parent.parent.parent.joinpath(
            "config.yaml",
        ),
    )

    return OmegaConf.structured(
        Settings(**settings_import),
    )


@lru_cache
def get_postgresql_settings() -> PostgreSQL:
    return get_settings().PostgreSQL


@lru_cache
def get_postgresql_schema() -> str:
    return get_postgresql_settings().SCHEMA


@lru_cache
def get_postgresql_url() -> str:
    postgresql_settings: PostgreSQL = get_settings().PostgreSQL

    return (
        f"{postgresql_settings.PROTOCOL}://"
        f"{postgresql_settings.USERNAME}:"
        f"{postgresql_settings.PASSWORD}@"
        f"{postgresql_settings.HOSTNAME}:"
        f"{postgresql_settings.PORT}/{postgresql_settings.DATABASE}"
    )


@lru_cache
def get_mongodb_settings() -> MongoDB:
    return get_settings().MongoDB


@lru_cache
def get_mongodb_collection() -> MongoDBCollections:
    return get_mongodb_settings().COLLECTIONS


@lru_cache
def get_mongodb_url() -> str:
    mongodb_settings = get_settings().MongoDB

    return (
        f"{mongodb_settings.PROTOCOL}://"
        f"{mongodb_settings.USERNAME}:"
        f"{mongodb_settings.PASSWORD}@"
        f"{mongodb_settings.HOSTNAME}:"
        f"{mongodb_settings.PORT}/"
        f"{mongodb_settings.PARAMETERS}"
    )


@lru_cache
def get_api_settings() -> API:
    return get_settings().API


@lru_cache
def get_allowed_ip_addresses() -> list | str:
    return get_api_settings().AllowedIPAddresses


@lru_cache
def get_ip_address_correspondence() -> bool:
    return get_api_settings().IPAddressCorrespondence


@lru_cache
def get_time_activity() -> dict:
    return get_api_settings().TimeActivity


@lru_cache
def get_administrators_policies() -> list:
    return get_settings().Policies.Administrator


@lru_cache
def get_investors_policies() -> list:
    return get_settings().Policies.Investor


@lru_cache
def get_risk_management() -> RiskManagement:
    return get_settings().RiskManagement


@lru_cache
def get_risk_management_models() -> list | None:
    return get_risk_management().Models


@lru_cache
def get_technical_indicators_values() -> TechnicalIndicators:
    return get_settings().TechnicalIndicators


@lru_cache
def get_default_administrators() -> dict[int, dict[str, str | date | list | None]]:
    return get_settings().DefaultAdministrators


@lru_cache
def get_default_investors() -> list[dict[str, str | date | list | None]]:
    return get_settings().DefaultInvestors
