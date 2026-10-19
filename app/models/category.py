from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Category(Base):
    __tablename__ = "categories"

    # id = Column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="categories_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="categories_slug_length_check"),
        UniqueConstraint("name", "level", name="uq_categories_name_level"),
        UniqueConstraint("slug", name="uq_categories_slug"),
    )
