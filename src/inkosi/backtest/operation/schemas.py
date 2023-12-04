from dataclasses import dataclass
from typing import TypeAlias

from inkosi.utils.utils import EnhancedStrEnum

ComparisonElement: TypeAlias = dict[str, int | float | str]

Colors: list[str] = [
    "#4c78a8",
    "#f58518",
    "#e45756",
    "#72b7b2",
    "#54a24b",
    "#eeca3b",
    "#b279a2",
    "#ff9da6",
    "#9d755d",
    "#bab0ac",
]


class Elements(EnhancedStrEnum):
    ELEMENT: str = "ELEMENT"
    PERIOD: str = "PERIOD"

    CLOSE_PRICE: str = "Close"


class AvailableRawColumns(EnhancedStrEnum):
    DATES: str = "Dates"
    OPEN_PRICE: str = "Open"
    HIGH_PRICE: str = "High"
    LOW_PRICE: str = "Low"
    CLOSE_PRICE: str = "Close"
    RETURNS: str = "Returns"


class VisualisationOptions(EnhancedStrEnum):
    OPEN_PRICE: str = "Open"
    HIGH_PRICE: str = "High"
    LOW_PRICE: str = "Low"
    CLOSE_PRICE: str = "Close"
    RETURNS: str = "Returns"


class Relation(EnhancedStrEnum):
    GREATER: str = ">"
    GREATER_THAN: str = ">="
    LESS: str = "<"
    LESS_THAN: str = "<="
    EQUAL: str = "=="


class AvailableTechincalIndicators(EnhancedStrEnum):
    SMA: str = "SMA"
    WMA: str = "WMA"
    EMA: str = "EMA"


class TimeFrames(EnhancedStrEnum):
    MINUTES_1: str = "1m"
    MINUTES_2: str = "2m"
    MINUTES_5: str = "5m"
    MINUTES_15: str = "15m"
    MINUTES_30: str = "30m"
    MINUTES_60: str = "60m"
    MINUTES_90: str = "90m"
    HOUR_1: str = "1h"
    DAY_1: str = "1d"
    DAY_5: str = "5d"
    WEEK_1: str = "1wk"
    MONTH_1: str = "1mo"
    MONTH_3: str = "3mo"


class DataSourceType(EnhancedStrEnum):
    YAHOO_FINANCE: str = "Yahoo Finance"


class SamplingMethods(EnhancedStrEnum):
    NORMAL_DISTRIBUTION: str = "Normal Sampling"
    LAPLACE_DISTRIBUTION: str = "Laplace Sampling"
    UNIFORM_DISTRIBUTION: str = "Uniform Sampling"


@dataclass
class Filter:
    first_element: ComparisonElement
    second_element: ComparisonElement
    relation: Relation | None
