from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from inkosi.api.metatrader import open_position
from inkosi.api.schemas import OpenRequestTradeResult, StatusTradeResult
from inkosi.database.mongodb.database import MongoDBCrud
from inkosi.database.mongodb.schemas import TradeRequest

router = APIRouter(prefix="/trading")


@router.post(path="/position")
async def position(order: TradeRequest) -> Response:
    mongodb = MongoDBCrud()

    result: OpenRequestTradeResult = open_position(order, False)
    match result.status:
        case StatusTradeResult.ORDER_FILLED:
            record_id: ObjectId | None = mongodb.add_trade(order)

            return JSONResponse(
                content={
                    "detail": "Position correctly opened",
                    "record": record_id,
                },
                status_code=status.HTTP_200_OK,
            )
        case _:
            return JSONResponse(
                content={
                    "detail": "Unable to open the position",
                    "message": result.detail,
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@router.delete(path="/position")
async def close_position(order: TradeRequest):
    return status.HTTP_200_OK
