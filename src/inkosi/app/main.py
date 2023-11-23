from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from inkosi import __project_name__, __version__
from inkosi.app import _constants
from inkosi.app.api.v1._routes import v1_router
from inkosi.database.mongodb.database import MongoDBInstance
from inkosi.database.postgresql.models import get_instance
from inkosi.log.log import Logger
from inkosi.portfolio.risk_management import RiskManagement

_API_HEALTHCHECK = "OK"
_API_DESCRIPTION = "Inkosi API"
_API_STATUS = "active"

logger = Logger(
    module_name="Main",
    package_name="app",
)

app = FastAPI(
    title=_constants.APPLICATION_NAME,
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    v1_router,
    prefix=_constants.API + _constants.V1,
)


@app.on_event(
    event_type="startup",
)
async def startup_event() -> None:
    mongo_manager = MongoDBInstance()
    if not mongo_manager.is_connected():
        logger.error(message="Unable to connect to the MongoDB Instance")

    get_instance().connect()

    RiskManagement()


@app.on_event(
    event_type="shutdown",
)
async def shutdown() -> None:
    RiskManagement().unload_model()


@app.get(
    path=_constants.HEALTHCHECK,
    summary=f"Get the healthcheck of {_constants.APPLICATION_NAME}",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def healthcheck() -> str:
    """
    Get the healthcheck of the application

    Returns
    -------
    str
        A message to ensure that the application is active
    """

    return _API_HEALTHCHECK


@app.get(
    path=_constants.STATUS,
    summary=f"Get the status of {_constants.APPLICATION_NAME}",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def status() -> dict[str, str]:
    """
    Get the status of the application

    Returns
    -------
    dict[str, str]
        A dictionary containing metadata about the status of the application
    """

    return {
        "name": __project_name__,
        "version": __version__,
        "description": _API_DESCRIPTION,
        "status": _API_STATUS,
    }
