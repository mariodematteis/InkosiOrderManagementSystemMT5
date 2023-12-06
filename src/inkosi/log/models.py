from enum import StrEnum


class LogType(StrEnum):
    """
    Enumeration representing different log types.

    Attributes:
        CRITICAL (str): Critical log type.
        DEBUG (str): Debug log type.
        ERROR (str): Error log type.
        INFO (str): Information log type.
        WARN (str): Warning log type.

    Note:
        This enumeration defines different log types as class attributes.
        Each attribute represents a specific log type with a descriptive name.
    """

    CRITICAL: str = "CRITICAL"
    DEBUG: str = "DEBUG"
    ERROR: str = "ERROR"
    INFO: str = "INFORMATION"
    WARN: str = "WARNING"
