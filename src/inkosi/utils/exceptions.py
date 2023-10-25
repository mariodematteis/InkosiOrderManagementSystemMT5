from pymongo.errors import ConnectionFailure


class MongoConnectionError(ConnectionFailure, Exception):
    "Unable to establish with the MongoDB Instance"


class PostgreSQLConnectionError(Exception):
    "Unable to establish with the PostgreSQL Instance"
