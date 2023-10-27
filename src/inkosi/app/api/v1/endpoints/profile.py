import random
import string
from hashlib import sha256

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse

from inkosi.database.postgresql.database import PostgreSQLCrud
from inkosi.database.postgresql.models import Authentication
from inkosi.database.postgresql.schemas import LoginCredentials, UserRole
from inkosi.log.log import Logger

router = APIRouter()

logger = Logger(module_name="Profile", package_name="api")


@router.get(path="/login")
async def login(
    credentials: LoginCredentials,
    request: Request,
) -> Response:
    postgresql = PostgreSQLCrud()
    records = postgresql.get_users(
        email_address=credentials.email_address,
        password=credentials.password,
    )

    match len(records):
        case 0:
            logger.warn(
                message=(
                    "Unable to locate the user with the following E-mail Address:"
                    f" {credentials.email_address}"
                )
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
            if not UserRole.has(key=records[0].role):
                logger.warn(
                    message=(
                        "Unable to identify the role of user with the following ID and"
                        f" E-mail Address respectively: {records[0].id} and"
                        f" {records[0].email_address}"
                    )
                )
                return JSONResponse(
                    content={
                        "detail": "Unable to identify the role",
                    },
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            token_id: str = sha256(
                "".join(
                    [
                        random.choice(
                            list(set(string.ascii_uppercase).union(string.digits))
                        )
                        for _ in range(16)
                    ]
                ).encode()
            ).hexdigest()

            authentication = Authentication(
                id=token_id,
                user_type=records[0].role,
                user_id=records[0].id,
                ip_address=request.client.host,
            )

            postgresql.postgresql_instance.add(model=[authentication])

            return JSONResponse(
                content={
                    "detail": "Successfully logged in",
                    "role": records[0].role,
                    "token": token_id,
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
                        "The user have been identified with two different type of roles"
                    )
                },
                status_code=status.HTTP_200_OK,
            )
        case _:
            logger.critical(
                message=(
                    "More than two users have been found with the following E-mail"
                    f" Address: {credentials.email_address}"
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
