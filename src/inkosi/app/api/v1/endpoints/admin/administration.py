from fastapi import APIRouter

from inkosi.database.postgresql.database import PostgreSQLCrud

router = APIRouter()


@router.post(path="/list_portfolio_managers", response_model=list[dict])
def list_portfolio_managers(status: str | None = None):
    postgresql = PostgreSQLCrud()

    if status is None:
        return postgresql.get_portfolio_managers()
