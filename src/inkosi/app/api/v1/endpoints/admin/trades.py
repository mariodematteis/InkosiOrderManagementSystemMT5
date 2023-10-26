from fastapi import APIRouter

from inkosi.app.schemas import Order

router = APIRouter()


@router.post(path="/execute_order")
def execute_order(order: Order):
    return
