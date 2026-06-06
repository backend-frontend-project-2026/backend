from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ConfirmAccountRequest(BaseModel):
    user_id: int
    code: str = Field(min_length=1, max_length=64)


class RequestPasswordResetRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    user_id: int
    code: str = Field(min_length=1, max_length=64)
    new_password: str = Field(min_length=8, max_length=128)
    new_password_repeat: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)
    new_password_repeat: str = Field(min_length=8, max_length=128)


class MessageResponse(BaseModel):
    message: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'