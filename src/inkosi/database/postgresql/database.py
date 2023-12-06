from datetime import datetime, timedelta
from hashlib import sha256

from beartype import beartype
from beartype.typing import Any, Iterable
from sqlalchemy import Engine, MetaData, TextClause, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

from inkosi.log.log import Logger
from inkosi.utils.exceptions import PostgreSQLConnectionError
from inkosi.utils.settings import (
    get_administrators_policies,
    get_investors_policies,
    get_ip_address_correspondence,
    get_postgresql_schema,
    get_postgresql_url,
    get_time_activity,
)

from .schemas import (
    AdministratorProfile,
    AuthenticationOutput,
    Commission,
    Fund,
    FundInformation,
    PoliciesUpdate,
    Tables,
    User,
    UserRole,
)

logger = Logger(
    module_name="PostgreSQLDatabase", package_name="postgresql", database=False
)


class DatabaseInstanceSingleton(
    type,
):
    """
    Metaclass implementing the Singleton pattern for a database instance.

    Attributes:
        _instance: The singleton instance of the class.

    Methods:
        __call__(cls, *args, **kwargs):
            Override the call method to implement the Singleton pattern.

    Note:
        This metaclass ensures that only one instance of the class is created,
        following the Singleton pattern.
    """

    _instance = None

    def __call__(
        cls,
        *args,
        **kwargs,
    ):
        """
        Override the call method to implement the Singleton pattern.

        Parameters:
            cls: The class.
            *args: Variable arguments.
            **kwargs: Keyword arguments.

        Returns:
            The singleton instance of the class.
        """

        if not cls._instance:
            cls._instance = super(
                type(
                    cls,
                ),
                cls,
            ).__call__(
                *args,
                **kwargs,
            )

        return cls._instance


class PostgreSQLInstance(metaclass=DatabaseInstanceSingleton):
    """
    Singleton class representing a PostgreSQL database instance.

    Attributes:
        engine (Engine): The SQLAlchemy database engine.
        metadata (MetaData): The SQLAlchemy metadata object.
        base (declarative_base): The SQLAlchemy declarative base.

    Methods:
        __init__(self): Initialize the PostgreSQL instance.
        connect(self): Connect to the PostgreSQL instance.
        add(self, model: Iterable[declarative_base()] | declarative_base()) -> bool:
            Add records to the database.
        select(self, query: TextClause | str) -> list[Any]:
            Execute a select query on the database.
        update(self, query: TextClause | str) -> bool:
            Execute an update query on the database.

    Note:
        This class represents a singleton PostgreSQL database instance. It provides
        methods for connecting to the database, adding records, executing select
        queries, and executing update queries.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the PostgreSQL instance.

        Raises:
            PostgreSQLConnectionError: If unable to establish a connection with the
            PostgreSQL instance.
        """

        self.engine: Engine = create_engine(
            get_postgresql_url(),
        )

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        __session = sessionmaker(bind=self.engine)
        with __session() as session:
            session.execute(
                CreateSchema(
                    name=get_postgresql_schema(),
                    if_not_exists=True,
                )
            )
            session.commit()

        self.metadata = MetaData(schema=get_postgresql_schema())

        self.base = declarative_base(metadata=self.metadata)

    def connect(
        self,
    ) -> None:
        """
        Connect to the PostgreSQL instance.

        Raises:
            PostgreSQLConnectionError: If unable to establish a connection with the
            PostgreSQL instance.
        """

        try:
            self.base.metadata.create_all(bind=self.engine)
        except Exception:
            logger.error(message="Unable to establish with the PostgreSQL Instance")
            raise PostgreSQLConnectionError

    @beartype
    def add(
        self,
        model: Iterable[declarative_base()] | declarative_base(),
    ) -> bool:
        """
        Add records to the database.

        Parameters:
            model (Iterable[declarative_base()] | declarative_base()): The model or
            iterable of models to add.

        Returns:
            bool: True if the addition is successful, False otherwise.
        """

        __session = sessionmaker(bind=self.engine)
        with __session() as session:
            try:
                if isinstance(model, Iterable):
                    session.add_all(model)
                else:
                    session.add(model)

                session.commit()
                session.close()
            except Exception as error:
                logger.error(
                    "Unable to add the specified records to the database. Error"
                    f" occurred: {error}"
                )
                return False
            else:
                return True

    @beartype
    def select(
        self,
        query: TextClause | str,
    ) -> list[Any]:
        """
        Execute a select query on the database.

        Parameters:
            query (TextClause | str): The select query.

        Returns:
            list[Any]: The result of the select query.
        """

        __session = sessionmaker(bind=self.engine)
        with __session() as session:
            __query = session.execute(
                query if isinstance(query, TextClause) else text(query)
            )
            result = __query.all()
            session.close()
            return result

    @beartype
    def update(
        self,
        query: TextClause | str,
    ) -> bool:
        """
        Execute an update query on the database.

        Parameters:
            query (TextClause | str): The update query.

        Returns:
            bool: True if the update is successful, False otherwise.
        """

        __session = sessionmaker(bind=self.engine)
        with __session() as session:
            try:
                session.execute(query if isinstance(query, TextClause) else text(query))
                session.commit()
                session.close()
            except Exception as error:
                logger.error(
                    f"Unable to update records on the database. Error occurred: {error}"
                )
                return False
            else:
                return True


class PostgreSQLCrud:
    def __init__(self) -> None:
        self.postgresql_instance = PostgreSQLInstance()

    def valid_authentication(
        self,
        token_id: str,
        ip_address: str | None = None,
    ) -> bool:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id, created_at,"
            " validity, user_id, ip_address FROM authentication WHERE id ="
            f" '{token_id}' AND mode = 'webapp';"
        )

        if get_ip_address_correspondence():
            __query += (
                " AND ip_address ="
                f" '{ip_address if isinstance(ip_address, str) else ''}';"
            )

        result = [
            AuthenticationOutput(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

        match len(result):
            case 1:
                row = result[0]
                created_at = row.created_at
                if datetime.now() <= created_at + timedelta(**get_time_activity()):
                    self.postgresql_instance.update(
                        f"SET search_path TO {get_postgresql_schema()}; DELETE FROM"
                        f" {Tables.AUTHENTICATION} WHERE id <> '{token_id}' AND user_id"
                        f" = '{row.user_id}';"
                    )
                    return True
                else:
                    self.postgresql_instance.update(
                        f"SET search_path TO {get_postgresql_schema()}; DELETE FROM"
                        f" {Tables.AUTHENTICATION} WHERE id = '{token_id}';"
                    )

        return False

    def valid_backtesting_token(
        self,
        token_id: str,
        ip_address: str | None = None,
    ) -> bool:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id, created_at,"
            " validity, user_id, ip_address FROM authentication WHERE id ="
            f" '{token_id}' AND mode = 'backtest';"
        )

        if get_ip_address_correspondence():
            __query += (
                " AND ip_address ="
                f" '{ip_address if isinstance(ip_address, str) else ''}';"
            )

        result = [
            AuthenticationOutput(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

        match len(result):
            case 1:
                row = result[0]
                created_at = row.created_at
                if datetime.now() <= created_at + timedelta(**get_time_activity()):
                    self.postgresql_instance.update(
                        f"SET search_path TO {get_postgresql_schema()}; DELETE FROM"
                        f" {Tables.AUTHENTICATION} WHERE id <> '{token_id}' AND user_id"
                        f" = '{row.user_id}';"
                    )
                    return True
                else:
                    self.postgresql_instance.update(
                        f"SET search_path TO {get_postgresql_schema()}; DELETE FROM"
                        f" {Tables.AUTHENTICATION} WHERE id = '{token_id}';"
                    )

        return False

    def get_users(
        self,
        email_address: str,
        password: str,
    ) -> list[User]:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id,"
            " CONCAT(first_name, ' ', second_name) AS full_name, first_name,"
            f" second_name, email_address, '{UserRole.ADMINISTRATOR}' AS role FROM"
            f" administrators WHERE CAST(id AS TEXT) = '{email_address}' AND"
            f" password = '{sha256(password.encode()).hexdigest()}' UNION ALL SELECT"
            " id, CONCAT(first_name, ' ', second_name) AS full_name, first_name,"
            f" second_name, email_address, '{UserRole.INVESTOR}' AS role"
            f" FROM investors WHERE email_address = '{email_address}' AND password ="
            f" '{sha256(password.encode()).hexdigest()}';"
        )

        return [
            User(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

    def get_administrator_by_email_address(
        self,
        email_address: str,
    ) -> list[AdministratorProfile]:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id,"
            " CONCAT(first_name, ' ', second_name) AS full_name, first_name,"
            f" second_name, email_address, policies, '{UserRole.ADMINISTRATOR}' AS role"
            f" FROM administrators WHERE email_address = '{email_address}';"
        )

        return [
            AdministratorProfile(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

    def get_investor_by_email_address(
        self,
        email_address: str,
    ) -> list[AdministratorProfile]:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id,"
            " CONCAT(first_name, ' ', second_name) AS full_name, first_name,"
            f" second_name, email_address, policies, '{UserRole.ADMINISTRATOR}' AS role"
            f" FROM investors WHERE email_address = '{email_address}';"
        )

        return [
            AdministratorProfile(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

    def get_portfolio_managers(
        self,
    ) -> list[AdministratorProfile]:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id,"
            " CONCAT(first_name, ' ', second_name) AS full_name, first_name,"
            f" second_name, email_address, policies, '{UserRole.ADMINISTRATOR}' AS role"
            " FROM administrators WHERE 'portfolio_manager_full_access' ="
            " ANY(policies);"
        )

        return [
            AdministratorProfile(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

    def get_funds(
        self,
    ) -> list[Fund]:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id, fund_name,"
            " investment_firm, administrator, investors, capital_distribution,"
            " commission_type, commission_value FROM funds"
        )

        return [
            Fund(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

    def update_policies(
        self,
        policies_update: PoliciesUpdate,
    ) -> bool:
        if not UserRole.has(policies_update.role):
            logger.critical(
                message=(
                    "Unable to update the policies of an unknown type of user (User ID:"
                    f" {policies_update.user_id})."
                )
            )
            return False

        if isinstance(policies_update.policies, str):
            policies_update.policies = [policies_update.policies]

        match policies_update.role:
            case UserRole.ADMINISTRATOR:
                policies_update.policies: list[str] = list(
                    set(policies_update.policies).intersection(
                        set(get_administrators_policies())
                    )
                )
            case UserRole.INVESTOR:
                policies_update.policies: list[str] = list(
                    set(policies_update.policies).intersection(
                        set(get_investors_policies())
                    )
                )
            case _:
                logger.critical(message="Unable to identify the role")
                return False

        __query = (
            f"SET search_path TO {get_postgresql_schema()}; UPDATE administrators SET"
            " policies = (SELECT array_agg(distinct e) FROM unnest(policies ||"
            f" array[{', '.join([x.__repr__() for x in policies_update.policies])}]"
            f"::text[]) e) WHERE id = {policies_update.user_id};"
        )

        self.postgresql_instance.update(query=__query)
        return True

    def get_fund_information(self, fund_name: str | None) -> FundInformation:
        where_clause = f"WHERE fund_name = '{fund_name}';"

        if fund_name is None:
            where_clause = ";"

        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id, investment_firm,"
            " fund_name, created_at, administrator, investors, capital_distribution,"
            " commission_type, commission_value, array['Sample1', 'Sample2']::text AS"
            f" strategies FROM funds {where_clause}"
        )

        return [
            FundInformation(**row._asdict())
            for row in self.postgresql_instance.select(query=__query)
        ]

    def check_for_investor_existence(
        self,
        investor_id: int,
    ) -> bool:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id FROM"
            f" investors WHERE id = '{str(investor_id)}';"
        )

        result = self.postgresql_instance.select(query=__query)
        match len(result):
            case 0:
                return False
            case 1:
                return True
            case _:
                logger.critical(
                    "Two or more investors have been found with the same id."
                )
                return False

    def check_for_administrator_existence(
        self,
        administrator_id: int,
    ) -> bool:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT id FROM"
            f" administrators WHERE id = '{str(administrator_id)}';"
        )

        result = self.postgresql_instance.select(query=__query)
        match len(result):
            case 0:
                return False
            case 1:
                return True
            case _:
                logger.critical(
                    "Two or more administrators have been found with the same id."
                )
                return False

    def add_investor_to_fund(
        self,
        investor_id: int,
        fund: str | int,
    ) -> bool:
        if self.check_for_investor_existence(investor_id=investor_id):
            __query = (
                f"SET search_path TO {get_postgresql_schema()}; UPDATE funds SET"
                " investors = (SELECT array_agg(distinct e) FROM"
                f" unnest(investors) || array['{str(investor_id)}']::text[]"
                f" e) WHERE fund_name = '{fund}' OR id = {fund};"
            )

            # TODO: Update capital_distribution JSONB

            self.postgresql_instance.update(query=__query)
            return True
        else:
            return False

    def add_administrator_to_fund(
        self,
        administrator_id: int,
        fund: str | int,
    ) -> bool:
        if self.check_for_administrator_existence(administrator_id=administrator_id):
            __query = (
                f"SET search_path TO {get_postgresql_schema()}; UPDATE funds SET"
                " administrators = (SELECT array_agg(distinct e) FROM"
                f" unnest(administrators) || array['{str(administrator_id)}']::text[]"
                f" e) WHERE fund_name = '{fund}' OR id = {fund};"
            )

            self.postgresql_instance.update(query=__query)
            return True
        else:
            return False

    def update_commission(
        self,
        commission: Commission,
    ) -> bool:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; UPDATE funds SET"
            f" commission_type = '{commission.commission_type}', commission_value ="
            f" {commission.commission_value} WHERE fund_name = '{commission.fund}'"
            f" OR id = {commission.fund};"
        )

        return self.postgresql_instance.update(query=__query)
