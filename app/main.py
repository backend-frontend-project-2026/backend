from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def main_page() -> dict[str, str]:
    return {'Hello': 'World'}
