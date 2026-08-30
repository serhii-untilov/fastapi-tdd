from sqlalchemy import Boolean, Integer, String

# Table and Column Validation


## Confirm the presence of all required tables within the database schema.
# @pytest.mark.model - see tests/utils/pytest_utils.py
def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("categories")


## Validate the existence of expected columns in each table, ensuring correct data types.
# @pytest.mark.structure - see tests/utils/pytest_utils.py
def test_model_structure_table_column_data_types(db_inspector):
    table = "categories"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)


## Verify nullable or not nullable fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "categories"
    columns = db_inspector.get_columns(table)
    expected_nullable = {
        "id": False,
        "name": False,
        "slug": False,
        "is_active": False,
        "level": False,
        "parent_id": True,
    }
    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(column_name), (
            f"column '{column_name}' is not nullable as expected"
        )


## Test columns with specific constraints to ensure they are accurately defined.
def test_model_structure_column_constraints(db_inspector):
    table = "categories"
    constraints = db_inspector.get_check_constraints(table)
    # print(constraints)
    assert any(constraint["name"] == "categories_name_length_check" for constraint in constraints)
    assert any(constraint["name"] == "categories_slug_length_check" for constraint in constraints)


## Verify the correctness of default values for relevant columns.
def test_model_structure_default_values(db_inspector):
    table = "categories"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert columns["is_active"]["default"] == "true"
    assert columns["level"]["default"] == "1"


## Ensure that column lengths align with defined requirements.
def test_model_structure_column_length(db_inspector):
    table = "categories"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert columns["name"]["type"].length == 100
    assert columns["slug"]["type"].length == 120


## Test columns with specific constraints to ensure they are accurately defined.
def test_model_structure_unique_constraints(db_inspector):
    table = "categories"
    constraints = db_inspector.get_unique_constraints(table)
    # print(constraints)
    assert any(constraint["name"] == "uq_categories_name_level" for constraint in constraints)
    assert any(constraint["name"] == "uq_categories_slug" for constraint in constraints)
