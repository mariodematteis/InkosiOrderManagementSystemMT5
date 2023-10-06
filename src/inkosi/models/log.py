from enum import StrEnum


class LogType(StrEnum):
    CRITICAL: str = "CRITICAL"
    DEBUG: str = "DEBUG"
    ERROR: str = "ERROR"
    INFO: str = "INFORMATION"
    WARN: str = "WARNING"
