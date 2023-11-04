from inkosi.utils.exceptions import MT5AvailabilityError

from .schemas import OpenRequestTradeResult

try:
    import MetaTrader5 as mt5

    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False


def check_mt5_available() -> None:
    if not MT5_AVAILABLE:
        raise MT5AvailabilityError


def initialize() -> bool:
    check_mt5_available()
    return mt5.initialize()


def shutdown() -> None:
    check_mt5_available()
    mt5.shutdown()


def open_position() -> OpenRequestTradeResult:
    ...
