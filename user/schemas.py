from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    created_at: str
    updated_at: str

    @staticmethod
    def format_datetime(value: datetime) -> str:
        return value.isoformat()

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            login=obj.login,
            name=obj.name,
            created_at=cls.format_datetime(obj.created_at),
            updated_at=cls.format_datetime(obj.updated_at),
        )


class LoginRequest(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
