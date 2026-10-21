from typing import Any

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.category import Category
from app.schemas.category_schema import CategoryCreate
from tests.factories.models_factory import get_random_category_dict


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value  # noqa: ARG005


@pytest.mark.parametrize("category", (get_random_category_dict() for _ in range(3)))
def test_unit_get_single_category_successfully(client, monkeypatch, category):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category))
    response = client.get(f"api/category/{category['slug']}")
    assert response.status_code == 200
    assert response.json() == category


@pytest.mark.parametrize("category", (get_random_category_dict() for _ in range(3)))
def test_unit_get_single_category_not_found(client, monkeypatch, category):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    response = client.get(f"api/category/{category['slug']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


@pytest.mark.parametrize("category", (get_random_category_dict() for _ in range(3)))
def test_unit_get_single_category_with_internal_server_error(client, monkeypatch, category):
    def mock_exception():
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_exception)
    response = client.get(f"api/category/{category['slug']}")
    assert response.status_code == 500


# Test category schema data validation
def test_unit_schema_category_validation():
    valid_data: dict[str, Any] = {
        "name": "Test category",
        "slug": "test-category",
    }

    category = CategoryCreate(**valid_data)
    assert category.name == "Test category"
    assert category.slug == "test-category"
    assert category.is_active
    assert category.level == 1
    assert category.parent_id is None

    invalid_data: dict[str, Any] = {
        "name": "Test category",
    }

    with pytest.raises(ValidationError):
        category = CategoryCreate(**invalid_data)


# Test GET all categories successfully
def test_unit_get_all_categories_successfully(client, monkeypatch):
    category = [get_random_category_dict(i) for i in range(5)]
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(category))
    response = client.get("api/category/")
    assert response.status_code == 200
    assert response.json() == category


def test_unit_get_all_categories_return_empty(client, monkeypatch):
    category = []
    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_output(category))
    response = client.get("api/category/")
    assert response.status_code == 200
    assert response.json() == []


def test_unit_get_all_category_with_internal_server_error(client, monkeypatch):
    def mock_create_category_exception():
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_create_category_exception)

    response = client.get("api/category/")
    assert response.status_code == 500


# Test POST new category successfully
def test_unit_create_category_successfully(client, monkeypatch):
    category_data = get_random_category_dict()

    # for key, value in category_data.items():
    # monkeypatch.setattr(Category, key, value)
    monkeypatch.setattr(Category, "id", category_data["id"])

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    body = category_data.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)

    assert response.status_code == 201
    # assert response.json()["id"] == category_data["id"]
    # with pytest.raises(KeyError):
    #     response.json()["name"]
    assert response.json() == {"id": category_data["id"]}


@pytest.mark.parametrize(
    "existing_category, category_data, expected_detail",
    [
        (True, get_random_category_dict(), "Category with this name and level exists"),
        (True, get_random_category_dict(), "Category with this slug exists"),
    ],
)
def test_unit_create_category_existing(
    client, monkeypatch, existing_category, category_data, expected_detail
):
    def mock_check_existing_category(db, category_data):
        if existing_category:
            raise HTTPException(status_code=400, detail=expected_detail)

    monkeypatch.setattr(
        "app.routers.category_routes.check_existing_category",
        mock_check_existing_category,
    )

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())

    body = category_data.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)

    assert response.status_code == 400

    if expected_detail:
        assert response.json() == {"detail": expected_detail}


def test_unit_create_category_with_internal_server_error(client, monkeypatch):
    category_data = get_random_category_dict()

    def mock_create_category_exception(*args, **kwargs):
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_create_category_exception)

    body = category_data.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)
    assert response.status_code == 500
