import random
from datetime import date, datetime
from functools import lru_cache

from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from inkosi.database.postgresql.database import PostgreSQLInstance


@lru_cache
def get_instance() -> PostgreSQLInstance:
    """
    Get a cached instance of the PostgreSQLInstance.

    Returns:
        PostgreSQLInstance: The cached instance of the PostgreSQL database.

    Note:
        This function is decorated with the LRU (Least Recently Used) cache,
        which helps in caching the result of the function to improve performance.
        It returns a cached instance of the `PostgreSQLInstance` class.
    """

    return PostgreSQLInstance()


class Administrator(get_instance().base):
    """
    SQLAlchemy model representing the 'administrators' table in the PostgreSQL database.

    Attributes:
        id (int): The unique identifier for the administrator.
        first_name (str): The first name of the administrator.
        second_name (str): The second name of the administrator.
        email_address (str): The email address of the administrator (unique).
        birthday (date): The birthday of the administrator.
        fiscal_code (str): The fiscal code of the administrator.
        password (str): The password of the administrator.
        policies (list): The list of policies associated with the administrator.
        active (bool): The status indicating whether the administrator is active.

    Note:
        This class is an SQLAlchemy model representing the 'administrators' table in
        the PostgreSQL database.
    """

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
    """
    SQLAlchemy model representing the 'investors' table in the PostgreSQL database.

    Attributes:
        id (int): The unique identifier for the investor.
        first_name (str): The first name of the investor.
        second_name (str): The second name of the investor.
        email_address (str): The email address of the investor (unique).
        birthday (date): The birthday of the investor.
        fiscal_code (str): The fiscal code of the investor.
        password (str): The password of the investor.
        policies (list): The list of policies associated with the investor.
        active (bool): The status indicating whether the investor is active.

    Note:
        This class is an SQLAlchemy model representing the 'investors' table in the
        PostgreSQL database.
    """

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
    """
    SQLAlchemy model representing the 'funds' table in the PostgreSQL database.

    Attributes:
        id (int): The unique identifier for the fund.
        fund_name (str): The name of the fund (unique).
        investment_firm (str): The name of the investment firm associated with the fund.
        created_at (date): The date when the fund was created.
        administrators (list[int]): The list of administrator IDs associated with the
        fund.
        investors (list[int]): The list of investor IDs associated with the fund.
        capital_distribution (dict): The capital distribution details for the fund.
        commission_type (str): The type of commission for the fund
        (default: 'percentual').
        commission_value (float): The commission value for the fund (default: 0.0).
        risk_limits (bool): The status indicating whether the fund has risk limits
        (default: False).
        raising_funds (bool): The status indicating whether the fund is raising funds
        (default: True).

    Note:
        This class is an SQLAlchemy model representing the 'funds' table in the
        PostgreSQL database.
    """

    __tablename__ = "funds"

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        default=random.randint(10000000, 99999999),
    )
    fund_name: str = Column(String, nullable=False, unique=True)
    investment_firm: str = Column(String, nullable=True)
    created_at: date = Column(Date, nullable=False)
    administrators: list[int] = Column(ARRAY(Integer), default=[])
    investors: list[int] = Column(ARRAY(Integer), default=[])
    capital_distribution: dict = Column(JSONB, default={})
    commission_type: str = Column(String, default="percentual")
    commission_value: str = Column(Float, default=0.0)
    risk_limits: bool = Column(Boolean, default=False)
    raising_funds: bool = Column(Boolean, default=True)


class Authentication(get_instance().base):
    """
    SQLAlchemy model representing the 'authentication' table in the PostgreSQL database.

    Attributes:
        id (str): The unique identifier for the authentication record.
        created_at (datetime): The date and time when the authentication record was
        created.
        validity (bool): The status indicating whether the authentication record is
        valid (default: True).
        user_type (str): The type of user associated with the authentication record.
        user_id (int): The user ID associated with the authentication record.
        mode (str): The authentication mode (e.g., login, logout).
        ip_address (str): The IP address associated with the authentication record
        (nullable).

    Note:
        This class is an SQLAlchemy model representing the 'authentication' table in
        the PostgreSQL database.
    """

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
