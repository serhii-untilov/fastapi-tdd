import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_connection import get_db_session
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryReturn
from app.schemas.responses import IdResponse

router = APIRouter()

router.prefix = "/category"
router.tags = ["Category"]

logger = logging.getLogger(__name__)


@router.get("/slug/{slug}", response_model=CategoryReturn)
def get_category_by_slug(
    slug: str,
    db: Session = Depends(get_db_session),
):
    try:
        category = db.query(Category).filter(Category.slug == slug).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


# Endpoint to retrieve all categories
@router.get("/", response_model=list[CategoryReturn])
def category_list(db: Session = Depends(get_db_session)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        logger.error(f"Unexpected error while getting category list: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.post("/", response_model=IdResponse, status_code=201)
def create_category(
    category_data: CategoryCreate, db: Session = Depends(get_db_session)
) -> IdResponse:
    try:
        check_existing_category(db, category_data)
        category = Category(**category_data.model_dump())
        db.add(category)
        db.flush()
        db.commit()
        # db.refresh(new_category)
        return IdResponse(id=category.id)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


def check_existing_category(db: Session, category_data: CategoryCreate):
    existing_category = (
        db.query(Category)
        .filter(
            (Category.slug == category_data.slug)
            | ((Category.name == category_data.name) & (Category.level == category_data.level))
        )
        .first()
    )
    if existing_category:
        if (
            existing_category.name == category_data.name
            and existing_category.level == category_data.level
        ):
            message = "Category with name and level already exists"
        else:
            message = "Category with slug already exists"
        raise HTTPException(status_code=400, detail=message)
