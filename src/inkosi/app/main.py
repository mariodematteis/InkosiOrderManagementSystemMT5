from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from inkosi import __project_name__, __version__
from inkosi.app import _constants
from inkosi.app.api.v1._routes import v1_router
from inkosi.app.dependencies import authentication, network_policies_check
from inkosi.database.mongodb.database import MongoDBInstance
from inkosi.database.postgresql.models import get_instance
from inkosi.log.log import Logger

_API_HEALTHCHECK = "OK"
_API_DESCRIPTION = "Inkosi API"
_API_STATUS = "active"

logger = Logger(module_name="Main", package_name="app")

templates = Jinja2Templates(directory="templates")

app = FastAPI(title=_constants.APPLICATION_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    path="/templates/stylesheets",
    app=StaticFiles(directory="templates/stylesheets"),
    name="stylesheets",
)
app.mount(
    path="/templates/contents",
    app=StaticFiles(directory="templates/contents"),
    name="contents",
)
app.mount(
    path="/templates/scripts",
    app=StaticFiles(directory="templates/scripts"),
    name="scripts",
)
app.include_router(
    v1_router,
    prefix=_constants.API + _constants.V1,
    dependencies=[Depends(authentication), Depends(network_policies_check)],
)


@app.on_event("startup")
async def startup_event() -> None:
    mongo_manager = MongoDBInstance()
    if not mongo_manager.is_connected():
        logger.error("Unable to connect to the MongoDB Instance")

    get_instance().connect()


@app.on_event(event_type="shutdown")
async def shutdown() -> None:
    ...


@app.get(
    path="/",
    summary="WebPage for logging to the platform",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def login_page(request: Request):
    """
    Login WebPage Endpoint

    Parameters
    ----------
    request : Request
        Headers and other information

    Returns
    -------
    _TemplateResponse
        HTML Page for Login
    """
    return templates.TemplateResponse(
        _constants.webpages.LOGIN,
        context={"request": request},
    )


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
