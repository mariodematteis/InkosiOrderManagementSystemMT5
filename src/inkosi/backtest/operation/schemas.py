from dataclasses import dataclass
from typing import TypeAlias

from inkosi.utils.utils import EnhancedStrEnum

ComparisonElement: TypeAlias = dict[str, int | float | str]


class Elements(EnhancedStrEnum):
    ELEMENT: str = "ELEMENT"
    PERIOD: str = "PERIOD"


class AvailableRawColumns(EnhancedStrEnum):
    DATES: str = "DATES"
    OPEN_PRICE: str = "OPEN"
    HIGH_PRICE: str = "HIGH"
    LOW_PRICE: str = "LOW"
    CLOSE_PRICE: str = "CLOSE"
    RETURNS: str = "RETURNS"


class Relation(EnhancedStrEnum):
    GREATER: str = ">"
    GREATHER_THAN: str = ">="
    LESS: str = "<"
    LESS_THAN: str = "<="
    EQUAL: str = "=="


class AvailableTechincalIndicators(EnhancedStrEnum):
    SMA: str = "SMA"
    WMA: str = "WMA"
    EMA: str = "EMA"


@dataclass
class Filter:
    first_element: ComparisonElement
    second_element: ComparisonElement
    relation: Relation
