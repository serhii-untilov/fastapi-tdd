import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        if "structure" in item.name:
            item.add_marker(pytest.mark.structure)
        if "unit" in item.name:
            item.add_marker(pytest.mark.unit)
        if "schema" in item.name:
            item.add_marker(pytest.mark.schema)
        if "integrate" in item.name:
            item.add_marker(pytest.mark.integrate)
