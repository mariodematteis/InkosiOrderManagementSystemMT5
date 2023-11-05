import random
from functools import lru_cache

from inkosi.database.mongodb.schemas import Position, TradeRequest
from inkosi.log.log import Logger
from inkosi.portfolio.risk_management import RiskManagement
from inkosi.utils.settings import get_environmental_settings

from .schemas import OpenRequestTradeResult, StatusTradeResult

try:
    import MetaTrader5 as mt5

    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False


logger = Logger(module_name="metatrader5", package_name="api")


def check_mt5_available() -> bool:
    if not MT5_AVAILABLE:
        raise False

    if not mt5.initialize(
        server=get_environmental_settings().SERVER,
        login=get_environmental_settings().ACCOUNT,
        password=get_environmental_settings().PASSWORD,
    ):
        logger.error(
            "Unable to establish a connection the Broker through the given credentials"
        )
        return False


def initialize() -> bool:
    return check_mt5_available()


def shutdown() -> None:
    check_mt5_available()
    mt5.shutdown()


@lru_cache
def get_all_symbols_available() -> list[str] | None:
    if initialize():
        return [symbol._asdict().get("name", "") for symbol in list(mt5.symols_get())]

    logger.critical("No symbols have been found")


def check_for_financial_product_existence(financial_product: str) -> bool:
    symbols_list = get_all_symbols_available()
    if not symbols_list:
        return False

    return financial_product in symbols_list


def check_for_positions_opened_on_symbol(symbol: str) -> int | None:
    if not initialize():
        return
    return mt5.positions_get(symbol=symbol)


# TODO: Add hinting
def get_symbol_filling(symbol: str) -> int | None:
    if not initialize() or check_for_financial_product_existence(symbol):
        return

    match mt5.symbol_info(symbol)._asdict().get("filling_mode", None):
        case None:
            logger.error(
                f"Unable to fetch informatin regarding the symbol specified: {symbol}"
            )
            return
        case 1:
            return mt5.ORDER_FILLING_FOK
        case 2:
            return mt5.ORDER_FILLING_IOC
        case _:
            return mt5.ORDER_FILLING_RETURN


# TODO: Check if returns less or equal to 0 when the market is closed on that product
def get_ask_of_symbol(symbol):
    ask = mt5.symbol_info_tick(symbol).ask
    if ask > 0:
        return ask
    else:
        get_ask_of_symbol(symbol)


def get_bid_of_symbol(symbol):
    bid = mt5.symbol_info_tick(symbol).bid
    if bid > 0:
        return bid
    else:
        get_bid_of_symbol(symbol)


def open_position(
    order: TradeRequest,
    allow_no_risk_limits: bool,
) -> OpenRequestTradeResult:
    risk_management = RiskManagement()

    if order.ticker is None:
        return OpenRequestTradeResult(
            detail="No Ticker has been provided",
            status=StatusTradeResult.NO_TICKER_PROVIDED,
        )

    if not check_for_financial_product_existence(order.ticker):
        return OpenRequestTradeResult(
            detail="Ticker provided doesn't exist",
            status=StatusTradeResult.TICKER_NOT_FOUND,
        )

    if not order.risk_management:
        volume: float = risk_management.compute_volume()
    else:
        volume: float | None = order.volume
        if not volume:
            return OpenRequestTradeResult(
                detail="No volume has been provided",
                status=StatusTradeResult.NO_VOLUME_PROVIDED,
            )

    match order.operation:
        case Position.BUY:
            position = mt5.POSITION_TYPE_BUY
            price: float = get_bid_of_symbol()
        case Position.SELL:
            position = mt5.POSITION_TYPE_SELL
            price: float = get_ask_of_symbol()
        case _:
            return OpenRequestTradeResult(
                detail="No specified operation has not been recognised",
                status=StatusTradeResult.NO_OPERATION_SPECIFIED,
            )

    trade_id: int = random.randint(100000000, 999999999)

    filling = get_symbol_filling(order.ticker)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": order.ticker,
        "volume": volume,
        "type": position,
        "price": price,
        "deviation": 20,
        "magic": trade_id,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling,
    }

    take_profit: float = 0.0
    stop_loss: float = 0.0

    match type(order.tp):
        case type(float()):
            take_profit = order.tp
        case _:
            take_profit: float | None = risk_management.adjust_take_profit()
            if not take_profit:
                if not allow_no_risk_limits:
                    return OpenRequestTradeResult(
                        detail="No Take Profit has been specified",
                        status=StatusTradeResult.NO_TAKE_PROFIT_SPECIFIED,
                    )
            else:
                request["tp"] = take_profit

    match type(order.sl):
        case type(float()):
            stop_loss = order.stop_loss
        case _:
            stop_loss: float | None = risk_management.adjust_stop_loss()

            if not stop_loss:
                if not allow_no_risk_limits:
                    return OpenRequestTradeResult(
                        detail="No Stop Loss has been specified",
                        status=StatusTradeResult.NO_STOP_LOSS_SPECIFIED,
                    )
            else:
                request["sl"] = stop_loss

    initialize()
    order_request = mt5.order_send(request)
    if order_request.retcode != mt5.TRADE_RETCODE_DONE:
        return OpenRequestTradeResult(
            detail="Unable to correctly fill the order",
            status=StatusTradeResult.NO_ORDER_FILLING,
            error="An error occurred while filling the order",
            error_code=order_request.retcode,
        )
    else:
        return OpenRequestTradeResult(
            detail="Order correctly filled",
            status=StatusTradeResult.ORDER_FILLED,
        )


# TODO: Rewrite
def close_position(
    order: TradeRequest,
    allow_no_risk_limits: bool,
) -> OpenRequestTradeResult:
    risk_management = RiskManagement()

    if order.ticker is None:
        return OpenRequestTradeResult(
            detail="No Ticker has been provided",
            status=StatusTradeResult.NO_TICKER_PROVIDED,
        )

    if not check_for_financial_product_existence(order.ticker):
        return OpenRequestTradeResult(
            detail="Ticker provided doesn't exist",
            status=StatusTradeResult.TICKER_NOT_FOUND,
        )

    if not order.risk_management:
        volume: float = risk_management.compute_volume()
    else:
        volume: float | None = order.volume
        if not volume:
            return OpenRequestTradeResult(
                detail="No volume has been provided",
                status=StatusTradeResult.NO_VOLUME_PROVIDED,
            )

    match order.operation:
        case Position.BUY:
            position = mt5.POSITION_TYPE_BUY
            price: float = get_bid_of_symbol()
        case Position.SELL:
            position = mt5.POSITION_TYPE_SELL
            price: float = get_ask_of_symbol()
        case _:
            return OpenRequestTradeResult(
                detail="No specified operation has not been recognised",
                status=StatusTradeResult.NO_OPERATION_SPECIFIED,
            )

    trade_id: int = random.randint(100000000, 999999999)

    filling = get_symbol_filling(order.ticker)
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": order.ticker,
        "volume": volume,
        "type": position,
        "price": price,
        "deviation": 20,
        "magic": trade_id,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling,
    }

    take_profit: float = 0.0
    stop_loss: float = 0.0

    match type(order.tp):
        case type(float()):
            take_profit = order.tp
        case _:
            take_profit: float | None = risk_management.adjust_take_profit()
            if not take_profit:
                if not allow_no_risk_limits:
                    return OpenRequestTradeResult(
                        detail="No Take Profit has been specified",
                        status=StatusTradeResult.NO_TAKE_PROFIT_SPECIFIED,
                    )
            else:
                request["tp"] = take_profit

    match type(order.sl):
        case type(float()):
            stop_loss = order.stop_loss
        case _:
            stop_loss: float | None = risk_management.adjust_stop_loss()

            if not stop_loss:
                if not allow_no_risk_limits:
                    return OpenRequestTradeResult(
                        detail="No Stop Loss has been specified",
                        status=StatusTradeResult.NO_STOP_LOSS_SPECIFIED,
                    )
            else:
                request["sl"] = stop_loss

    initialize()
    order_request = mt5.order_send(request)
    if order_request.retcode != mt5.TRADE_RETCODE_DONE:
        return OpenRequestTradeResult(
            detail="Unable to correctly fill the order",
            status=StatusTradeResult.NO_ORDER_FILLING,
            error="An error occurred while filling the order",
            error_code=order_request.retcode,
        )
    else:
        return OpenRequestTradeResult(
            detail="Order correctly filled",
            status=StatusTradeResult.ORDER_FILLED,
        )
