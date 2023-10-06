from pymongo.errors import ConnectionFailure


class MongoConnectionError(ConnectionFailure, Exception):
    pass
