from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    level = Column(Integer, nullable=False, default=1, server_default="1")
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="categories_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="categories_slug_length_check"),
        UniqueConstraint("name", "level", name="uq_categories_name_level"),
        UniqueConstraint("slug", name="uq_categories_slug"),
    )
