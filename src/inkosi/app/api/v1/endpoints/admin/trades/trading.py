from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from inkosi.api.metatrader import open_position
from inkosi.api.schemas import OpenRequestTradeResult
from inkosi.database.mongodb.database import MongoDBCrud
from inkosi.database.mongodb.schemas import TradeRequest

router = APIRouter()


@router.post(path="/position")
async def position(order: TradeRequest) -> Response:
    mongodb = MongoDBCrud()

    result: OpenRequestTradeResult = open_position()
    match result.status:
        case 0:
            mongodb.add_trade(order)
            return JSONResponse(
                content={
                    "detail": "Position correctly opened",
                },
                status_code=status.HTTP_200_OK,
            )
        case -1:
            return JSONResponse(content={"detail": "Position "})
        case _:
            return JSONResponse(
                content={
                    "detail": "Unable to open the position",
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@router.delete(path="/position")
async def close_position(order: TradeRequest):
    return status.HTTP_200_OK
