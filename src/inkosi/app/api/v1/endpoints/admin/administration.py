from hashlib import sha256

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from inkosi.app.schemas import AdministratorRequest, InvestorRequest, Returns
from inkosi.database.mongodb.database import MongoDBCrud
from inkosi.database.mongodb.schemas import ReturnRequest
from inkosi.database.postgresql.database import PostgreSQLCrud, PostgreSQLInstance
from inkosi.database.postgresql.models import Administrator, Investor
from inkosi.database.postgresql.schemas import (
    AddAdministratorToFund,
    AddInvestorToFund,
    AdministratorProfile,
    Commission,
    Fund,
    FundInformation,
    InvestorProfile,
    PoliciesUpdate,
)
from inkosi.utils.settings import get_api_settings

router = APIRouter()


@router.get(path="/available_apis")
async def return_available_apis() -> Response:
    return JSONResponse(
        content={"detail": get_api_settings().APIs},
        status_code=status.HTTP_200_OK,
    )


@router.post(
    path="/create_administrator",
    response_model=list[AdministratorProfile],
)
async def create_administrator(administrator_request: AdministratorRequest):
    postgres_instance = PostgreSQLInstance()

    administrator = Administrator(
        first_name=administrator_request.first_name,
        second_name=administrator_request.second_name,
        email_address=administrator_request.email_address,
        birthday=administrator_request.birthday,
        fiscal_code=administrator_request.fiscal_code,
        password=sha256(administrator_request.password.encode()).hexdigest(),
        policies=administrator_request.policies,
        active=administrator_request.active,
    )

    postgres_instance.add(model=[administrator])

    postgres = PostgreSQLCrud()
    return postgres.get_administrator_by_email_address(
        email_address=administrator.email_address
    )


@router.post(
    path="/create_investor",
    response_model=list[InvestorProfile],
)
async def create_investor(investor_request: InvestorRequest):
    postgres_instance = PostgreSQLInstance()

    investor = Investor(
        first_name=investor_request.first_name,
        second_name=investor_request.second_name,
        email_address=investor_request.email_address,
        birthday=investor_request.birthday,
        fiscal_code=investor_request.fiscal_code,
        password=sha256(investor_request.password.encode()).hexdigest(),
        policies=investor_request.policies,
        active=investor_request.active,
    )

    postgres_instance.add(model=[investor])

    postgres = PostgreSQLCrud()
    return postgres.get_investor_by_email_address(email_address=investor.email_address)


@router.get(
    path="/list_portfolio_managers",
    response_model=list[AdministratorProfile],
)
async def list_portfolio_managers(status: bool | None = None):
    """
    Return the list of Active, Inactive or all Portfolio Managers

    Parameters
    ----------
    status : bool | None, optional
        Specify if you would like to discover active or inactive portfolio managers
        , by default None

    Returns
    -------
    list[AdministratorProfile]
        List containing records of Portfolio Manager, each of them contains information
        such as: Full Name, E-mail Address, Policies, ...
    """
    postgresql = PostgreSQLCrud()

    if status is None:
        return postgresql.get_portfolio_managers()


@router.get(
    path="/list_funds",
    response_model=list[Fund],
)
async def list_funds(status: bool | None = None):
    """
    Return the list of Active, Inactive or all Funds

    Parameters
    ----------
    status : bool | None, optional
        Specify if you would like to discover active or inactive funds, by default None

    Returns
    -------
    list[Fund]
        List containing records of Fund, each of them contains information
        such as: id, Fund Name, Portfolio Managers, ...
    """
    postgresql = PostgreSQLCrud()

    if status is None:
        return postgresql.get_funds()


@router.post(path="/returns", response_model=Returns)
async def returns(return_request: ReturnRequest):
    postgres = PostgreSQLCrud()
    fund_information: FundInformation = postgres.get_fund_information(
        return_request.fund_name
    )

    initial_capital: float = sum(fund_information.capital_distribution.values())

    mongodb = MongoDBCrud()
    result = mongodb.get_returns(fund=fund_information.id)

    for record in result:
        ...


@router.put(
    path="/update_policies",
    response_class=Response,
)
async def update_policies(policies_update: PoliciesUpdate):
    postgres = PostgreSQLCrud()
    result = postgres.update_policies(
        policies_update=policies_update,
    )

    if not result:
        return JSONResponse(
            content={
                "detail": "Unable to update the policy",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return JSONResponse(
        content={
            "detail": "Correctly updated",
        },
        status_code=status.HTTP_200_OK,
    )


@router.post(path="/add_investor")
async def add_investor(add_investor_to_fund: AddInvestorToFund) -> Response:
    postgres = PostgreSQLCrud()
    result = postgres.add_investor_to_fund(
        add_investor_to_fund.investor_id,
        add_investor_to_fund.fund,
    )

    if result:
        return JSONResponse(
            content={
                "detail": "Investor correctly added to the fund",
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={
                "detail": "Unable to add the investor to the fund",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(path="/add_administrator")
async def add_administrator(
    add_administrator_to_fund: AddAdministratorToFund,
) -> Response:
    postgres = PostgreSQLCrud()
    result = postgres.add_administrator_to_fund(
        add_administrator_to_fund.administrator_id,
        add_administrator_to_fund.fund,
    )

    if result:
        return JSONResponse(
            content={
                "detail": "Administrator correctly added to the fund",
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={
                "detail": "Unable to add the administrator to the fund",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put(path="/update_commission")
async def update_commission(
    commission: Commission,
) -> Response:
    postgres = PostgreSQLCrud()
    result = postgres.update_commission(commission=commission)

    if result:
        return JSONResponse(
            content={
                "detail": "Commission information correctly updated",
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={
                "detail": "Unable to update the commission information",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
