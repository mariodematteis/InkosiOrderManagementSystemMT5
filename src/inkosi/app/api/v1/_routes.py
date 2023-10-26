from fastapi import APIRouter

from .endpoints.admin.administration import router as administration_router
from .endpoints.admin.operations import router as operations_router
from .endpoints.admin.scheduler import router as scheduler_router
from .endpoints.admin.trades import router as trades_router
from .endpoints.profile import router as profile_router

v1_router = APIRouter()

v1_router.include_router(administration_router, tags=["Administrator"])
v1_router.include_router(operations_router, tags=["Operations"])
v1_router.include_router(scheduler_router, tags=["Scheduler"])
v1_router.include_router(trades_router, tags=["Trades"])
v1_router.include_router(profile_router, tags=["Profile"])
