import certifi
from pymongo import MongoClient
from pymongo.database import Database

from inkosi.log.log import Logger
from inkosi.utils.exceptions import MongoConnectionError
from inkosi.utils.settings import get_mongodb_settings, get_mongodb_url

logger = Logger(module_name="MongoDBDatabase", package_name="mongodb", database=False)


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


class MongoDBInstance(
    metaclass=DatabaseInstanceSingleton,
):
    client: MongoClient = None
    database: Database = None

    def __init__(
        self,
    ) -> None:
        try:
            if get_mongodb_settings().TLS:
                self.client = MongoClient(
                    get_mongodb_url(),
                    tlsCAFile=certifi.where(),
                )
            else:
                self.client = MongoClient(
                    get_mongodb_url(),
                )

            self.client.admin.command(
                "ping",
            )
            self.database = self.client[get_mongodb_settings().DATABASE]
        except Exception:
            logger.error(message="Unable to establish with the MongoDB Instance")
            raise MongoConnectionError

    def is_connected(
        self,
    ) -> bool:
        try:
            if not isinstance(
                self.client,
                MongoClient,
            ):
                return False

            self.client.admin.command(
                "ping",
            )
        except Exception:
            return False

        return True

    def close_database_connection(
        self,
    ) -> None:
        self.client.close()
