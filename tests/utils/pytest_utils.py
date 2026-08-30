import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        elif "structure" in item.name:
            item.add_marker(pytest.mark.structure)
        elif "unit" in item.name:
            item.add_marker(pytest.mark.unit)
        elif "unit_schema" in item.name:
            item.add_marker(pytest.mark.unit_schema)
