import numpy as np
import torch
from numpy.typing import NDArray

from inkosi.database.mongodb.schemas import Position
from inkosi.log.log import Logger

from .models import (
    TICKS_ASK_INDEX,
    TICKS_BID_INDEX,
    TICKS_DATETIME_INDEX,
    BacktestRecord,
    BacktestRequest,
    TradeResult,
    TradeStatus,
)

logger = Logger(
    module_name="backtest",
    package_name="backtest",
    database=False,
)


def checker(
    dataset: NDArray,
    direction: Position,
    starting_index: int,
    entry_point: float,
    take_profit: float,
    stop_loss: float,
    delta: int = 20000,
) -> int | None:
    current_index = starting_index
    last_index = dataset.shape[0]

    if not Position.has(direction):
        logger.critical("Backtest Interrupted... Dataset records exhausted")
        return

    while current_index < last_index:
        if direction == Position.BUY:
            result = np.argmax(
                (
                    dataset[current_index : current_index + delta]
                    >= entry_point + take_profit
                )
            )

        elif direction == Position.SELL:
            result = np.argmax(
                (
                    dataset[current_index : current_index + delta]
                    <= entry_point - abs(stop_loss)
                )
            )

        if not result:
            current_index += delta

        if result:
            return result


@torch.compile
def backtest(request: BacktestRequest) -> list[BacktestRecord] | None:
    result: list[BacktestRecord] = []
    dataset: NDArray = request.dataset.get_dataset()
    n_dataset: int = dataset.shape[0]

    if len(request.direction) != len(request.starting_indexes):
        logger.error(
            "The length of the 'Direction' vector is not equal to the 'Starting"
            " Indexes' vector"
        )
        return

    for occurence, direction, take_profit, stop_loss in zip(
        request.starting_indexes,
        request.direction,
        request.take_profits,
        request.stop_losses,
    ):
        if occurence + 1 > n_dataset:
            logger.critical("Backtest Interrupted... Dataset records exhausted")
            break

        entry_point_index: int = occurence + 1

        if direction == Position.BUY:
            entry_point_price: float = dataset[entry_point_index, TICKS_BID_INDEX]
        if direction == Position.SELL:
            entry_point_price: float = dataset[entry_point_index, TICKS_ASK_INDEX]

        result_up = checker(
            dataset,
            Position.BUY,
            entry_point_index,
            entry_point_price,
            take_profit,
            stop_loss,
        )
        result_down = checker(
            dataset,
            Position.SELL,
            entry_point_index,
            entry_point_price,
            take_profit,
            stop_loss,
        )

        if direction == Position.BUY:
            if result_down == 0:
                trade_result = TradeResult.PROFIT
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                )
            elif result_up == 0:
                trade_result = TradeResult.LOSS
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                )
            else:
                trade_result = TradeResult.PENDING
                trade_status = TradeStatus.PENDING

                last = "NA"

            if result_up < result_down:
                trade_result = TradeResult.PROFIT
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                )
            else:
                trade_result = TradeResult.LOSS
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                )
        elif direction == Position.SELL:
            if result_down == 0:
                trade_result = TradeResult.LOSS
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                )
            elif result_up == 0:
                trade_result = TradeResult.PROFIT
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                )

            else:
                trade_result = TradeResult.PENDING
                trade_status = TradeStatus.PENDING
                last = "NA"

            if result_up < result_down:
                trade_result = TradeResult.LOSS
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_up, TICKS_DATETIME_INDEX]
                )
            else:
                trade_result = TradeResult.PROFIT
                trade_status = TradeStatus.CLOSED

                last = (
                    dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                    - dataset[entry_point_index + result_down, TICKS_DATETIME_INDEX]
                )
        else:
            logger.critical(
                f"Unable to identify the specified 'Direction' parameter: {direction}"
            )

        result.append(
            BacktestRecord(
                direction=direction,
                entry_point=entry_point_price,
                entry_point_index=entry_point_index,
                take_profit=take_profit,
                stop_loss=stop_loss,
                price_close=...,
                price_close_index=...,
                time_opening=...,
                time_closing=...,
                status=trade_status,
                result=trade_result,
            )
        )

    return result
