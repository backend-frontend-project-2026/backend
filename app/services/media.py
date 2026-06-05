import uuid
from pathlib import Path
from typing import Optional

import anyio
from fastapi import UploadFile

from app.core.settings import settings
from app.models.media import MediaKind, MediaModel, MediaUploadResponse
from app.utils.repository import Repository

ALLOWED_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class MediaService:
    def __init__(self, repository: Repository[MediaModel]):
        self._repository = repository

    async def upload(
        self, file: UploadFile, kind: Optional[MediaKind] = None
    ) -> MediaUploadResponse:
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            from app.exceptions.base import BadRequestError

            raise BadRequestError('Unsupported file type')

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            from app.exceptions.base import BadRequestError

            raise BadRequestError('File too large')

        ext = Path(file.filename or 'file').suffix or '.jpg'
        subfolder = kind.value if kind else 'other'
        filename = f'{subfolder}/{uuid.uuid4().hex}{ext}'

        dest = Path(settings.MEDIA_DIR) / filename
        await anyio.to_thread.run_sync(lambda: (dest.parent.mkdir(parents=True, exist_ok=True), dest.write_bytes(content)))

        url = f'{settings.MEDIA_BASE_URL}/{filename}'

        record = MediaModel(
            kind=kind,
            filename=filename,
            original_filename=file.filename or '',
            content_type=file.content_type,
            file_size=len(content),
            url=url,
        )
        saved = await self._repository.save(record)
        return MediaUploadResponse.model_validate(saved)
