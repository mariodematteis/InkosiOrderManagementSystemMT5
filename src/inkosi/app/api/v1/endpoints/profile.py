from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from inkosi.database.postgresql.database import PostgreSQLCrud
from inkosi.database.postgresql.models import LoginCredentials
from inkosi.log.log import Logger

router = APIRouter()

logger = Logger(module_name="Profile", package_name="api")


@router.get(path="/login")
async def login(credentials: LoginCredentials) -> Response:
    postgresql = PostgreSQLCrud()
    records = postgresql.get_users(
        email_address=credentials.EmailAddress, password=credentials.Password
    )

    match len(records):
        case 0:
            logger.warn(
                "Unable to locate the user with the following E-mail Address:"
                f" {credentials.EmailAddress}"
            )

            return JSONResponse(
                content={
                    "detail": (
                        "Unable to locate the user through the E-mail Address given"
                    )
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        case 1:
            return JSONResponse(
                content={
                    "detail": (
                        "Unable to locate the user through the E-mail Address given"
                    )
                },
                status_code=status.HTTP_200_OK,
            )
        case 2:
            roles = set([user.get("Role", "") for user in records])
            if "" in roles:
                return JSONResponse(
                    content={"detail": "The Key selected is not correct"},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            if len(roles) == 1:
                return JSONResponse(
                    content={
                        "detail": (
                            "Two users have been identified using the same E-mail"
                            " Address"
                        ),
                    },
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return JSONResponse(
                content={
                    "detail": (
                        "The user have been identifie with two different type of roles"
                    )
                },
                status_code=status.HTTP_200_OK,
            )
        case _:
            logger.critical(
                message=(
                    "More than two users have been found with the following E-mail"
                    f" Address: {credentials.EmailAddress}"
                )
            )
            return JSONResponse(
                content={
                    "detail": (
                        "More than two users have been found with the E-mail Address"
                        " given"
                    )
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
