from sqlalchemy import UUID, Boolean, Float, Integer, Numeric

# Table and Column Validation


## Confirm the presence of all required tables within the database schema.
# @pytest.mark.model - see tests/utils/pytest_utils.py
def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("product_lines")


## Validate the existence of expected columns in each table, ensuring correct data types.
# @pytest.mark.structure - see tests/utils/pytest_utils.py
def test_model_structure_table_column_data_types(db_inspector):
    table = "product_lines"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["price"]["type"], type(Numeric(precision=5, scale=2)))
    assert isinstance(columns["sku"]["type"], UUID)
    assert isinstance(columns["stock_qty"]["type"], Integer)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["order"]["type"], Integer)
    assert isinstance(columns["weight"]["type"], Float)
    assert isinstance(columns["product_id"]["type"], Integer)
    # assert isinstance(columns["attributes"]["type"], Integer)


## Verify nullable or not nullable fields
def test_model_structure_nullable_constraints(db_inspector):
    table = "product_lines"
    columns = db_inspector.get_columns(table)
    expected_nullable = {
        "id": False,
        "price": False,
        "sku": False,
        "stock_qty": False,
        "is_active": False,
        "order": False,
        "weight": False,
        "product_id": False,
        "attributes": True,
    }
    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(column_name), (
            f"column '{column_name}' is not nullable as expected"
        )


## Test columns with specific constraints to ensure they are accurately defined.
# def test_model_structure_column_constraints(db_inspector):
#     table = "product_lines"
#     constraints = db_inspector.get_check_constraints(table)
#     # print(constraints)
#     assert any(constraint["name"] == "products_name_length_check" for constraint in constraints)
#     assert any(constraint["name"] == "products_slug_length_check" for constraint in constraints)


## Verify the correctness of default values for relevant columns.
def test_model_structure_default_values(db_inspector):
    table = "product_lines"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert columns["is_active"]["default"] == "true"


## Ensure that column lengths align with defined requirements.
# def test_model_structure_column_length(db_inspector):
#     table = "product_lines"
#     columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
#     assert columns["name"]["type"].length == 200
#     assert columns["slug"]["type"].length == 220


## Test columns with specific constraints to ensure they are accurately defined.
def test_model_structure_unique_constraints(db_inspector):
    table = "product_lines"
    constraints = db_inspector.get_unique_constraints(table)
    # print(constraints)
    assert any(constraint["name"] == "uq_product_lines_sku" for constraint in constraints)
