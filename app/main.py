from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def main_page() -> dict[str, str]:
    return {'Hello': 'World'}
