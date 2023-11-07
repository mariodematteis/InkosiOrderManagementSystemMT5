from dataclasses import asdict

import certifi
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database

from inkosi.log.log import Logger
from inkosi.utils.exceptions import MongoConnectionError
from inkosi.utils.settings import (
    get_mongodb_collection,
    get_mongodb_settings,
    get_mongodb_url,
)

from .schemas import TradeRequest

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


class MongoDBCrud:
    def __init__(self) -> None:
        self.mongodb_instance = MongoDBInstance()

    def add_trade(
        self,
        trade_request: TradeRequest,
    ) -> ObjectId:
        trades_collection = self.mongodb_instance.database[
            get_mongodb_collection().Trade
        ]

        result = trades_collection.insert_one(
            asdict(
                trade_request,
            ),
        )
        return result.inserted_id

    def update_trade(
        self,
        trade_id: ObjectId | str,
        updates: TradeRequest,
    ) -> dict | None:
        trades_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Trade
        ]

        result: dict | None = trades_collection.find_one_and_update(
            {
                "_id": trade_id
                if isinstance(trade_id, ObjectId)
                else ObjectId(trade_id),
            },
            {
                "$set": asdict(
                    updates,
                    dict_factory=lambda x: {k: v for (k, v) in x if v is not None},
                ),
            },
            return_document=ReturnDocument.AFTER,
        )
        return result

    def remove_trade(
        self,
        trade_id: ObjectId | str,
    ) -> bool:
        trades_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Trade
        ]

        result = trades_collection.delete_one(
            {
                "_id": trade_id
                if isinstance(trade_id, ObjectId)
                else ObjectId(trade_id),
            },
        )
        return result.deleted_count == 1

    def get_trade(
        self,
        trade_id: ObjectId | str,
    ) -> dict:
        trades_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Trade
        ]

        if isinstance(trade_id, str):
            trade_id = ObjectId(trade_id)

        result = list(
            trades_collection.aggregate(
                [
                    {
                        "$match": {
                            "_id": trade_id,
                        },
                    },
                    {
                        "$addFields": {
                            "_id": {
                                "$toString": "$_id",
                            },
                        },
                    },
                ]
            )
        )
        return result[0] if len(result) == 1 else {}

    def get_all_trades(
        self,
        opened: bool | None = None,
    ) -> list[dict]:
        trades_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Trade
        ]

        match opened:
            case bool():
                return list(
                    trades_collection.aggregate(
                        [
                            {
                                "$match": {
                                    "status": opened,
                                },
                            },
                            {
                                "$addFields": {
                                    "_id": {
                                        "$toString": "$_id",
                                    },
                                },
                            },
                        ]
                    )
                )
            case _:
                return list(
                    trades_collection.aggregate(
                        [
                            {
                                "$addFields": {
                                    "_id": {
                                        "$toString": "$_id",
                                    },
                                },
                            },
                        ]
                    )
                )

    def get_deal_from_id(
        self,
        record_id: str,
    ) -> TradeRequest:
        trades_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Trade
        ]

        records = trades_collection.aggregate(
            [
                {
                    "$match": {
                        "_id": ObjectId(
                            record_id,
                        ),
                    },
                },
                {
                    "$unset": "_id",
                },
            ],
        )

        if not records:
            logger.critical(message="No record has been found")
            return

        record = list(records)[0]

        return TradeRequest(**record)
