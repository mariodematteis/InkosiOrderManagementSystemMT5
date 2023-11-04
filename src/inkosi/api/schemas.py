from dataclasses import dataclass


@dataclass
class OpenRequestTradeResult:
    detail: str
    status: int
    error: str | None = None
    error_code: int | None = None
