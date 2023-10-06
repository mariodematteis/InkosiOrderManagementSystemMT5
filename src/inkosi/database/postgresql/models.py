from datetime import date

from sqlalchemy import ARRAY, Boolean, Column, Date, Float, Integer, String
from sqlalchemy.orm import relationship

from inkosi.database.postgresql.database import PostgreSQLInstance

instance = PostgreSQLInstance()


class Administrator(instance.base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    email_address = Column(String, unique=True, index=True, nullable=False)
    birthday: date = Column(Date, nullable=False)
    fiscal_code = Column(String, nullable=True)
    password = Column(String, nullable=False)
    policies = Column(ARRAY(String), nullable=False, default=[])
    active = Column(Boolean, nullable=False, default=True)

    investor_id = relationship("Investor", back_populates="id")


class Investor(instance.base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    email_address = Column(String, unique=True, index=True, nullable=False)
    birthday: date = Column(Date, nullable=False)
    fiscal_code = Column(String, nullable=True)
    password = Column(String, nullable=False)
    fund_deposit: float = Column(Float, nullable=False, default=0.0)
    policies: list = Column(ARRAY(String), nullable=False, default=[])
    active: bool = Column(Boolean, nullable=False, default=True)

    admiator_id = relationship("Admiator", back_populates="id")
