# from app.models import category
from app.models.category import Category
from tests.factories.models_factory import get_random_category_dict


def test_integrate_test_a(client, db_session_integration):
    category_data = get_random_category_dict()
    new_category = Category(**category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()


def test_integrate_test_b(client, db_session_integration):
    category_data = get_random_category_dict()
    new_category = Category(**category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()


def test_integrate_create_category_successfully(client, db_session_integration):
    # Arrange: Prepare test data
    category = get_random_category_dict()
    category_data = category.pop("id")

    # Act
    response = client.post("api/category/", json=category_data)

    # Assert: Verify response
    assert response.status_code == 201
