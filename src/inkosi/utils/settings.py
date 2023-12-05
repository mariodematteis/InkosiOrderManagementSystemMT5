from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from omegaconf import OmegaConf
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    """
    Settings class for MetaTrader 5 (MT5) account access.

    This class inherits from BaseSettings and includes configuration options
    for specifying the environment file, environment variable prefix, and
    case sensitivity for settings.

    Parameters
    ----------
    ACCOUNT: int
        MetaTrader 5 account number.
    PASSWORD: str
        Password for the MetaTrader 5 account.
    SERVER: str
        MetaTrader 5 server name.

    Notes
    -----
        The settings ACCOUNT, PASSWORD, and SERVER correspond to MetaTrader 5
        account information.
    """

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
    """
    Data class representing the maximum amount of time before the generated
    token for access expires.

    Parameters
    ----------
    days: int
        Number of days until token expiration.
    hours: int
        Number of hours until token expiration.
    minutes: int
        Number of minutes until token expiration.
    seconds: int
        Number of seconds until token expiration.

    Notes
    -----
        This class is designed to hold information about the time duration
        before an access token expires. It is commonly used in login scenarios.
    """

    days: int
    hours: int
    minutes: int
    seconds: int


@dataclass
class MongoDBCollections:
    """
    Data class representing the MongoDB Collections used respectively for Logs and
    Trading Operations.
    """

    Log: str
    Trade: str


@dataclass
class PostgreSQL:
    """
    Data class representing the configuration details for connecting to a PostgreSQL
    database.

    Parameters
    ----------
    PROTOCOL: str
        Protocol used for the connection, generally "postgresql"
    USERNAME: str
        Username for authenticating the database connection.
    PASSWORD: str
        Password for authenticating the database connection.
    HOSTNAME: str
        Hostname or IP address of the PostgreSQL server.
    PORT: str
        Port number on which the PostgreSQL server is listening.
    DATABASE: str
        Name of the PostgreSQL database to connect to.
    SCHEMA: str
        Name of the database schema to use.
    PARAMETERS: str
        Additional connection parameters as a string.
    """

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
    """
    Data class representing the configuration details for connecting to a MongoDB
    database.

    Parameters
    ----------
    PROTOCOL: str
        Protocol used for the connection (e.g., "mongodb" or "mongodb+srv").
    USERNAME: str
        Username for authenticating the MongoDB connection.
    PASSWORD: str
        Password for authenticating the MongoDB connection.
    HOSTNAME: str
        Hostname or IP address of the MongoDB server.
    PORT: int
        Port number on which the MongoDB server is listening.
    DATABASE: str
        Name of the MongoDB database to connect to.
    PARAMETERS: str
        Additional connection parameters as a string.
    TLS: bool
        Flag indicating whether to use TLS/SSL for the connection.
    COLLECTIONS: MongoDBCollections
        An instance of the MongoDBCollections class, representing the collections within
        the MongoDB database.
    """

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
    """
    Data class representing the configuration details for an API.

    Parameters
    ----------
    AllowedIPAddresses: str | list
        Allowed IP addresses for API access. This can be a single IP address (string)
        or a list of IP addresses.
    TokenAuthentication: bool
        Flag indicating whether token authentication is required.
    IPAddressCorrespondence: bool
        Flag indicating whether IP address correspondence is checked.
    TimeActivity: TimeActivity
        An instance of the TimeActivity class representing the maximum amount of time
        before the generated token for access expires.
    APIs: list
        List of APIs associated with the configuration.
    """

    AllowedIPAddresses: str | list
    TokenAuthentication: bool
    IPAddressCorrespondence: bool
    TimeActivity: TimeActivity
    APIs: list


@dataclass
class Policies:
    """
    Data class representing access policies for different user roles.

    Parameters
    ----------
    Administrator: list[str]
        List of policies for users with the Administrator role.
    Investor: list[str]
        List of policies for users with the Investor role.

    Notes
    -----
    To the state of art, for the A
    """

    Administrator: list[str]
    Investor: list[str]


@dataclass
class RiskManagement:
    """
    Data class representing risk management configuration.

    Parameters
    ----------
    Models: list | None
        List of risk management models. If None, no specific risk management models are
        defined.
    """

    Models: list | None


@dataclass
class TechnicalIndicators:
    """
    Data class representing configuration for technical indicators.

    Parameters
    ----------
    MovingAveragePeriod: int | float
        Period for the moving average. This can be an integer or a float value.
    """

    MovingAveragePeriod: int | float


@dataclass
class Settings:
    """
    Data class representing a configuration settings bundle.

    Parameters
    ----------
    PostgreSQL: PostgreSQL
        Configuration settings for connecting to a PostgreSQL database.
    MongoDB: MongoDB
        Configuration settings for connecting to a MongoDB database.
    API: API
        Configuration settings for an API.
    Policies: Policies
        Access policies for different user roles.
    RiskManagement: RiskManagement
        Configuration settings for risk management.
    TechnicalIndicators: TechnicalIndicators
        Configuration for technical indicators.
    DockerInstance: bool
        Flag indicating whether the application is running in a Docker instance.
    """

    PostgreSQL: PostgreSQL
    MongoDB: MongoDB
    API: API
    Policies: Policies
    RiskManagement: RiskManagement
    TechnicalIndicators: TechnicalIndicators

    DockerInstance: bool


@lru_cache
def get_environmental_settings() -> EnvSettings:
    """
    Function to fetch environmental settings using caching.

    Returns
    -------
    EnvSettings
        An instance of the EnvSettings class representing the environmental
        configuration settings.
    """

    return EnvSettings()


@lru_cache
def get_settings() -> Settings:
    """
    Function to fetch application settings using caching.

    Returns
    -------
    Settings
        An instance of the Settings class representing the overall configuration
        settings for the application.
    """

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
    """
    Function to fetch PostgreSQL settings using caching.

    Returns
    -------
    PostgreSQL
        An instance of the PostgreSQL class representing the overall configuration
        settings for the PostgreSQL Instance.
    """

    return get_settings().PostgreSQL


@lru_cache
def get_postgresql_schema() -> str:
    """
    Function to fetch PostgreSQL Schema settings using caching.

    Returns
    -------
    Settings
        An instance of the Settings class representing the overall configuration
        settings for the application.
    """

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
