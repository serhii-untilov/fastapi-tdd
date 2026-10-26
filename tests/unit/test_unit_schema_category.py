from typing import Any

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.category import Category
from app.schemas.category_schema import CategoryCreate
from app.schemas.responses import Status
from tests.factories.models_factory import get_random_category_dict


def mock_output(return_value=None):
    return lambda *args, **kwargs: return_value  # noqa: ARG005


# Test Delete a category


def test_unit_delete_category_successfully(client, monkeypatch):
    category_dict = get_random_category_dict()
    category_instance = Category(**category_dict)

    monkeypatch.setattr(Category, "id", category_dict["id"])
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category_instance))
    monkeypatch.setattr("sqlalchemy.orm.Session.delete", mock_output(category_instance))
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    response = client.delete(f"api/category/{category_dict['id']}")

    assert response.status_code == 200
    assert response.json() == Status.SUCCESS


def test_unit_delete_category_not_found(client, monkeypatch):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    response = client.delete("api/category/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_unit_delete_category_internal_error(client, monkeypatch):
    def mock_exception():
        raise Exception("Internal error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_exception)

    response = client.delete("api/category/1")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal error"}


# Test PUT update a category


def test_unit_update_category_successfully(client, monkeypatch):
    category_dict = get_random_category_dict()
    category_instance = Category(**category_dict)

    monkeypatch.setattr(Category, "id", category_dict["id"])
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category_instance))
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    body = category_dict.copy()
    body.pop("id")
    response = client.put(f"api/category/{category_dict['id']}", json=body)

    assert response.status_code == 200
    assert response.json() == Status.SUCCESS


def test_unit_update_category_not_found(client, monkeypatch):
    category_dict = get_random_category_dict()

    monkeypatch.setattr(Category, "id", category_dict["id"])
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    body = category_dict.copy()
    body.pop("id")

    response = client.put(f"api/category/{category_dict['id']}", json=body)

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_unit_update_category_internal_error(client, monkeypatch):
    category = get_random_category_dict()

    def mock_exception():
        raise Exception("Internal error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_exception)

    body = category.copy()
    body.pop("id")

    response = client.put(f"api/category/{category['id']}", json=body)

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal error"}


# Test get a single category


@pytest.mark.parametrize("category", (get_random_category_dict() for _ in range(3)))
def test_unit_get_single_category_successfully(client, monkeypatch, category):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output(category))
    response = client.get(f"api/category/slug/{category['slug']}")
    assert response.status_code == 200
    assert response.json() == category


@pytest.mark.parametrize("category", (get_random_category_dict() for _ in range(3)))
def test_unit_get_single_category_not_found(client, monkeypatch, category):
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    response = client.get(f"api/category/slug/{category['slug']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


@pytest.mark.parametrize("category", (get_random_category_dict() for _ in range(3)))
def test_unit_get_single_category_with_internal_server_error(client, monkeypatch, category):
    def mock_exception():
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_exception)
    response = client.get(f"api/category/slug/{category['slug']}")
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


# Test GET all categories


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
    def mock_exception():
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.all", mock_exception)
    response = client.get("api/category/")
    assert response.status_code == 500


# Test POST new category


def test_unit_create_category_successfully(client, monkeypatch):
    category_data = get_random_category_dict()

    monkeypatch.setattr(Category, "id", category_data["id"])
    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_output())

    body = category_data.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)

    assert response.status_code == 201
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
    def mock_check_existing_category(_db, _category_data):
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

    def mock_exception():
        raise Exception("Internal server error")

    monkeypatch.setattr("sqlalchemy.orm.Query.first", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.flush", mock_output())
    monkeypatch.setattr("sqlalchemy.orm.Session.commit", mock_exception)

    body = category_data.copy()
    body.pop("id")
    response = client.post("api/category/", json=body)
    assert response.status_code == 500
