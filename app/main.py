from fastapi import FastAPI
from app.db.engine import create_db_and_tables

app = FastAPI()

@app.get('/')
def main_page():
    return {'Hello': 'World'}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
