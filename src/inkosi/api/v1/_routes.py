from fastapi import APIRouter

from .endpoints.admin.scheduler import router as scheduler_router

v1_router = APIRouter()
v1_router.include_router(
    scheduler_router,
    tags=["Scheduler"],
)
