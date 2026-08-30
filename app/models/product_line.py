from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class ProductLine(Base):
    __tablename__ = "product_lines"

    id = Column(Integer, primary_key=True)
    price = Column(type(Numeric(precision=5, scale=2)), nullable=False)
    sku = Column(UUID, nullable=False)
    stock_qty = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    order = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    # attributes = Column(Integer, ForeignKey("product_line_attributes.id"), nullable=True)

    __table_args__ = (UniqueConstraint("sku", name="uq_product_lines_sku"),)
