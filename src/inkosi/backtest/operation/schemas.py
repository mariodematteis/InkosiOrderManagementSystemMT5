from dataclasses import dataclass
from typing import TypeAlias

from inkosi.utils.utils import EnhancedStrEnum

ComparisonElement: TypeAlias = dict[str, int | float | str]


class Elements(EnhancedStrEnum):
    """
    Enumeration of generic elements.

    Attributes:
        ELEMENT (str): Represents a generic element.
        PERIOD (str): Represents a period element.
    """

    ELEMENT: str = "ELEMENT"
    PERIOD: str = "PERIOD"


class AvailableRawColumns(EnhancedStrEnum):
    """
    Enumeration of available raw columns in a dataset.

    Attributes:
        DATES (str): Column representing dates.
        OPEN_PRICE (str): Column representing open prices.
        HIGH_PRICE (str): Column representing high prices.
        LOW_PRICE (str): Column representing low prices.
        CLOSE_PRICE (str): Column representing close prices.
        RETURNS (str): Column representing returns.
    """

    DATES: str = "DATES"
    OPEN_PRICE: str = "OPEN"
    HIGH_PRICE: str = "HIGH"
    LOW_PRICE: str = "LOW"
    CLOSE_PRICE: str = "CLOSE"
    RETURNS: str = "RETURNS"


class Relation(EnhancedStrEnum):
    """
    Enumeration of comparison relations.

    Attributes:
        GREATER (str): Represents the greater than relation.
        GREATHER_THAN (str): Represents the greater than or equal to relation.
        LESS (str): Represents the less than relation.
        LESS_THAN (str): Represents the less than or equal to relation.
        EQUAL (str): Represents the equal to relation.
    """

    GREATER: str = ">"
    GREATHER_THAN: str = ">="
    LESS: str = "<"
    LESS_THAN: str = "<="
    EQUAL: str = "=="


class AvailableTechincalIndicators(EnhancedStrEnum):
    """
    Enumeration of available technical indicators.

    Attributes:
        SMA (str): Represents the Simple Moving Average indicator.
        WMA (str): Represents the Weighted Moving Average indicator.
        EMA (str): Represents the Exponential Moving Average indicator.
    """

    SMA: str = "SMA"
    WMA: str = "WMA"
    EMA: str = "EMA"


@dataclass
class Filter:
    """
    Data class representing a filter condition.

    Attributes:
        first_element (ComparisonElement): The first element in the comparison.
        second_element (ComparisonElement): The second element in the comparison.
        relation (Relation): The relation between the elements.
    """

    first_element: ComparisonElement
    second_element: ComparisonElement
    relation: Relation
