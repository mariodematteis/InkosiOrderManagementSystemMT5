import random
from dataclasses import dataclass
from datetime import date
from functools import lru_cache

from sqlalchemy import ARRAY, Boolean, Column, Date, Float, Integer, String

from inkosi.database.postgresql.database import PostgreSQLInstance


@lru_cache
def get_instance() -> PostgreSQLInstance:
    return PostgreSQLInstance()


class Administrator(get_instance().base):
    __tablename__ = "administrators"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        default=random.randint(10000000, 99999999),
    )
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    email_address = Column(String, nullable=False, unique=True)
    birthday: date = Column(Date, nullable=True)
    fiscal_code = Column(String, nullable=True)
    password = Column(String, nullable=False)
    policies = Column(ARRAY(String), default=[])
    active = Column(Boolean, default=True)


class Investor(get_instance().base):
    __tablename__ = "investors"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        default=random.randint(10000000, 99999999),
    )
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    email_address = Column(String, unique=True, nullable=False)
    birthday: date = Column(Date, nullable=False)
    fiscal_code = Column(String, nullable=True)
    password = Column(String, nullable=False)
    fund_deposit: float = Column(Float, default=0.0)
    policies: list = Column(ARRAY(String), default=[])
    active: bool = Column(Boolean, default=True)


@dataclass
class Users:
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    policies: list[str]
    active: bool


@dataclass
class PortfolioManager:
    full_name: str
    first_name: str
    second_name: str
    email_address: str
    policies: list[str]


@dataclass
class LoginCredentials:
    EmailAddress: str
    Password: str
