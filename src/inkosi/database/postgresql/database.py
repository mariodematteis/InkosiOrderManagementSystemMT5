from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from inkosi.utils.settings import get_postgresql_url


class DatabaseInstanceSingleton(
    type,
):
    _instance = None

    def __call__(
        cls,
        *args,
        **kwargs,
    ):
        if not cls._instance or not cls._instance.is_connected():
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
        self.engine = create_engine(
            get_postgresql_url(),
        )

        if not database_exists(self.engine.url):
            print("Creating")
            create_database(self.engine.url)

        self.session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

        self.base = declarative_base()

    def is_connected(
        self,
    ) -> bool:
        ...

    def close_database_connection(
        self,
    ) -> None:
        ...
