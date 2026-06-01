from typing import Any

from pydantic import BaseModel, Field


class ErrorDetails(BaseModel):
    optional: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    details: ErrorDetails = Field(default_factory=ErrorDetails)
    message: str