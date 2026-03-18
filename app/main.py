from fastapi import FastAPI
from app.db.engine import create_db_and_tables

from app.db.engine import create_db_and_tables

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    yield


app = FastAPI(lifespan=lifespan)

@app.get('/')
def main_page():
    return {'Hello': 'World'}
