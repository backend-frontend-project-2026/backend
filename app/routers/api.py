from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.chats import router as chats_router
from app.routers.cities import router as cities_router
from app.routers.complaints import router as complaints_router
from app.routers.deals import router as deals_router
from app.routers.dorms import router as dorms_router
from app.routers.faculties import router as faculties_router
from app.routers.media import router as media_router
from app.routers.messages import router as messages_router
from app.routers.neighbourhoods import router as neighbourhoods_router
from app.routers.profiles import router as profiles_router
from app.routers.reactions import router as reactions_router
from app.routers.references import router as references_router
from app.routers.roles import router as roles_router
from app.routers.tags import router as tags_router
from app.routers.universities import router as universities_router
from app.routers.users import router as users_router

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(users_router)
api_router.include_router(profiles_router)
api_router.include_router(deals_router)
api_router.include_router(reactions_router)

api_router.include_router(chats_router)
api_router.include_router(messages_router)
api_router.include_router(complaints_router)

api_router.include_router(universities_router)
api_router.include_router(faculties_router)
api_router.include_router(dorms_router)
api_router.include_router(neighbourhoods_router)
api_router.include_router(tags_router)
api_router.include_router(auth_router)
api_router.include_router(roles_router)
api_router.include_router(cities_router)
api_router.include_router(media_router)
api_router.include_router(references_router)