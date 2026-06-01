import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.db.engine import async_session_maker
from app.services.bootstrap import bootstrap_roles_and_permissions


async def main() -> None:
    async with async_session_maker() as session:
        await bootstrap_roles_and_permissions(session)


if __name__ == '__main__':
    asyncio.run(main())