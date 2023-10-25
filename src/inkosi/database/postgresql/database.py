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
from inkosi.utils.settings import get_postgresql_schema, get_postgresql_url

logger = Logger(
    module_name="PostgreSQLDatabase", package_name="postgresql", database=False
)


class DatabaseInstanceSingleton(
    type,
):
    _instance = None

    def __call__(
        cls,
        *args,
        **kwargs,
    ):
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
    def __init__(
        self,
    ) -> None:
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

    def connect(self) -> None:
        try:
            self.base.metadata.create_all(bind=self.engine)
        except Exception:
            logger.error("Unable to establish with the PostgreSQL Instance")
            raise PostgreSQLConnectionError

    @beartype
    def add(self, model: Iterable[declarative_base()] | declarative_base()) -> None:
        __session = sessionmaker(bind=self.engine)
        with __session() as session:
            if isinstance(model, Iterable):
                session.add_all(model)
            else:
                session.add(model)

            session.commit()
            session.close()

    @beartype
    def select(self, query: TextClause | str) -> list[Any]:
        __session = sessionmaker(bind=self.engine)
        with __session() as session:
            __query = session.execute(
                query if isinstance(query, TextClause) else text(query)
            )
            result = __query.all()
            session.close()
            return result


class PostgreSQLCrud:
    def __init__(self) -> None:
        self.postgresql_instance = PostgreSQLInstance()

    def get_users(self, email_address: str, password: str) -> list[dict]:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT CONCAT(first_name, '"
            " ', second_name) AS full_name, first_name, second_name, email_address,"
            " 'administrator' AS Role FROM administrators WHERE email_address ="
            f" '{email_address}' AND password ="
            f" '{sha256(password.encode()).hexdigest()}' UNION ALL SELECT"
            " CONCAT(first_name, ' ', second_name) AS full_name, first_name,"
            " second_name, email_address, 'investor' AS Role FROM investors WHERE"
            f" email_address = '{email_address}' AND password ="
            f" '{sha256(password.encode()).hexdigest()}';"
        )

        return [row._asdict() for row in self.postgresql_instance.select(query=__query)]

    def get_portfolio_managers(
        self,
    ) -> list[dict]:
        __query = (
            f"SET search_path TO {get_postgresql_schema()}; SELECT CONCAT(first_name, '"
            " ', second_name) AS full_name, first_name, second_name, email_address,"
            " 'administrator' AS Role FROM administrators WHERE"
            " 'portfolio_manager_full_access' = ANY(policies);"
        )

        return [row._asdict() for row in self.postgresql_instance.select(query=__query)]
