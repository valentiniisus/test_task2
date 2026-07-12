"""Response shapes for dummyjson.com GET /users."""

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="allow")  # dummyjson returns a lot more
    # (address, bank, crypto...) — only asserting on the subset we actually use

    id: int
    firstName: str
    lastName: str
    email: str
    username: str
    age: int
    gender: str


class UsersList(BaseModel):
    users: list[User]
    total: int
    skip: int
    limit: int
