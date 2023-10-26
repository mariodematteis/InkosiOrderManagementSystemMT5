import random
import string
from datetime import date
from functools import lru_cache

from sqlalchemy import ARRAY, Boolean, Column, Date, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from inkosi.database.postgresql.database import PostgreSQLInstance


@lru_cache
def get_instance() -> PostgreSQLInstance:
    return PostgreSQLInstance()


class Administrator(get_instance().base):
    __tablename__ = "administrators"

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        default=random.randint(10000000, 49999999),
    )
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    email_address: str = Column(String, nullable=False, unique=True)
    birthday: date = Column(Date, nullable=True)
    fiscal_code: str = Column(String, nullable=True)
    password: str = Column(String, nullable=False)
    policies: list = Column(ARRAY(String), default=[])
    active: bool = Column(Boolean, default=True)


class Investor(get_instance().base):
    __tablename__ = "investors"

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        default=random.randint(50000000, 99999999),
    )
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    email_address: str = Column(String, unique=True, nullable=False)
    birthday: date = Column(Date, nullable=False)
    fiscal_code: str = Column(String, nullable=True)
    password: str = Column(String, nullable=False)
    fund_deposit: float = Column(Float, default=0.0)
    policies: list = Column(ARRAY(String), default=[])
    active: bool = Column(Boolean, default=True)


class Funds(get_instance().base):
    __tablename__ = "funds"

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        default=random.randint(10000000, 99999999),
    )
    fund_name: str = Column(String, nullable=False, unique=True)
    investment_firm: list[int] = Column(ARRAY(String), default=[])
    administrator: list[int] = Column(ARRAY(Integer), default=[])
    investors: list[int] = Column(ARRAY(Integer), default=[])
    capital_distribution: dict = Column(JSONB, default={})
    commission_type: str = Column(String, default="percentual")
    commission_value: str = Column(Float, default=0.0)


class Orders(get_instance().base):
    __tablename__ = "orders"

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        default=lambda n: "".join(
            [
                random.choice(list(set(string.ascii_uppercase).union(string.digits)))
                for i in range(n)
            ]
        ),
    )
    volume: float = Column(Float, nullable=False)
    investors: dict = Column(JSONB, default={})
    returns: float = Column(Float, default=0.0)
    commission_broker: float = Column(Float, default=0.0)
    commission_fund: float = Column(Float, default=0.0)
    fund: str = Column(Float, nullable=False)
