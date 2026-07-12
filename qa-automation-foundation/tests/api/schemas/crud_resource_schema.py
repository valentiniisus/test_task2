"""Shape of a resource in the local Flask fixture backend
(tests/api/fixtures/fixture_server.py, seeded from db.json)."""

from pydantic import BaseModel


class Resource(BaseModel):
    id: int
    name: str
    job: str
