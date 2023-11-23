from datetime import date, datetime, timedelta

import pandas as pd
from fastapi import APIRouter

from inkosi.app.schemas import Returns
from inkosi.database.mongodb.database import MongoDBCrud
from inkosi.database.mongodb.schemas import ReturnRequest
from inkosi.database.postgresql.database import PostgreSQLCrud
from inkosi.database.postgresql.schemas import FundInformation

router = APIRouter()


@router.post(
    path="/returns",
    summary="",
    response_model=Returns,
)
async def returns(
    return_request: ReturnRequest,
):
    postgres = PostgreSQLCrud()
    fund_information: FundInformation = postgres.get_fund_information(
        return_request.fund_name
    )

    fund_creation_date: date = fund_information.created_at
    initial_capital: float = sum(fund_information.capital_distribution.values())
    # cumulative_returns: float = initial_capital

    mongodb = MongoDBCrud()
    result = mongodb.get_returns(fund=fund_information.id)

    raw_dates_range = pd.date_range(start=fund_creation_date, end=datetime.today())
    raw_returns = dict[date, float]

    for _date in raw_dates_range:
        raw_returns[_date] = raw_returns.get(_date - timedelta(days=1), initial_capital)
        respective_records = result.get(_date, [])
        for record in respective_records:
            raw_returns[_date] += record.get("return")
