from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.dependencies.session import init_db
from app.routers.api import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


@app.get('/')
def main_page():
    return {'Hello': 'World'}
