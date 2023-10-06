from fastapi import Depends, FastAPI, status

from inkosi import __project_name__, __version__
from inkosi.api import _constants
from inkosi.api.dependencies import authentication, network_policies_check
from inkosi.api.v1._routes import v1_router
from inkosi.database.mongodb.database import MongoDBInstance
from inkosi.database.postgresql.models import instance

_API_HEALTHCHECK = "OK"
_API_DESCRIPTION = "Inkosi API"
_API_STATUS = "active"

app = FastAPI(title=_constants.APPLICATION_NAME)
app.include_router(
    v1_router,
    prefix=_constants.API + _constants.V1,
    dependencies=[Depends(authentication), Depends(network_policies_check)],
)


@app.on_event("startup")
async def startup_event() -> None:
    instance.base.metadata.create_all(bind=instance.engine)
    mongo_manager = MongoDBInstance()
    assert mongo_manager.is_connected


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
