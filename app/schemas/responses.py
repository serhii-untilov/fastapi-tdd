from enum import Enum

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class Status(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
