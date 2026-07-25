from fastapi import FastAPI

from app.api.endpoints.charity_project import (
    router as charity_project_router,
)
from app.api.endpoints.donation import router as donation_router
from app.core.config import settings
from app.core.db import Base, engine
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['Charity Projects'],
)
app.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donations'],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes if route.name != 'users:delete_user'
]
app.include_router(users_router, prefix='/users', tags=['users'])


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
