from sqlalchemy import UUID, Boolean, DateTime, Enum, Integer, String, Text

# Table and Column Validation


## Confirm the presence of all required tables within the database schema.
# @pytest.mark.model - see tests/utils/pytest_utils.py
def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("products")


## Validate the existence of expected columns in each table, ensuring correct data types.
# @pytest.mark.structure - see tests/utils/pytest_utils.py
def test_model_structure_table_column_data_types(db_inspector):
    table = "products"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["pid"]["type"], UUID)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["description"]["type"], Text)
    assert isinstance(columns["is_digital"]["type"], Boolean)
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["updated_at"]["type"], DateTime)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["stock_status"]["type"], Enum)
    assert isinstance(columns["category_id"]["type"], Integer)
    assert isinstance(columns["seasonal_event"]["type"], Integer)
    assert isinstance(columns["product_type"]["type"], Integer)


## Verify nullable or not nullable fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "products"
    columns = db_inspector.get_columns(table)
    expected_nullable = {
        "id": False,
        "pid": False,
        "name": False,
        "slug": False,
        "description": True,
        "is_digital": False,
        "created_at": False,
        "updated_at": False,
        "is_active": False,
        "stock_status": False,
        "category_id": False,
        "seasonal_event": False,
        "product_type": False,
    }
    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(column_name), (
            f"column '{column_name}' is not nullable as expected"
        )


## Test columns with specific constraints to ensure they are accurately defined.
def test_model_structure_column_constraints(db_inspector):
    table = "products"
    constraints = db_inspector.get_check_constraints(table)
    # print(constraints)
    assert any(constraint["name"] == "products_name_length_check" for constraint in constraints)
    assert any(constraint["name"] == "products_slug_length_check" for constraint in constraints)


## Verify the correctness of default values for relevant columns.
def test_model_structure_default_values(db_inspector):
    table = "products"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert columns["is_active"]["default"] == "true"
    assert columns["stock_status"]["default"] == "'oos'::status_enum"


## Ensure that column lengths align with defined requirements.
def test_model_structure_column_length(db_inspector):
    table = "products"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert columns["name"]["type"].length == 200
    assert columns["slug"]["type"].length == 220


## Test columns with specific constraints to ensure they are accurately defined.
def test_model_structure_unique_constraints(db_inspector):
    table = "products"
    constraints = db_inspector.get_unique_constraints(table)
    # print(constraints)
    assert any(constraint["name"] == "uq_products_pid" for constraint in constraints)
    assert any(constraint["name"] == "uq_products_slug" for constraint in constraints)
