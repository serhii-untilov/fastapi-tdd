from enum import Enum

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class Status(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
