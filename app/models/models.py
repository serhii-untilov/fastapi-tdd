from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from .base import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, nullable=False)
    alternative_text = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    product_line_id = Column(Integer, ForeignKey("product_lines.id"), nullable=False)

    __table_args__ = (
        CheckConstraint('"order" >= 1 AND "order" <= 20', name="product_image_order_range"),
        CheckConstraint(
            "LENGTH(alternative_text) > 0",
            name="product_image_alternative_length_check",
        ),
        CheckConstraint("LENGTH(url) > 0", name="product_image_url_length_check"),
        UniqueConstraint("order", "product_line_id", name="uq_product_image_order_product_line_id"),
    )


class SeasonalEvent(Base):
    __tablename__ = "seasonal_events"

    id = Column(Integer, primary_key=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0",
            name="seasonal_event_name_length_check",
        ),
        UniqueConstraint("name", name="uq_seasonal_event_name"),
    )


class Attribute(Base):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0",
            name="attribute_name_length_check",
        ),
        UniqueConstraint("name", name="uq_attribute_name"),
    )


class ProductType(Base):
    __tablename__ = "product_types"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    level = Column(
        Integer,
        nullable=False,
    )
    parent_id = Column(Integer, ForeignKey("product_types.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_type_name_length_check"),
        UniqueConstraint("name", "level", name="uq_product_type_name_level"),
    )


class AttributeValue(Base):
    __tablename__ = "attribute_values"

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_value = Column(String(100), nullable=False)
    attribute_id = Column(Integer, ForeignKey("attributes.id"), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(attribute_value) > 0", name="attribute_value_name_length_check"),
        UniqueConstraint("attribute_value", "attribute_id", name="uq_attribute_value_attribute_id"),
    )


class ProductLineAttributeValue(Base):
    __tablename__ = "product_line_attribute_values"

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_value_id = Column(Integer, ForeignKey("attribute_values.id"), nullable=False)
    product_line_id = Column(Integer, ForeignKey("product_lines.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "attribute_value_id",
            "product_line_id",
            name="uq_product_line_attribute_value",
        ),
    )


class ProductProductType(Base):
    __tablename__ = "product_product_types"

    id = Column(Integer, primary_key=True, nullable=False)
    product_type_id = Column(Integer, ForeignKey("product_types.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "product_type_id",
            "product_id",
            name="uq_product_id_product_type_id",
        ),
    )
