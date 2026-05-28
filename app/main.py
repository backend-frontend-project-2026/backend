from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.engine import async_session_maker
from app.routers.api import api_router
from app.services.bootstrap import bootstrap_roles_and_permissions


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await bootstrap_roles_and_permissions(session)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)