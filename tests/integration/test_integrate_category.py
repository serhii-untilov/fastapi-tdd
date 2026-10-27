# from app.models import category
from app.models.category import Category
from app.schemas.responses import Status
from tests.factories.models_factory import get_random_category_dict

# def test_integrate_test_a(client, db_session_integration):
#     category_data = get_random_category_dict()
#     new_category = Category(**category_data)
#     db_session_integration.add(new_category)
#     db_session_integration.commit()
#
#
# def test_integrate_test_b(client, db_session_integration):
#     category_data = get_random_category_dict()
#     new_category = Category(**category_data)
#     db_session_integration.add(new_category)
#     db_session_integration.commit()


def test_integrate_create_category_successfully(client, db_session_integration):
    # Arrange: Prepare test data

    category = get_random_category_dict()
    category.pop("id")

    # Act

    response = client.post("api/category/", json=category)

    # Assert

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["id"] is not None

    response_id = response_data["id"]
    found = db_session_integration.query(Category).filter(Category.id == response_id).first()

    assert found is not None

    found_data = {column.name: getattr(found, column.name) for column in found.__table__.columns}
    found_data.pop("id")

    assert category == found_data


def test_integrate_create_category_duplicate(client, db_session_integration):
    category_data = get_random_category_dict()
    category = Category(**category_data)
    db_session_integration.add(category)
    db_session_integration.commit()
    category_data.pop("id")

    response = client.post("api/category/", json=category_data)

    assert response.status_code == 400


def test_integrate_create_category_duplicate_slug(client, db_session_integration):
    category1 = get_random_category_dict()
    category2 = get_random_category_dict()

    category1["slug"] = "same-slug"
    category2["slug"] = "same-slug"

    db_session_integration.add(Category(**category1))
    db_session_integration.commit()

    response = client.post("api/category/", json=category2)

    assert response.status_code == 400


def test_integrate_get_all_categories(client, db_session_integration):
    # Arrange: Prepare test data

    categories = [get_random_category_dict() for i in range(5)]
    for category_data in categories:
        category = Category(**category_data)
        db_session_integration.add(category)
        db_session_integration.commit()

    # Act

    response = client.get("api/category/")

    # Assert

    assert response.status_code == 200
    assert response.json() is not None

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == len(categories)

    for response_category, category in zip(response_data, categories, strict=True):
        assert response_category["name"] == category["name"]
        assert response_category["slug"] == category["slug"]
        assert response_category["is_active"] == category["is_active"]
        assert response_category["level"] == category["level"]


def test_integrate_update_category_successfully(client, db_session_integration):
    initial_category_data = get_random_category_dict()
    new_category = Category(**initial_category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()

    updated_category_data = {
        "name": "Updated Name",
        "slug": "updated-slug",
        "is_active": False,
        "level": 10,
    }

    response = client.put(f"/api/category/{new_category.id}", json=updated_category_data)

    assert response.status_code == 200
    assert response.json() == Status.SUCCESS

    response = client.get(f"/api/category/slug/{updated_category_data['slug']}")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == updated_category_data["name"]
    assert response_data["slug"] == updated_category_data["slug"]
    assert response_data["is_active"] == updated_category_data["is_active"]
    assert response_data["level"] == updated_category_data["level"]


def test_integrate_delete_category_successfully(client, db_session_integration):
    category_data = get_random_category_dict()
    category = Category(**category_data)
    db_session_integration.add(category)
    db_session_integration.commit()

    response = client.delete(f"/api/category/{category.id}")

    assert response.status_code == 200
    assert response.json() == Status.SUCCESS

    deleted_category = db_session_integration.query(Category).filter_by(id=category.id).first()

    assert deleted_category is None
