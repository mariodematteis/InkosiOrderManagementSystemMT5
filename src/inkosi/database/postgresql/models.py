import random
from datetime import date, datetime
from functools import lru_cache

from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Float, Integer, String
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
    investment_firm: str = Column(String, nullable=True)
    administrators: list[int] = Column(ARRAY(Integer), default=[])
    investors: list[int] = Column(ARRAY(Integer), default=[])
    capital_distribution: dict = Column(JSONB, default={})
    commission_type: str = Column(String, default="percentual")
    commission_value: str = Column(Float, default=0.0)
    risk_limits: bool = Column(Boolean, default=False)


class Authentication(get_instance().base):
    __tablename__ = "authentication"

    id: int = Column(
        String,
        primary_key=True,
        index=True,
        nullable=False,
    )

    created_at: datetime = Column(
        DateTime,
        default=datetime.now(),
        nullable=False,
    )
    validity: bool = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    user_type: str = Column(String, nullable=False)
    user_id: int = Column(Integer, nullable=False)
    mode: str = Column(String, nullable=False)
    ip_address: str = Column(String, nullable=True)
