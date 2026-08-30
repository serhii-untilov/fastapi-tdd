from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    pid = Column(UUID, nullable=False)
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False)
    description = Column(Text, nullable=True)
    is_digital = Column(Boolean, nullable=False, default=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    stock_status = Column(
        Enum("oos", "is", "obo", name="status_enum"),
        nullable=False,
        server_default="oos",
    )
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    seasonal_event = Column(Integer, ForeignKey("seasonal_events.id"), nullable=False)
    product_type = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="products_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="products_slug_length_check"),
        UniqueConstraint("pid", name="uq_products_pid"),
        UniqueConstraint("slug", name="uq_products_slug"),
    )
