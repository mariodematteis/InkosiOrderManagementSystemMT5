from enum import StrEnum


class EnhancedStrEnum(StrEnum):
    @classmethod
    def has(cls, key: str):
        return key in cls.__members__.values()

    @classmethod
    def list(cls):
        return list(cls.__members__.values())
