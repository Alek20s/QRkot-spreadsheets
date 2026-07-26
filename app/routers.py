# app/routers.py
from fastapi import APIRouter

from app.api.endpoints.charity_project import (
    router as charity_project_router,
)
from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.yandex_api import router as yandex_router

main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['Charity Projects'],
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donations'],
)
main_router.include_router(
    yandex_router,
    prefix='/yandex',
    tags=['Yandex Disk'],
)
