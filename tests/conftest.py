import pytest
import importlib


@pytest.fixture(scope="session")
def httpmonitor():
    importlib.machinery.SOURCE_SUFFIXES.append('')
    spec = importlib.util.spec_from_file_location("httpmonitor", "httpmonitor")
    httpmonitor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(httpmonitor)
    return httpmonitor
