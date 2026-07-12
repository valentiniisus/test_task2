"""Response shapes for dummyjson.com POST /auth/login."""

from pydantic import BaseModel, ConfigDict


class LoginSuccess(BaseModel):
    model_config = ConfigDict(extra="allow")  # API can add fields over time

    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
    accessToken: str
    refreshToken: str


class LoginError(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str
