from fastapi import APIRouter, status

from inkosi.database.mongodb.schemas import TradeRequest

router = APIRouter()


@router.post(path="/open_position")
def open_position(order: TradeRequest):
    return status.HTTP_200_OK


@router.delete(path="/close_position")
def close_position(order: TradeRequest):
    return status.HTTP_200_OK
