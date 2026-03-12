from fastapi import FastAPI
from app.db.engine import create_db_and_tables

app = FastAPI()

@app.get('/')
async def main_page() -> dict[str, str]:
    return {'Hello': 'World'}
