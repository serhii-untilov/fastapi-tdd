from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class CategoryBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    slug: Annotated[str, StringConstraints(min_length=1, max_length=120)]
    is_active: bool | None = True
    level: int | None = 1
    parent_id: int | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryReturn(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
