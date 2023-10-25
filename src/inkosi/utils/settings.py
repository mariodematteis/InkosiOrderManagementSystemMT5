from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from omegaconf import OmegaConf


@dataclass
class MongoDBCollections:
    Log: str


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


@dataclass
class Settings:
    PostgreSQL: PostgreSQL
    MongoDB: MongoDB
    API: API

    DockerInstance: bool


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
