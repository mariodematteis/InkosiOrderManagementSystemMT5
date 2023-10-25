from dataclasses import dataclass

from inkosi.models.log import LogType


@dataclass
class Log:
    PackageName: str
    ModuleName: str
    Level: LogType
    Message: str
