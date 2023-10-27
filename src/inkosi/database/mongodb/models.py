from dataclasses import dataclass

from bson import ObjectId

from inkosi.log.models import LogType


@dataclass
class Trade:
    _id: ObjectId


@dataclass
class Log:
    PackageName: str
    ModuleName: str
    Level: LogType
    Message: str
