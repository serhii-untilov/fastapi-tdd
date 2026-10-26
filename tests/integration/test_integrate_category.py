# from app.models import category
from app.models.category import Category
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


# def test_integrate_create_category_successfully(client, db_session_integration):
#     # Arrange: Prepare test data
#
#     category = get_random_category_dict()
#     category.pop("id")
#
#     # Act
#
#     response = client.post("api/category/", json=category)
#
#     # Assert
#
#     assert response.status_code == 201
#
#     response_data = response.json()
#
#     assert response_data["id"] is not None
#
#     response_id = response_data["id"]
#     found = db_session_integration.query(Category).filter(Category.id == response_id).first()
#
#     assert found is not None
#
#     found_data = {column.is_active: getattr(found, column.name) for column in found.__table__.columns}
#     found_data.pop("id")
#
#     assert category == found_data
#
#
# def test_integrate_create_category_duplicate(client, db_session_integration):
#     category_data = get_random_category_dict()
#     category = Category(**category_data)
#     db_session_integration.add(category)
#     db_session_integration.commit()
#     category_data.pop("id")
#
#     response = client.post("api/category/", json=category_data)
#
#     assert response.status_code == 400
#


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
