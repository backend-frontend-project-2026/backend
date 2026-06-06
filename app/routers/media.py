from typing import Optional

from fastapi import APIRouter, Security, UploadFile

from app.dependencies.auth import get_current_user
from app.dependencies.services import MediaServiceDep
from app.exceptions.responses import bad_request_response, internal_server_error_response
from app.models.media import MediaKind, MediaUploadResponse
from app.models.users import UserModel

router = APIRouter(prefix='/media', tags=['Media'])


@router.post(
    '/upload',
    response_model=MediaUploadResponse,
    status_code=201,
    responses={**bad_request_response, **internal_server_error_response},
)
async def upload_media(
    file: UploadFile,
    media_service: MediaServiceDep,
    kind: Optional[MediaKind] = None,
    _current_user: UserModel = Security(get_current_user, scopes=['media:upload']),
):
    return await media_service.upload(file, kind)
